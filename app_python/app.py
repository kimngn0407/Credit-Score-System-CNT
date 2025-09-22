"""
Streamlit App for Model Visualization
Ứng dụng hiển thị trực quan cho LORA Adapter và LightGBM models
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from model_loader import load_models
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Bảng Điều Khiển Trực Quan AI Models",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.model-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 10px;
    margin: 1rem 0;
}
.metric-card {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_models_cached():
    """Cache loaded models to improve performance"""
    return load_models(".")

def render_adapter_info(loader):
    """Render LORA Adapter information"""
    st.markdown("### 🧠 Mô Hình LORA Adapter")
    
    adapter_info = loader.get_adapter_summary()
    
    if "error" not in adapter_info:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Cấu Hình Mô Hình")
            st.markdown(f"**Mô Hình Gốc:** {adapter_info.get('Base Model', 'N/A')}")
            st.markdown(f"**Loại PEFT:** {adapter_info.get('PEFT Type', 'N/A')}")
            st.markdown(f"**Loại Tác Vụ:** {adapter_info.get('Task Type', 'N/A')}")
            st.markdown(f"**Chế Độ Inference:** {'✅' if adapter_info.get('Inference Mode') else '❌'}")
        
        with col2:
            st.markdown("#### Tham Số LoRA")
            st.metric("Rank LoRA (r)", adapter_info.get('LoRA Rank (r)', 0))
            st.metric("Alpha LoRA", adapter_info.get('LoRA Alpha', 0))
            st.metric("Dropout LoRA", f"{adapter_info.get('LoRA Dropout', 0):.3f}")
        
        # Target Modules
        target_modules = adapter_info.get('Target Modules', [])
        if target_modules:
            st.markdown("#### Module Mục Tiêu")
            cols = st.columns(len(target_modules))
            for i, module in enumerate(target_modules):
                with cols[i % len(cols)]:
                    st.markdown(f"📦 `{module}`")
        
        # Advanced Features
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("DoRA", "✅" if adapter_info.get('Use DoRA') else "❌")
        with col2:
            st.metric("QLoRA", "✅" if adapter_info.get('Use QLoRA') else "❌")
        with col3:
            st.metric("RSLoRA", "✅" if adapter_info.get('Use RSLoRA', False) else "❌")
    else:
        st.error("Không thể tải cấu hình LORA Adapter")

def render_lightgbm_info(loader):
    """Render LightGBM model information"""
    st.markdown("### 🌳 Mô Hình LightGBM")
    
    lgb_info = loader.get_lightgbm_summary()
    
    if "error" not in lgb_info:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Số Cây", lgb_info.get('Number of Trees', 0))
        with col2:
            st.metric("Số Đặc Trưng", lgb_info.get('Number of Features', 0))
        with col3:
            st.metric("Số Lớp", lgb_info.get('Number of Classes', 1))
        with col4:
            st.metric("Mục Tiêu", lgb_info.get('Objective', 'Unknown'))
        
        # Feature Names
        feature_names = lgb_info.get('Feature Names', [])
        if feature_names:
            st.markdown("#### Các Đặc Trưng Của Mô Hình")
            feature_df = pd.DataFrame({
                'Đặc Trưng': feature_names,
                'Chỉ Số': range(len(feature_names))
            })
            st.dataframe(feature_df, use_container_width=True)
    else:
        st.error("Không thể tải mô hình LightGBM")

def render_feature_importance(loader):
    """Render feature importance visualization"""
    st.markdown("### 📊 Phân Tích Tầm Quan Trọng Đặc Trưng")
    
    try:
        importance_df = loader.get_feature_importance()
        
        if not importance_df.empty:
            # Create feature importance chart
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=('Tầm Quan Trọng Theo Gain', 'Tầm Quan Trọng Theo Split'),
                specs=[[{"secondary_y": False}, {"secondary_y": False}]]
            )
            
            # Gain importance
            fig.add_trace(
                go.Bar(
                    x=importance_df['importance_gain'],
                    y=importance_df['feature'],
                    orientation='h',
                    name='Gain',
                    marker_color='lightblue'
                ),
                row=1, col=1
            )
            
            # Split importance
            fig.add_trace(
                go.Bar(
                    x=importance_df['importance_split'],
                    y=importance_df['feature'],
                    orientation='h',
                    name='Split',
                    marker_color='lightcoral'
                ),
                row=1, col=2
            )
            
            fig.update_layout(
                height=600,
                title_text="So Sánh Tầm Quan Trọng Đặc Trưng",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display top features
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Top Đặc Trưng Theo Gain")
                st.dataframe(
                    importance_df[['feature', 'importance_gain']].head(10),
                    use_container_width=True
                )
            
            with col2:
                st.markdown("#### Top Đặc Trưng Theo Split")
                st.dataframe(
                    importance_df[['feature', 'importance_split']].head(10),
                    use_container_width=True
                )
        else:
            st.warning("Không có dữ liệu tầm quan trọng đặc trưng")
    except Exception as e:
        st.error(f"Lỗi khi tạo biểu đồ tầm quan trọng: {e}")

def render_prediction_demo(loader):
    """Render prediction demo interface"""
    st.markdown("### 🎯 Demo Dự Đoán Rủi Ro Vay Vốn")
    st.markdown("**Điền thông tin dưới đây để dự đoán khả năng vỡ nợ khoản vay**")
    st.markdown("---")
    
    if loader.lightgbm_model is None:
        st.error("Mô hình LightGBM chưa được tải")
        return
    
    # Input section without form first to make sure it shows
    st.markdown("#### 📝 Nhập Thông Tin Người Vay")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Thông Tin Cá Nhân")
        person_age = st.slider("🎂 Tuổi", 18, 80, 35, help="Tuổi của người vay")
        person_income = st.number_input(
            "💰 Thu Nhập Hàng Năm (USD)", 
            min_value=10000, max_value=500000, value=75000, step=1000,
            help="Thu nhập hàng năm của người vay"
        )
        
        home_ownership = st.selectbox(
            "🏠 Tình Trạng Nhà Ở",
            options=[0, 1, 2],
            format_func=lambda x: {0: "Thuê nhà", 1: "Sở hữu", 2: "Thế chấp"}[x],
            help="Tình trạng sở hữu nhà của người vay"
        )
        
        emp_length = st.slider(
            "💼 Thời Gian Làm Việc (năm)", 
            0, 20, 5,
            help="Số năm kinh nghiệm làm việc"
        )
    
    with col2:
        st.markdown("##### Thông Tin Khoản Vay")
        loan_intent = st.selectbox(
            "🎯 Mục Đích Vay",
            options=[0, 1, 2, 3, 4, 5],
            format_func=lambda x: {
                0: "Cá nhân", 1: "Giáo dục", 2: "Y tế",
                3: "Kinh doanh", 4: "Cải thiện nhà", 5: "Trả nợ"
            }[x],
            help="Mục đích sử dụng khoản vay"
        )
        
        loan_amount = st.number_input(
            "💵 Số Tiền Vay (USD)", 
            min_value=1000, max_value=50000, value=10000, step=500,
            help="Số tiền muốn vay"
        )
        
        default_on_file = st.selectbox(
            "⚠️ Lịch Sử Vỡ Nợ",
            options=[0, 1],
            format_func=lambda x: {0: "Không", 1: "Có"}[x],
            help="Đã từng vỡ nợ trước đây hay chưa"
        )
        
        credit_hist_length = st.slider(
            "📊 Thời Gian Có Tín Dụng (năm)", 
            0, 25, 10,
            help="Số năm có lịch sử tín dụng"
        )
    
    # Big predict button
    st.markdown("---")
    st.markdown("#### 🔮 Thực Hiện Dự Đoán")
    
    predict_button = st.button("� DỰ ĐOÁN RỦI RO NGAY", type="primary", use_container_width=True)
    
    submitted = predict_button
    
    # Results section
    if submitted:
        st.markdown("---")
        st.markdown("#### 📊 Kết Quả Dự Đoán")
        
        # Create input array
        input_data = np.array([[
            person_age, person_income, home_ownership, emp_length,
            loan_intent, loan_amount, default_on_file, credit_hist_length
        ]])
        
        try:
            with st.spinner("Đang phân tích..."):
                prediction = loader.predict_lightgbm(input_data)[0]
                # Model đã trả về probability trực tiếp, không cần sigmoid
                probability = prediction
                
                # Display result in columns
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    # Risk level determination
                    if probability > 0.7:
                        risk_level = "RỦI RO CAO"
                        risk_color = "red"
                        risk_emoji = "🔴"
                    elif probability > 0.4:
                        risk_level = "RỦI RO TRUNG BÌNH"
                        risk_color = "orange"
                        risk_emoji = "🟡"
                    else:
                        risk_level = "RỦI RO THẤP"
                        risk_color = "green"
                        risk_emoji = "🟢"
                    
                    st.markdown(f"**Xác Suất Vỡ Nợ:** {probability:.1%}")
                    st.markdown(f"**Mức Độ Rủi Ro:** {risk_emoji} <span style='color: {risk_color}; font-weight: bold; font-size: 1.2em;'>{risk_level}</span>", unsafe_allow_html=True)
                    
                    # Recommendation
                    if probability > 0.6:
                        st.error("❌ **Khuyến nghị:** KHÔNG nên phê duyệt khoản vay")
                    elif probability > 0.3:
                        st.warning("⚠️ **Khuyến nghị:** Cần xem xét kỹ thêm")
                    else:
                        st.success("✅ **Khuyến nghị:** Có thể phê duyệt khoản vay")
                
                with col2:
                    # Probability gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = probability * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Xác Suất Vỡ Nợ (%)"},
                        delta = {'reference': 50},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 30], 'color': "lightgreen"},
                                {'range': [30, 60], 'color': "yellow"},
                                {'range': [60, 100], 'color': "lightcoral"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 50
                            }
                        }
                    ))
                    
                    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Detailed analysis
                st.markdown("#### 📈 Phân Tích Chi Tiết")
                analysis_col1, analysis_col2 = st.columns(2)
                
                with analysis_col1:
                    st.markdown("**Thông Tin Đầu Vào:**")
                    st.write(f"• Tuổi: {person_age}")
                    st.write(f"• Thu nhập: ${person_income:,}")
                    st.write(f"• Số tiền vay: ${loan_amount:,}")
                    st.write(f"• Tỷ lệ vay/thu nhập: {(loan_amount/person_income)*100:.1f}%")
                
                with analysis_col2:
                    st.markdown("**Yếu Tố Rủi Ro:**")
                    if loan_amount/person_income > 0.3:
                        st.write("⚠️ Tỷ lệ vay/thu nhập cao")
                    if default_on_file == 1:
                        st.write("🔴 Có lịch sử vỡ nợ")
                    if person_age < 25:
                        st.write("⚠️ Tuổi còn trẻ (ít kinh nghiệm)")
                    if emp_length < 2:
                        st.write("⚠️ Thời gian làm việc ngắn")
                    if credit_hist_length < 3:
                        st.write("⚠️ Lịch sử tín dụng ngắn")
                
        except Exception as e:
            st.error(f"Lỗi khi thực hiện dự đoán: {e}")
    
    # Add some example cases
    st.markdown("---")
    st.markdown("#### 💡 Thử Các Ví Dụ Mẫu")
    st.markdown("*Nhấn vào một trong các nút dưới để tự động điền thông tin mẫu*")
    
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        if st.button("👍 Hồ Sơ Tốt - RỦI RO THẤP", use_container_width=True, type="secondary"):
            st.success("Đã điền thông tin hồ sơ tốt! Kéo lên trên để xem và nhấn nút Dự Đoán.")
    
    with example_col2:
        if st.button("⚠️ Hồ Sơ Trung Bình", use_container_width=True, type="secondary"):
            st.warning("Đã điền thông tin hồ sơ trung bình! Kéo lên trên để xem và nhấn nút Dự Đoán.")
    
    with example_col3:
        if st.button("❌ Hồ Sơ Rủi Ro - RỦI RO CAO", use_container_width=True, type="secondary"):
            st.error("Đã điền thông tin hồ sơ rủi ro cao! Kéo lên trên để xem và nhấn nút Dự Đoán.")
    
    # Instructions
    st.markdown("---")
    st.markdown("### 📋 Hướng Dẫn Sử Dụng")
    st.markdown("""
    1. **Điều chỉnh các thanh trượt và dropdown** ở phía trên
    2. **Nhập số liệu** vào các ô số (thu nhập, số tiền vay)
    3. **Nhấn nút "🚀 DỰ ĐOÁN RỦI RO NGAY"** để xem kết quả
    4. **Hoặc thử các ví dụ mẫu** bằng cách nhấn các nút ở trên
    """)
    
    if not submitted:
        st.info("👆 Hãy điều chỉnh các thông tin ở trên và nhấn nút Dự Đoán để xem kết quả!")

def main():
    """Main application function"""
    st.markdown("<h1 class='main-header'>🤖 Bảng Điều Khiển Trực Quan AI Models</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Load models
    with st.spinner("Đang tải models..."):
        loader = load_models_cached()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Điều Hướng")
    page = st.sidebar.selectbox(
        "Chọn một mục:",
        ["📋 Tổng Quan", "🧠 LORA Adapter", "🌳 Mô Hình LightGBM", "📊 Phân Tích Đặc Trưng", "🎯 Demo Dự Đoán"]
    )
    
    if page == "📋 Tổng Quan":
        st.markdown("## 📋 Tổng Quan Về Models")
        st.markdown("""
        Bảng điều khiển này cung cấp các trực quan hóa và phân tích toàn diện cho hai mô hình AI:
        
        1. **🧠 LORA Adapter Model**: Mô hình Parameter-Efficient Fine-Tuning (PEFT) dựa trên Low-Rank Adaptation
        2. **🌳 LightGBM Model**: Framework gradient boosting được tối ưu hóa cho phân loại nhị phân
        
        Sử dụng thanh điều hướng bên trái để khám phá các khía cạnh khác nhau của những mô hình này.
        """)
        
        # Quick stats
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧠 LORA Adapter")
            adapter_info = loader.get_adapter_summary()
            if "error" not in adapter_info:
                st.success("✅ Mô hình đã tải thành công")
                st.info(f"Mô Hình Gốc: {adapter_info.get('Base Model', 'N/A')}")
                st.info(f"Loại Tác Vụ: {adapter_info.get('Task Type', 'N/A')}")
            else:
                st.error("❌ Không thể tải mô hình")
        
        with col2:
            st.markdown("### 🌳 LightGBM Model")
            lgb_info = loader.get_lightgbm_summary()
            if "error" not in lgb_info:
                st.success("✅ Mô hình đã tải thành công")
                st.info(f"Số Cây: {lgb_info.get('Number of Trees', 0)}")
                st.info(f"Số Đặc Trưng: {lgb_info.get('Number of Features', 0)}")
            else:
                st.error("❌ Không thể tải mô hình")
    
    elif page == "🧠 LORA Adapter":
        render_adapter_info(loader)
    
    elif page == "🌳 Mô Hình LightGBM":
        render_lightgbm_info(loader)
    
    elif page == "📊 Phân Tích Đặc Trưng":
        render_feature_importance(loader)
    
    elif page == "🎯 Demo Dự Đoán":
        render_prediction_demo(loader)
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Mẹo**: Sử dụng thanh bên để điều hướng giữa các công cụ trực quan hóa và phân tích mô hình khác nhau.")

if __name__ == "__main__":
    main()