"""
Simple demo version for better input visibility
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from model_loader import load_models
from batch_prediction import render_batch_prediction_page

# Helper functions for SHAP-like analysis
def calculate_income_impact(income, loan_amount):
    """Calculate income impact on loan approval"""
    debt_to_income = loan_amount / income
    if income < 40000:
        return -0.0234 if debt_to_income > 0.3 else -0.0156
    elif income < 60000:
        return -0.0089 if debt_to_income > 0.4 else 0.0023
    else:
        return 0.0156 if debt_to_income < 0.3 else 0.0089

def calculate_loan_amount_impact(loan_amount, income):
    """Calculate loan amount impact"""
    debt_to_income = loan_amount / income
    if debt_to_income > 0.5:
        return -0.0234
    elif debt_to_income > 0.3:
        return -0.0156
    elif debt_to_income > 0.2:
        return -0.0067
    else:
        return 0.0023

def calculate_age_impact(age):
    """Calculate age impact"""
    if age < 25:
        return -0.0034
    elif age < 35:
        return 0.0089
    elif age < 55:
        return 0.0123
    else:
        return 0.0067

def calculate_credit_history_impact(credit_length):
    """Calculate credit history impact"""
    if credit_length < 3:
        return -0.0089
    elif credit_length < 8:
        return 0.0045
    elif credit_length < 15:
        return 0.0067
    else:
        return 0.0089

def calculate_home_ownership_impact(ownership):
    """Calculate home ownership impact"""
    if ownership == 0:  # Rent
        return -0.0023
    elif ownership == 1:  # Own
        return 0.0045
    else:  # Mortgage
        return 0.0034

def calculate_employment_impact(emp_length):
    """Calculate employment length impact"""
    if emp_length < 2:
        return -0.0034
    elif emp_length < 5:
        return 0.0023
    elif emp_length < 10:
        return 0.0045
    else:
        return 0.0067

def calculate_loan_intent_impact(intent):
    """Calculate loan intent impact"""
    # 0: Personal, 1: Education, 2: Medical, 3: Venture, 4: Home improvement, 5: Debt consolidation
    intent_impacts = {0: -0.0012, 1: 0.0034, 2: 0.0023, 3: -0.0045, 4: 0.0067, 5: -0.0023}
    return intent_impacts.get(intent, 0)

def calculate_default_impact(default_history):
    """Calculate default history impact"""
    return -0.0089 if default_history == 1 else 0.0012

def get_feature_explanation(feature_name, impact, age, income, home_ownership, emp_length, 
                          loan_intent, loan_amount, default_on_file, credit_hist_length):
    """Get detailed explanation for each feature impact"""
    
    explanations = {
        'Thu nhập (person_income)': {
            'positive': f"Thu nhập ${income:,} của anh/chị nằm trong mức khá tốt, thể hiện khả năng tài chính ổn định và đủ khả năng chi trả khoản vay.",
            'negative': f"Thu nhập hiện tại ${income:,} của anh/chị thấp hơn mức trung bình mà chúng tôi thường chấp thuận, đây là yếu tố cản trở lớn nhất trong quyết định này."
        },
        'Số tiền vay (loan_amnt)': {
            'positive': f"Khoản vay ${loan_amount:,} phù hợp với khả năng tài chính hiện tại của anh/chị, tạo áp lực trả nợ ở mức hợp lý.",
            'negative': f"Khoản vay ${loan_amount:,} tương đối cao so với khả năng tài chính hiện tại (tỷ lệ {(loan_amount/income)*100:.1f}% thu nhập), tạo áp lực trả nợ đáng kể."
        },
        'Tuổi (person_age)': {
            'positive': f"Độ tuổi {age} của anh/chị nằm trong khoảng thuận lợi, thể hiện sự ổn định và kinh nghiệm trong công việc.",
            'negative': f"Độ tuổi {age} còn tương đối trẻ, có thể chưa có đủ kinh nghiệm tài chính và ổn định trong công việc."
        },
        'Lịch sử tín dụng (cb_person_cred_hist_length)': {
            'positive': f"Anh/chị có {credit_hist_length} năm lịch sử tín dụng khá tốt, điều này thể hiện sự uy tín trong việc thực hiện các cam kết tài chính.",
            'negative': f"Lịch sử tín dụng {credit_hist_length} năm còn tương đối ngắn, chưa đủ để đánh giá đầy đủ thói quen tài chính."
        },
        'Tình trạng sở hữu nhà (person_home_ownership)': {
            'positive': "Việc sở hữu tài sản bất động sản là điểm cộng tích cực trong hồ sơ của anh/chị, thể hiện tài sản đảm bảo.",
            'negative': "Việc chưa sở hữu nhà riêng có thể ảnh hưởng nhẹ đến đánh giá tài sản đảm bảo."
        },
        'Thời gian làm việc (person_emp_length)': {
            'positive': f"Kinh nghiệm làm việc {emp_length} năm ổn định góp phần tích cực vào đánh giá khả năng trả nợ.",
            'negative': f"Thời gian làm việc {emp_length} năm còn ít, có thể ảnh hưởng đến ổn định thu nhập trong tương lai."
        },
        'Mục đích vay (loan_intent)': {
            'positive': "Mục đích sử dụng khoản vay được đánh giá tích cực, có khả năng tạo ra giá trị hoặc cải thiện tình hình tài chính.",
            'negative': "Mục đích sử dụng khoản vay có ảnh hưởng nhẹ tiêu cực đến quyết định phê duyệt."
        },
        'Lịch sử nợ xấu (cb_person_default_on_file)': {
            'positive': "Không có lịch sử nợ xấu trong quá khứ, thể hiện thái độ trả nợ tích cực.",
            'negative': "Có dấu hiệu nhỏ về rủi ro tín dụng trong quá khứ, mặc dù không nghiêm trọng."
        }
    }
    
    explanation_type = 'positive' if impact > 0 else 'negative'
    return explanations.get(feature_name, {}).get(explanation_type, "Không có thông tin chi tiết.")

def generate_advice(income, loan_amount, age, emp_length, credit_hist_length, home_ownership, default_history, default_probability):
    """Generate personalized advice"""
    
    advice_parts = []
    
    if default_probability > 0.6:  # High risk
        advice_parts.append("Để cải thiện hồ sơ vay, anh/chị nên xem xét:")
        
        debt_to_income = loan_amount / income
        if debt_to_income > 0.3:
            reduction_percent = ((debt_to_income - 0.25) / debt_to_income) * 100
            advice_parts.append(f"• Giảm số tiền vay xuống khoảng {reduction_percent:.0f}% so với hiện tại (còn khoảng ${loan_amount * (1 - reduction_percent/100):,.0f})")
        
        if income < 50000:
            target_income = income * 1.3
            advice_parts.append(f"• Tăng thu nhập lên ít nhất ${target_income:,.0f} (tăng {((target_income - income)/income)*100:.0f}%)")
        
        if emp_length < 3:
            advice_parts.append("• Tích lũy thêm kinh nghiệm làm việc (ít nhất 3 năm)")
        
        if credit_hist_length < 5:
            advice_parts.append("• Xây dựng lịch sử tín dụng tích cực thêm vài năm")
            
    elif default_probability > 0.3:  # Medium risk
        advice_parts.append("Hồ sơ của anh/chị có tiềm năng, cần cải thiện một vài điểm:")
        
        if loan_amount / income > 0.25:
            advice_parts.append(f"• Giảm nhẹ số tiền vay xuống khoảng ${loan_amount * 0.8:,.0f}")
        
        if income < 60000:
            advice_parts.append("• Tăng thu nhập hoặc có thêm nguồn thu nhập phụ")
            
        advice_parts.append("• Tiếp tục duy trì lịch sử tín dụng tốt")
        
    else:  # Low risk
        advice_parts.append("Hồ sơ của anh/chị rất tốt! Một vài gợi ý để duy trì:")
        advice_parts.append("• Tiếp tục duy trì thu nhập ổn định")
        advice_parts.append("• Giữ tỷ lệ nợ/thu nhập ở mức thấp")
        advice_parts.append("• Duy trì lịch sử tín dụng tích cực")
    
    return "\n".join(advice_parts)

st.set_page_config(
    page_title="Demo Dự Đoán Rủi Ro Vay Vốn",
    page_icon="🎯",
    layout="wide"
)

def main():
    st.title("🤖 AI Model Analysis & Prediction Dashboard")
    
    # Sidebar navigation
    st.sidebar.title("🧭 Điều Hướng")
    page = st.sidebar.selectbox(
        "Chọn trang:",
        ["🎯 Demo Dự Đoán", "📊 Dự Đoán Hàng Loạt (CSV)", "🧠 Phân Tích LORA Model", "🌳 Phân Tích LightGBM", "📊 Feature Importance"]
    )
    
    # Load model - Remove cache to ensure SHAP explainer is properly loaded
    def load_model():
        return load_models(".")
    
    loader = load_model()
    
    # Check SHAP explainer status for sidebar
    if hasattr(loader, 'shap_explainer') and loader.shap_explainer:
        st.sidebar.success("✅ SHAP TreeExplainer loaded")
    else:
        st.sidebar.warning("⚠️ SHAP TreeExplainer not available")
    
    if page == "🎯 Demo Dự Đoán":
        render_prediction_page(loader)
    elif page == "📊 Dự Đoán Hàng Loạt (CSV)":
        render_batch_prediction_page(loader)
    elif page == "🧠 Phân Tích LORA Model":
        render_lora_analysis(loader)
    elif page == "🌳 Phân Tích LightGBM":
        render_lightgbm_analysis(loader)
    elif page == "📊 Feature Importance":
        render_feature_importance(loader)

def render_prediction_page(loader):
    st.markdown("# 🎯 Demo Dự Đoán Rủi Ro Vay Vốn")
    st.markdown("### Điền thông tin dưới đây để dự đoán khả năng được duyệt cho vay")
    
    if loader.lightgbm_model is None:
        st.error("❌ Không thể tải mô hình LightGBM")
        return
    
    st.success("✅ Mô hình đã sẵn sàng!")
    
    # Main layout: Left for inputs, Right for results
    main_col1, main_col2 = st.columns([1, 1])
    
    with main_col1:
        st.markdown("## 📝 THÔNG TIN ĐẦU VÀO")
        
        # Create two sub-columns for inputs
        input_col1, input_col2 = st.columns(2)
        
        with input_col1:
            st.markdown("#### 👤 Thông Tin Cá Nhân")
            
            # Age slider
            person_age = st.slider(
                "🎂 Tuổi của bạn", 
                min_value=18, max_value=80, value=35, step=1
            )
            st.write(f"Tuổi được chọn: **{person_age} tuổi**")
            
            # Income input
            person_income = st.number_input(
                "💰 Thu nhập hàng năm (USD)", 
                min_value=10000, max_value=500000, value=75000, step=1000
            )
            st.write(f"Thu nhập: **${person_income:,}**")
            
            # Home ownership
            home_options = ["Thuê nhà", "Sở hữu", "Thế chấp"]
            home_ownership_text = st.selectbox("🏠 Tình trạng nhà ở", home_options)
            home_ownership = home_options.index(home_ownership_text)
            st.write(f"Nhà ở: **{home_ownership_text}**")
            
            # Employment length
            emp_length = st.slider(
                "💼 Số năm làm việc", 
                min_value=0, max_value=20, value=5, step=1
            )
            st.write(f"Kinh nghiệm: **{emp_length} năm**")
        
        with input_col2:
            st.markdown("#### 💰 Thông Tin Khoản Vay")
            
            # Loan intent
            intent_options = ["Cá nhân", "Giáo dục", "Y tế", "Kinh doanh", "Cải thiện nhà", "Trả nợ"]
            loan_intent_text = st.selectbox("🎯 Mục đích vay", intent_options)
            loan_intent = intent_options.index(loan_intent_text)
            st.write(f"Mục đích: **{loan_intent_text}**")
            
            # Loan amount
            loan_amount = st.number_input(
                "💵 Số tiền muốn vay (USD)", 
                min_value=1000, max_value=50000, value=10000, step=500
            )
            st.write(f"Số tiền vay: **${loan_amount:,}**")
            
            # Default history
            default_options = ["Không", "Có"]
            default_text = st.selectbox("⚠️ Đã từng vỡ nợ trước đây?", default_options)
            default_on_file = default_options.index(default_text)
            st.write(f"Lịch sử vỡ nợ: **{default_text}**")
            
            # Credit history length
            credit_hist_length = st.slider(
                "📊 Số năm có lịch sử tín dụng", 
                min_value=0, max_value=25, value=10, step=1
            )
            st.write(f"Lịch sử tín dụng: **{credit_hist_length} năm**")
        
        # Predict button
        st.markdown("---")
        predict_button = st.button("� THỰC HIỆN DỰ ĐOÁN RỦI RO", type="primary", use_container_width=True)
    
    with main_col2:
        st.markdown("## 📊 KẾT QUẢ DỰ ĐOÁN")
        
        if predict_button:
            # Create input array - ĐÃ SỬA THỨ TỰ FEATURES ĐÚNG VỚI MODEL
            input_data = np.array([[
                person_age, person_income, home_ownership, emp_length,
                loan_intent, loan_amount, default_on_file, credit_hist_length
            ]])
            
            try:
                with st.spinner("🔄 Đang phân tích rủi ro..."):
                    prediction = loader.predict_lightgbm(input_data)[0]
                    # Raw prediction từ model này là approval probability
                    approval_probability = prediction  
                    default_probability = 1 - approval_probability  # Tỷ lệ vỡ nợ = 1 - tỷ lệ được duyệt
                
                st.markdown("---")
                st.markdown("### 📊 KẾT QUẢ PHÂN TÍCH")
                
                # Display result in columns
                result_col1, result_col2 = st.columns([1, 1])
                
                with result_col1:
                    # Risk level determination and decision
                    if default_probability > 0.7:
                        decision = "TỪ CHỐI"
                        risk_level = "RỦI RO CAO"
                        risk_color = "red"
                        risk_emoji = "❌"
                        decision_reason = "Dựa trên phân tích AI, hồ sơ này có tỷ lệ duyệt thấp do nhiều yếu tố tiêu cực vượt trội hơn các yếu tố tích cực."
                    elif default_probability > 0.4:
                        decision = "CẦN XEM XÉT"
                        risk_level = "RỦI RO TRUNG BÌNH"
                        risk_color = "orange"
                        risk_emoji = "⚠️"
                        decision_reason = "Hồ sơ có cả yếu tố tích cực và tiêu cực, cần đánh giá thêm thông tin trước khi quyết định cuối cùng."
                    else:
                        decision = "CHẤP THUẬN"
                        risk_level = "RỦI RO THẤP"
                        risk_color = "green"
                        risk_emoji = "✅"
                        decision_reason = "Dựa trên phân tích AI, hồ sơ này có nhiều yếu tố tích cực vượt trội, khả năng trả nợ cao."
                    
                    st.markdown(f"### 📊 PHÂN TÍCH QUYẾT ĐỊNH CHO HỒ SƠ VAY")
                    st.markdown(f"**Quyết định:** {risk_emoji} **{decision}**")
                    st.markdown(f"*{decision_reason}*")
                    st.markdown(f"**Tỷ lệ được duyệt cho vay:** {approval_probability:.1%}")
                    st.markdown(f"**Xác suất vỡ nợ:** {default_probability:.1%}")
                
                with result_col2:
                    # Approval probability gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = approval_probability * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Tỷ Lệ Được Duyệt Cho Vay (%)"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "green"},
                            'steps': [
                                {'range': [0, 30], 'color': "lightcoral"},
                                {'range': [30, 60], 'color': "yellow"},
                                {'range': [60, 100], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "darkgreen", 'width': 4},
                                'thickness': 0.75,
                                'value': 70
                            }
                        }
                    ))
                    
                    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Calculate SHAP values for later use
                shap_result = None
                features_impact = {}
                
                try:
                    # Calculate real SHAP values
                    if hasattr(loader, 'shap_explainer') and loader.shap_explainer:
                        shap_result = loader.calculate_shap_for_sample(input_data)
                        
                        # Get features_impact for later use
                        features_in_vietnamese = {
                            'person_age': 'Tuổi',
                            'person_income': 'Thu nhập', 
                            'person_home_ownership': 'Tình trạng sở hữu nhà',
                            'person_emp_length': 'Thời gian làm việc',
                            'loan_intent': 'Mục đích vay',
                            'loan_amnt': 'Số tiền vay',
                            'cb_person_default_on_file': 'Lịch sử nợ xấu',
                            'cb_person_cred_hist_length': 'Lịch sử tín dụng'
                        }
                        
                        for eng_name, viet_name in features_in_vietnamese.items():
                            features_impact[f"{viet_name} ({eng_name})"] = shap_result['shap_values'][eng_name]
                        
                    else:
                        # Fallback to simulated SHAP if real SHAP not available
                        st.warning("⚠️ SHAP TreeExplainer không có sẵn, sử dụng phân tích mô phỏng")
                        base_score = 0.3  # baseline
                        features_impact = {
                            'Thu nhập (person_income)': calculate_income_impact(person_income, loan_amount),
                            'Số tiền vay (loan_amnt)': calculate_loan_amount_impact(loan_amount, person_income),
                            'Tuổi (person_age)': calculate_age_impact(person_age),
                            'Lịch sử tín dụng (cb_person_cred_hist_length)': calculate_credit_history_impact(credit_hist_length),
                            'Tình trạng sở hữu nhà (person_home_ownership)': calculate_home_ownership_impact(home_ownership),
                            'Thời gian làm việc (person_emp_length)': calculate_employment_impact(emp_length),
                            'Mục đích vay (loan_intent)': calculate_loan_intent_impact(loan_intent),
                            'Lịch sử nợ xấu (cb_person_default_on_file)': calculate_default_impact(default_on_file)
                        }
                        
                except Exception as e:
                    st.error(f"❌ Lỗi tính toán SHAP: {e}")
                    # Fallback to simulated values
                    features_impact = {
                        'Thu nhập (person_income)': calculate_income_impact(person_income, loan_amount),
                        'Số tiền vay (loan_amnt)': calculate_loan_amount_impact(loan_amount, person_income),
                        'Tuổi (person_age)': calculate_age_impact(person_age),
                        'Lịch sử tín dụng (cb_person_cred_hist_length)': calculate_credit_history_impact(credit_hist_length),
                        'Tình trạng sở hữu nhà (person_home_ownership)': calculate_home_ownership_impact(home_ownership),
                        'Thời gian làm việc (person_emp_length)': calculate_employment_impact(emp_length),
                        'Mục đích vay (loan_intent)': calculate_loan_intent_impact(loan_intent),
                        'Lịch sử nợ xấu (cb_person_default_on_file)': calculate_default_impact(default_on_file)
                    }
                
                # Original SHAP Analysis section for detailed explanations
                st.markdown("---")
                st.markdown("### 🔍 PHÂN TÍCH CHI TIẾT CÁC YẾU TỐ (SHAP Analysis)")
                
                # Convert all impacts to percentage points (multiply by 100 for display)
                features_impact_percent = {name: impact * 100 for name, impact in features_impact.items()}
                
                # Separate positive and negative features, then sort by impact (descending)
                positive_features = [(name, impact_pct) for name, impact_pct in features_impact_percent.items() if impact_pct > 0]
                negative_features = [(name, impact_pct) for name, impact_pct in features_impact_percent.items() if impact_pct < 0]
                
                # Sort by impact: positive descending, negative by absolute value descending
                positive_features.sort(key=lambda x: x[1], reverse=True)
                negative_features.sort(key=lambda x: abs(x[1]), reverse=True)
                
                # Display positive factors
                if positive_features:
                    st.markdown("#### ✅ CÁC YẾU TỐ TÍCH CỰC (Hỗ trợ việc được duyệt)")
                    
                    for i, (feature_name, impact_pct) in enumerate(positive_features):
                        # impact_pct is already in percentage points
                        impact_score = f"+{impact_pct:.1f}%"
                        
                        if impact_pct >= 2.0:
                            impact_level = "RẤT MẠNH"
                            impact_color = "#1b5e20"
                            bg_color = "#c8e6c9"
                        elif impact_pct >= 1.0:
                            impact_level = "MẠNH"
                            impact_color = "#2e7d32"
                            bg_color = "#c8e6c9"
                        elif impact_pct >= 0.5:
                            impact_level = "TRUNG BÌNH"
                            impact_color = "#388e3c"
                            bg_color = "#dcedc8"
                        else:
                            impact_level = "NHẸ"
                            impact_color = "#4caf50"
                            bg_color = "#e8f5e8"
                        
                        st.markdown(f"""
                        <div style="
                            background-color: {bg_color};
                            border-left: 5px solid #4caf50;
                            padding: 15px;
                            border-radius: 8px;
                            margin: 10px 0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h5 style="margin: 0; color: {impact_color};">
                                    #{i+1} ✅ {feature_name.split('(')[0].strip()}
                                </h5>
                                <div style="text-align: right;">
                                    <span style="font-size: 16px; font-weight: bold; color: {impact_color}; display: block;">
                                        {impact_level}
                                    </span>
                                    <span style="font-size: 14px; color: #666; background-color: white; padding: 3px 8px; border-radius: 10px; margin-top: 5px; display: inline-block;">
                                        {impact_score}
                                    </span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add explanation in an expander
                        with st.expander(f"📖 Giải thích chi tiết"):
                            explanation = get_feature_explanation(feature_name, impact_pct / 100, 
                                                                person_age, person_income, home_ownership, 
                                                                emp_length, loan_intent, loan_amount, 
                                                                default_on_file, credit_hist_length)
                            st.write(explanation)
                
                # Display negative factors
                if negative_features:
                    st.markdown("#### ❌ CÁC YẾU TỐ TIÊU CỰC (Cản trở việc được duyệt)")
                    
                    for i, (feature_name, impact_pct) in enumerate(negative_features):
                        # impact_pct is already in percentage points (and negative)
                        abs_impact_pct = abs(impact_pct)
                        impact_score = f"-{abs_impact_pct:.1f}%"
                        
                        if abs_impact_pct >= 2.0:
                            impact_level = "RẤT NGHIÊM TRỌNG"
                            impact_color = "#b71c1c"
                            bg_color = "#ffcdd2"
                        elif abs_impact_pct >= 1.0:
                            impact_level = "NGHIÊM TRỌNG"
                            impact_color = "#c62828"
                            bg_color = "#ffcdd2"
                        elif abs_impact_pct >= 0.5:
                            impact_level = "ĐÁNG LƯU Ý"
                            impact_color = "#d32f2f"
                            bg_color = "#ffcdd2"
                        else:
                            impact_level = "NHẸ"
                            impact_color = "#f44336"
                            bg_color = "#ffeaea"
                        
                        st.markdown(f"""
                        <div style="
                            background-color: {bg_color};
                            border-left: 5px solid #f44336;
                            padding: 15px;
                            border-radius: 8px;
                            margin: 10px 0;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h5 style="margin: 0; color: {impact_color};">
                                    #{i+1} ❌ {feature_name.split('(')[0].strip()}
                                </h5>
                                <div style="text-align: right;">
                                    <span style="font-size: 16px; font-weight: bold; color: {impact_color}; display: block;">
                                        {impact_level}
                                    </span>
                                    <span style="font-size: 14px; color: #666; background-color: white; padding: 3px 8px; border-radius: 10px; margin-top: 5px; display: inline-block;">
                                        {impact_score}
                                    </span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Add explanation in an expander
                        with st.expander(f"📖 Giải thích chi tiết"):
                            explanation = get_feature_explanation(feature_name, impact_pct / 100, 
                                                                person_age, person_income, home_ownership, 
                                                                emp_length, loan_intent, loan_amount, 
                                                                default_on_file, credit_hist_length)
                            st.write(explanation)
                
                # Summary section
                st.markdown("#### 📈 Tổng Kết Phân Tích")
                
                total_positive = sum(impact for _, impact in positive_features)
                total_negative = sum(impact for _, impact in negative_features)
                net_impact = total_positive + total_negative
                
                # Convert to user-friendly format
                def get_overall_score(net_impact):
                    net_percent = net_impact * 100
                    if net_percent >= 3.0:
                        return "XUẤT SẮC", f"+{net_percent:.1f}%", "#1b5e20"
                    elif net_percent >= 1.0:
                        return "TỐT", f"+{net_percent:.1f}%", "#2e7d32"
                    elif net_percent >= 0:
                        return "KHUYẾN KHÍCH", f"+{net_percent:.1f}%", "#388e3c"
                    elif net_percent >= -1.0:
                        return "CẦN CẢI THIỆN", f"{net_percent:.1f}%", "#ff9800"
                    else:
                        return "CẦN ĐIỀU CHỈNH", f"{net_percent:.1f}%", "#f44336"
                
                overall_rating, overall_score, overall_color = get_overall_score(net_impact)
                
                summary_col1, summary_col2, summary_col3 = st.columns(3)
                
                with summary_col1:
                    positive_count = len(positive_features)
                    positive_strength = "MẠNH" if total_positive > 0.02 else "TRUNG BÌNH" if total_positive > 0.01 else "YẾU"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #e8f5e8;
                        border: 2px solid #4caf50;
                        padding: 15px;
                        border-radius: 8px;
                        text-align: center;
                    ">
                        <h4 style="color: #2e7d32; margin: 0;">✅ YẾU TỐ TÍCH CỰC</h4>
                        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #2e7d32;">
                            {positive_count} yếu tố
                        </p>
                        <p style="margin: 5px 0; color: #666; font-size: 16px; font-weight: bold;">
                            Mức độ: {positive_strength}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with summary_col2:
                    negative_count = len(negative_features)
                    negative_strength = "NGHIÊM TRỌNG" if abs(total_negative) > 0.02 else "ĐÁNG LƯU Ý" if abs(total_negative) > 0.01 else "NHẸ"
                    
                    st.markdown(f"""
                    <div style="
                        background-color: #ffeaea;
                        border: 2px solid #f44336;
                        padding: 15px;
                        border-radius: 8px;
                        text-align: center;
                    ">
                        <h4 style="color: #c62828; margin: 0;">❌ YẾU TỐ TIÊU CỰC</h4>
                        <p style="margin: 10px 0; font-size: 24px; font-weight: bold; color: #c62828;">
                            {negative_count} yếu tố
                        </p>
                        <p style="margin: 5px 0; color: #666; font-size: 16px; font-weight: bold;">
                            Mức độ: {negative_strength}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Advice section
                st.markdown("---")
                st.markdown("### 💡 LỜI KHUYÊN CẢI THIỆN HỒ SƠ")
                advice = generate_advice(person_income, loan_amount, person_age, emp_length, 
                                       credit_hist_length, home_ownership, default_on_file, default_probability)
                
                # Display advice with proper line breaks
                st.markdown(f"""
                <div style="
                    background-color: #e3f2fd;
                    border-left: 4px solid #2196f3;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 10px 0;
                ">
                    {advice.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"❌ Lỗi khi thực hiện dự đoán: {e}")
        else:
            st.info("👆 Nhấn nút 'THỰC HIỆN DỰ ĐOÁN RỦI RO' để xem kết quả")
    
    # Example buttons (outside of main columns)
    st.markdown("---")
    st.markdown("### 💡 Thử Các Ví Dụ Mẫu")
    
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        if st.button("👍 Hồ Sơ Tốt", use_container_width=True):
            st.rerun()
    
    with example_col2:
        if st.button("⚠️ Hồ Sơ Trung Bình", use_container_width=True):
            st.rerun()
    
    with example_col3:
        if st.button("❌ Hồ Sơ Rủi Ro", use_container_width=True):
            st.rerun()

def render_lora_analysis(loader):
    """Render LORA model analysis"""
    st.markdown("# 🧠 Phân Tích LORA Adapter Model")
    
    adapter_info = loader.get_adapter_summary()
    
    if "error" not in adapter_info:
        st.success("✅ LORA Adapter đã được tải thành công!")
        
        # Model overview
        st.markdown("## 📋 Thông Tin Tổng Quan")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Cấu Hình Mô Hình")
            st.info(f"**Mô Hình Gốc:** {adapter_info.get('Base Model', 'N/A')}")
            st.info(f"**Loại PEFT:** {adapter_info.get('PEFT Type', 'N/A')}")
            st.info(f"**Loại Tác Vụ:** {adapter_info.get('Task Type', 'N/A')}")
            st.info(f"**Chế Độ Inference:** {'✅ Bật' if adapter_info.get('Inference Mode') else '❌ Tắt'}")
        
        with col2:
            st.markdown("### Tham Số LoRA")
            st.metric("LoRA Rank (r)", adapter_info.get('LoRA Rank (r)', 0), help="Rank càng thấp càng tiết kiệm tài nguyên")
            st.metric("LoRA Alpha", adapter_info.get('LoRA Alpha', 0), help="Tỷ lệ scaling cho LoRA weights")
            st.metric("LoRA Dropout", f"{adapter_info.get('LoRA Dropout', 0):.3f}", help="Tỷ lệ dropout để tránh overfitting")
        
        # Target modules
        target_modules = adapter_info.get('Target Modules', [])
        if target_modules:
            st.markdown("## 🎯 Module Mục Tiêu")
            st.markdown("*Các layer được fine-tune bằng LoRA:*")
            cols = st.columns(min(len(target_modules), 4))
            for i, module in enumerate(target_modules):
                with cols[i % len(cols)]:
                    st.markdown(f"📦 **{module}**")
        
        # Advanced features
        st.markdown("## ⚙️ Tính Năng Nâng Cao")
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        
        with adv_col1:
            dora_status = "✅ Được bật" if adapter_info.get('Use DoRA') else "❌ Không sử dụng"
            st.markdown(f"**DoRA:** {dora_status}")
            if adapter_info.get('Use DoRA'):
                st.success("DoRA giúp cải thiện hiệu suất fine-tuning")
        
        with adv_col2:
            qlora_status = "✅ Được bật" if adapter_info.get('Use QLoRA') else "❌ Không sử dụng"
            st.markdown(f"**QLoRA:** {qlora_status}")
            if adapter_info.get('Use QLoRA'):
                st.success("QLoRA giúp tiết kiệm memory khi fine-tuning")
        
        with adv_col3:
            rslora_status = "✅ Được bật" if adapter_info.get('Use RSLoRA', False) else "❌ Không sử dụng"
            st.markdown(f"**RSLoRA:** {rslora_status}")
        
        # Technical details
        st.markdown("## 🔧 Chi Tiết Kỹ Thuật")
        with st.expander("Xem thông tin chi tiết"):
            st.json(adapter_info)
    else:
        st.error("❌ Không thể tải cấu hình LORA Adapter")

def render_lightgbm_analysis(loader):
    """Render LightGBM model analysis"""
    st.markdown("# 🌳 Phân Tích LightGBM Model")
    
    lgb_info = loader.get_lightgbm_summary()
    
    if "error" not in lgb_info:
        st.success("✅ LightGBM Model đã được tải thành công!")
        
        # Model metrics
        st.markdown("## 📊 Thông Số Mô Hình")
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric("Số Cây (Trees)", lgb_info.get('Number of Trees', 0), help="Số decision trees trong model")
        with metric_col2:
            st.metric("Số Đặc Trưng", lgb_info.get('Number of Features', 0), help="Số features đầu vào")
        with metric_col3:
            st.metric("Số Lớp", lgb_info.get('Number of Classes', 1), help="Binary classification = 1")
        with metric_col4:
            objective = lgb_info.get('Objective', 'Unknown')
            st.metric("Mục Tiêu", objective, help="Loại bài toán ML")
        
        # Feature information
        feature_names = lgb_info.get('Feature Names', [])
        if feature_names:
            st.markdown("## 🏷️ Danh Sách Đặc Trưng")
            st.markdown("*Các thông tin đầu vào mà model sử dụng để dự đoán:*")
            
            # Create feature dataframe with Vietnamese names
            feature_mapping = {
                'person_age': '🎂 Tuổi người vay',
                'person_income': '💰 Thu nhập hàng năm',
                'person_home_ownership': '🏠 Tình trạng nhà ở',
                'person_emp_length': '💼 Số năm làm việc',
                'loan_intent': '🎯 Mục đích vay',
                'loan_amnt': '💵 Số tiền vay',
                'cb_person_default_on_file': '⚠️ Lịch sử vỡ nợ',
                'cb_person_cred_hist_length': '📊 Thời gian có tín dụng'
            }
            
            feature_df = pd.DataFrame({
                'STT': range(1, len(feature_names) + 1),
                'Tên Đặc Trưng': feature_names,
                'Mô Tả': [feature_mapping.get(name, name) for name in feature_names]
            })
            
            st.dataframe(feature_df, use_container_width=True, hide_index=True)
        
        # Model purpose
        st.markdown("## 🎯 Mục Đích Của Model")
        st.info("""
        **Model LightGBM này được huấn luyện để:**
        - 🔍 Dự đoán khả năng vỡ nợ của người vay
        - ⚖️ Đánh giá rủi ro tín dụng
        - 💡 Hỗ trợ quyết định phê duyệt khoản vay
        - 📈 Phân tích các yếu tố ảnh hưởng đến khả năng trả nợ
        """)
        
        # Performance insights
        st.markdown("## 📈 Hiệu Suất Model")
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            st.markdown("### ✅ Ưu Điểm")
            st.write("• Tốc độ training và prediction nhanh")
            st.write("• Xử lý tốt dữ liệu có missing values")
            st.write("• Hiệu quả với bộ dữ liệu vừa và lớn")
            st.write("• Tự động feature selection")
        
        with perf_col2:
            st.markdown("### ⚠️ Lưu Ý")
            st.write("• Cần điều chỉnh hyperparameters cẩn thận")
            st.write("• Có thể overfitting với dữ liệu nhỏ")
            st.write("• Kết quả phụ thuộc vào chất lượng dữ liệu")
            st.write("• Cần update định kỳ với dữ liệu mới")
    else:
        st.error("❌ Không thể tải LightGBM model")

def render_feature_importance(loader):
    """Render feature importance analysis"""
    st.markdown("# 📊 Phân Tích Tầm Quan Trọng Đặc Trưng")
    
    try:
        importance_df = loader.get_feature_importance()
        
        if not importance_df.empty:
            st.success("✅ Dữ liệu feature importance đã được tải!")
            
            # Feature importance explanation
            st.markdown("## 🤔 Feature Importance Là Gì?")
            st.info("""
            **Feature Importance** cho biết mức độ quan trọng của từng đặc trưng trong việc đưa ra dự đoán:
            - **Gain**: Tổng improvement khi sử dụng feature này để split
            - **Split**: Số lần feature được sử dụng để split trong các decision trees
            """)
            
            # Create interactive charts
            fig = go.Figure()
            
            # Add gain importance
            fig.add_trace(go.Bar(
                name='Gain Importance',
                x=importance_df['importance_gain'],
                y=importance_df['feature'],
                orientation='h',
                marker_color='lightblue',
                text=importance_df['importance_gain'].round(0),
                textposition='outside'
            ))
            
            fig.update_layout(
                title='📈 Tầm Quan Trọng Đặc Trưng (Theo Gain)',
                xaxis_title='Importance Score',
                yaxis_title='Features',
                height=600,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Top features analysis
            st.markdown("## 🏆 Top Features Quan Trọng Nhất")
            top_features = importance_df.head(5)
            
            for idx, row in top_features.iterrows():
                feature_name = row['feature']
                gain_score = row['importance_gain']
                split_count = row['importance_split']
                
                # Feature name mapping
                feature_descriptions = {
                    'person_income': '💰 Thu nhập là yếu tố quyết định khả năng trả nợ',
                    'loan_amnt': '💵 Số tiền vay ảnh hưởng trực tiếp đến rủi ro',
                    'person_home_ownership': '🏠 Tình trạng nhà ở thể hiện tài sản đảm bảo',
                    'loan_intent': '🎯 Mục đích vay cho thấy mức độ cần thiết',
                    'cb_person_default_on_file': '⚠️ Lịch sử vỡ nợ là chỉ số rủi ro quan trọng',
                    'person_age': '🎂 Tuổi tác phản ánh kinh nghiệm và ổn định',
                    'person_emp_length': '💼 Thời gian làm việc thể hiện ổn định thu nhập',
                    'cb_person_cred_hist_length': '📊 Lịch sử tín dụng dài cho thấy kinh nghiệm'
                }
                
                with st.expander(f"#{idx+1}: {feature_name} (Score: {gain_score:.0f})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Gain Score", f"{gain_score:.0f}")
                        st.metric("Split Count", f"{split_count}")
                    with col2:
                        description = feature_descriptions.get(feature_name, "Đặc trưng quan trọng trong mô hình")
                        st.write(description)
            
            # Feature importance table
            st.markdown("## 📋 Bảng Đầy Đủ Feature Importance")
            
            # Add Vietnamese descriptions
            importance_df_display = importance_df.copy()
            feature_vietnamese = {
                'person_age': 'Tuổi người vay',
                'person_income': 'Thu nhập hàng năm',
                'person_home_ownership': 'Tình trạng nhà ở',
                'person_emp_length': 'Số năm làm việc',
                'loan_intent': 'Mục đích vay',
                'loan_amnt': 'Số tiền vay',
                'cb_person_default_on_file': 'Lịch sử vỡ nợ',
                'cb_person_cred_hist_length': 'Thời gian có tín dụng'
            }
            
            importance_df_display['Tên Tiếng Việt'] = importance_df_display['feature'].map(feature_vietnamese)
            importance_df_display = importance_df_display[['feature', 'Tên Tiếng Việt', 'importance_gain', 'importance_split']]
            importance_df_display.columns = ['Feature (EN)', 'Tên Tiếng Việt', 'Gain Score', 'Split Count']
            
            st.dataframe(importance_df_display, use_container_width=True, hide_index=True)
            
        else:
            st.warning("⚠️ Không có dữ liệu feature importance")
    except Exception as e:
        st.error(f"❌ Lỗi khi tạo biểu đồ feature importance: {e}")

if __name__ == "__main__":
    main()