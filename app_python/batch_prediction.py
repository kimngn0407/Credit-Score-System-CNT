"""
Batch Prediction Module
Xử lý dự đoán hàng loạt từ file CSV
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import io
from datetime import datetime
import time

def validate_csv_columns(df):
    """Kiểm tra và validate các cột cần thiết trong CSV"""
    required_columns = [
        'person_age', 'person_income', 'person_home_ownership', 
        'person_emp_length', 'loan_intent', 'loan_amnt', 
        'cb_person_default_on_file', 'cb_person_cred_hist_length'
    ]
    
    missing_columns = []
    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)
    
    return missing_columns

def create_sample_csv():
    """Tạo file CSV mẫu để download"""
    sample_data = {
        'person_age': [25, 35, 45, 30, 50],
        'person_income': [45000, 65000, 85000, 55000, 75000],
        'person_home_ownership': [0, 1, 1, 2, 1],  # 0: RENT, 1: OWN, 2: MORTGAGE
        'person_emp_length': [2, 8, 15, 5, 12],
        'loan_intent': [0, 1, 2, 3, 4],  # Different purposes
        'loan_amnt': [10000, 15000, 25000, 12000, 20000],
        'cb_person_default_on_file': [0, 0, 0, 1, 0],  # 0: No, 1: Yes
        'cb_person_cred_hist_length': [3, 10, 18, 7, 15]
    }
    
    df = pd.DataFrame(sample_data)
    return df

def process_batch_predictions(df, loader):
    """Xử lý dự đoán hàng loạt"""
    results = []
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_rows = len(df)
    
    for idx, row in df.iterrows():
        # Update progress
        progress = (idx + 1) / total_rows
        progress_bar.progress(progress)
        status_text.text(f'Đang xử lý hồ sơ {idx + 1}/{total_rows}...')
        
        # Create input array
        input_data = np.array([[
            row['person_age'], row['person_income'], row['person_home_ownership'],
            row['person_emp_length'], row['loan_intent'], row['loan_amnt'],
            row['cb_person_default_on_file'], row['cb_person_cred_hist_length']
        ]])
        
        try:
            # Get prediction
            prediction = loader.predict_lightgbm(input_data)[0]
            approval_probability = prediction
            default_probability = 1 - approval_probability
            
            # Determine decision
            if default_probability > 0.7:
                decision = "TỪ CHỐI"
                risk_level = "RỦI RO CAO"
            elif default_probability > 0.4:
                decision = "CÂN NHẮC"
                risk_level = "RỦI RO TRUNG BÌNH"
            else:
                decision = "CHẤP THUẬN"
                risk_level = "RỦI RO THẤP"
            
            # Calculate SHAP if available
            shap_summary = "N/A"
            if hasattr(loader, 'shap_explainer') and loader.shap_explainer:
                try:
                    shap_result = loader.calculate_shap_for_sample(input_data[0])
                    # Get top positive and negative factors
                    features_in_vietnamese = {
                        'person_age': 'Tuổi',
                        'person_income': 'Thu nhập',
                        'person_home_ownership': 'Tình trạng nhà',
                        'person_emp_length': 'Thời gian làm việc',
                        'loan_intent': 'Mục đích vay',
                        'loan_amnt': 'Số tiền vay',
                        'cb_person_default_on_file': 'Lịch sử nợ xấu',
                        'cb_person_cred_hist_length': 'Lịch sử tín dụng'
                    }
                    
                    # Find most important factors
                    shap_values = shap_result['shap_values']
                    sorted_features = sorted(shap_values.items(), key=lambda x: abs(x[1]), reverse=True)
                    top_factor = sorted_features[0] if sorted_features else None
                    
                    if top_factor:
                        feature_viet = features_in_vietnamese.get(top_factor[0], top_factor[0])
                        impact = "+" if top_factor[1] > 0 else "-"
                        shap_summary = f"{feature_viet} ({impact})"
                    
                except Exception:
                    shap_summary = "Error"
            
            result = {
                'STT': idx + 1,
                'Tuổi': row['person_age'],
                'Thu nhập': f"${row['person_income']:,}",
                'Số tiền vay': f"${row['loan_amnt']:,}",
                'Tỷ lệ duyệt': f"{approval_probability:.1%}",
                'Xác suất vỡ nợ': f"{default_probability:.1%}",
                'Quyết định': decision,
                'Mức rủi ro': risk_level,
                'Yếu tố chính': shap_summary
            }
            
            results.append(result)
            
        except Exception as e:
            # Handle error cases
            result = {
                'STT': idx + 1,
                'Tuổi': row['person_age'],
                'Thu nhập': f"${row['person_income']:,}",
                'Số tiền vay': f"${row['loan_amnt']:,}",
                'Tỷ lệ duyệt': "Error",
                'Xác suất vỡ nợ': "Error",
                'Quyết định': "LỖI",
                'Mức rủi ro': "LỖI",
                'Yếu tố chính': str(e)[:50]
            }
            results.append(result)
        
        # Small delay to show progress
        time.sleep(0.1)
    
    # Complete progress
    progress_bar.progress(1.0)
    status_text.text('✅ Hoàn thành!')
    
    return pd.DataFrame(results)

def create_batch_visualizations(results_df):
    """Tạo các biểu đồ cho kết quả batch prediction"""
    
    # 1. Decision Distribution Pie Chart
    st.markdown("#### 📊 Phân Bổ Quyết Định")
    decision_counts = results_df['Quyết định'].value_counts()
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=decision_counts.index,
        values=decision_counts.values,
        hole=0.4,
        marker_colors=['#4CAF50', '#FF9800', '#F44336', '#9E9E9E']
    )])
    
    fig_pie.update_layout(
        title="Tỷ Lệ Các Quyết Định Cho Vay",
        height=400
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # 2. Risk Level Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Phân Bổ Mức Rủi Ro")
        risk_counts = results_df['Mức rủi ro'].value_counts()
        
        fig_risk = go.Figure(data=[go.Bar(
            x=risk_counts.index,
            y=risk_counts.values,
            marker_color=['#4CAF50', '#FF9800', '#F44336', '#9E9E9E']
        )])
        
        fig_risk.update_layout(
            title="Số Lượng Theo Mức Rủi Ro",
            xaxis_title="Mức Rủi Ro",
            yaxis_title="Số Lượng",
            height=400
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        # 3. Approval Rate by Age Group
        st.markdown("#### 👥 Tỷ Lệ Duyệt Theo Độ Tuổi")
        
        # Convert approval rate back to numeric for analysis
        numeric_results = results_df.copy()
        numeric_results['Approval_Rate'] = numeric_results['Tỷ lệ duyệt'].str.replace('%', '').str.replace('Error', '0').astype(float) / 100
        numeric_results['Age_Group'] = pd.cut(numeric_results['Tuổi'], 
                                            bins=[0, 25, 35, 50, 100], 
                                            labels=['18-25', '26-35', '36-50', '50+'])
        
        age_approval = numeric_results.groupby('Age_Group')['Approval_Rate'].mean()
        
        fig_age = go.Figure(data=[go.Bar(
            x=age_approval.index.astype(str),
            y=age_approval.values * 100,
            marker_color='#2196F3'
        )])
        
        fig_age.update_layout(
            title="Tỷ Lệ Duyệt Trung Bình (%)",
            xaxis_title="Nhóm Tuổi",
            yaxis_title="Tỷ Lệ Duyệt (%)",
            height=400
        )
        
        st.plotly_chart(fig_age, use_container_width=True)

def create_excel_report(results_df, original_df):
    """Tạo file Excel báo cáo chi tiết"""
    output = io.BytesIO()
    
    # Create Excel writer
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Results sheet
        results_df.to_excel(writer, sheet_name='Kết Quả Dự Đoán', index=False)
        
        # Original data sheet
        original_df.to_excel(writer, sheet_name='Dữ Liệu Gốc', index=False)
        
        # Summary sheet
        summary_data = {
            'Thống Kê': [
                'Tổng số hồ sơ',
                'Số hồ sơ được chấp thuận',
                'Số hồ sơ bị từ chối', 
                'Số hồ sơ cần cân nhắc',
                'Tỷ lệ chấp thuận trung bình',
                'Tỷ lệ rủi ro cao'
            ],
            'Giá Trị': [
                len(results_df),
                len(results_df[results_df['Quyết định'] == 'CHẤP THUẬN']),
                len(results_df[results_df['Quyết định'] == 'TỪ CHỐI']),
                len(results_df[results_df['Quyết định'] == 'CÂN NHẮC']),
                f"{(len(results_df[results_df['Quyết định'] == 'CHẤP THUẬN']) / len(results_df) * 100):.1f}%",
                f"{(len(results_df[results_df['Mức rủi ro'] == 'RỦI RO CAO']) / len(results_df) * 100):.1f}%"
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Tổng Kết', index=False)
    
    output.seek(0)
    return output

def render_batch_prediction_page(loader):
    """Render trang dự đoán hàng loạt"""
    st.markdown("# 📊 Dự Đoán Hàng Loạt Từ File CSV")
    st.markdown("### Upload file CSV để dự đoán rủi ro cho nhiều hồ sơ cùng lúc")
    
    if loader.lightgbm_model is None:
        st.error("❌ Không thể tải mô hình LightGBM")
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📁 Upload CSV", "📋 Hướng Dẫn", "📥 File Mẫu"])
    
    with tab3:
        st.markdown("### 📥 Tải File CSV Mẫu")
        st.markdown("Sử dụng file mẫu này để hiểu định dạng dữ liệu cần thiết:")
        
        sample_df = create_sample_csv()
        st.dataframe(sample_df, use_container_width=True)
        
        # Create download button for sample
        csv_sample = sample_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Tải File Mẫu (CSV)",
            data=csv_sample,
            file_name=f"loan_sample_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
        st.markdown("#### 📝 Giải Thích Các Cột:")
        st.markdown("""
        - **person_age**: Tuổi (18-80)
        - **person_income**: Thu nhập hàng năm (USD)
        - **person_home_ownership**: Tình trạng nhà (0=Thuê, 1=Sở hữu, 2=Thế chấp)
        - **person_emp_length**: Số năm làm việc (0-20)
        - **loan_intent**: Mục đích vay (0=Cá nhân, 1=Giáo dục, 2=Y tế, 3=Kinh doanh, 4=Cải thiện nhà, 5=Trả nợ)
        - **loan_amnt**: Số tiền vay (USD)
        - **cb_person_default_on_file**: Lịch sử vỡ nợ (0=Không, 1=Có)
        - **cb_person_cred_hist_length**: Số năm có lịch sử tín dụng
        """)
    
    with tab2:
        st.markdown("### 📋 Hướng Dẫn Sử Dụng")
        st.markdown("""
        #### 🔢 Bước 1: Chuẩn Bị File CSV
        - File CSV phải có đúng 8 cột theo thứ tự trên
        - Không được có dòng header tiếng Việt (sử dụng tên cột tiếng Anh)
        - Dữ liệu phải ở định dạng số
        
        #### 📤 Bước 2: Upload File
        - Click vào vùng upload hoặc kéo thả file
        - Hệ thống sẽ tự động kiểm tra định dạng
        
        #### ⚡ Bước 3: Xử Lý Tự Động
        - Hệ thống sẽ dự đoán từng hồ sơ
        - Hiển thị thanh tiến trình
        
        #### 📊 Bước 4: Xem Kết Quả
        - Bảng kết quả chi tiết
        - Biểu đồ phân tích
        - Tải báo cáo Excel
        """)
    
    with tab1:
        st.markdown("### 📁 Upload File CSV")
        
        uploaded_file = st.file_uploader(
            "Chọn file CSV chứa dữ liệu hồ sơ vay:",
            type=['csv'],
            help="File CSV phải chứa đúng 8 cột theo định dạng mẫu"
        )
        
        if uploaded_file is not None:
            try:
                # Read CSV
                df = pd.read_csv(uploaded_file)
                
                st.success(f"✅ Đã tải file thành công! Tìm thấy {len(df)} hồ sơ.")
                
                # Validate columns
                missing_cols = validate_csv_columns(df)
                
                if missing_cols:
                    st.error(f"❌ File CSV thiếu các cột sau: {', '.join(missing_cols)}")
                    st.info("💡 Vui lòng tải file mẫu và điều chỉnh dữ liệu theo đúng định dạng.")
                    return
                
                # Show preview
                st.markdown("#### 👀 Xem Trước Dữ Liệu")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Process predictions button
                if st.button("🚀 BẮT ĐẦU DỰ ĐOÁN HÀNG LOẠT", type="primary", use_container_width=True):
                    st.markdown("---")
                    st.markdown("### ⚡ Đang Xử Lý Dự Đoán...")
                    
                    # Process predictions
                    results_df = process_batch_predictions(df, loader)
                    
                    # Show results
                    st.markdown("---")
                    st.markdown("### 🎯 Kết Quả Dự Đoán Hàng Loạt")
                    
                    # Summary metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    total_count = len(results_df)
                    approved_count = len(results_df[results_df['Quyết định'] == 'CHẤP THUẬN'])
                    rejected_count = len(results_df[results_df['Quyết định'] == 'TỪ CHỐI'])
                    review_count = len(results_df[results_df['Quyết định'] == 'CÂN NHẮC'])
                    
                    with col1:
                        st.metric("📊 Tổng Hồ Sơ", total_count)
                    
                    with col2:
                        st.metric("✅ Chấp Thuận", approved_count, f"{approved_count/total_count*100:.1f}%")
                    
                    with col3:
                        st.metric("❌ Từ Chối", rejected_count, f"{rejected_count/total_count*100:.1f}%")
                    
                    with col4:
                        st.metric("⚠️ Cân Nhắc", review_count, f"{review_count/total_count*100:.1f}%")
                    
                    # Detailed results table
                    st.markdown("#### 📋 Bảng Kết Quả Chi Tiết")
                    st.dataframe(results_df, use_container_width=True, height=400)
                    
                    # Visualizations
                    st.markdown("---")
                    st.markdown("### 📈 Phân Tích Kết Quả")
                    create_batch_visualizations(results_df)
                    
                    # Download options
                    st.markdown("---")
                    st.markdown("### 💾 Tải Kết Quả")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # CSV download
                        csv_results = results_df.to_csv(index=False)
                        st.download_button(
                            label="📄 Tải Kết Quả (CSV)",
                            data=csv_results,
                            file_name=f"loan_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                    
                    with col2:
                        # Excel download
                        excel_file = create_excel_report(results_df, df)
                        st.download_button(
                            label="📊 Tải Báo Cáo (Excel)",
                            data=excel_file,
                            file_name=f"loan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                    
                    st.success("🎉 Hoàn thành! Bạn có thể tải kết quả ở các nút phía trên.")
                
            except Exception as e:
                st.error(f"❌ Lỗi khi đọc file: {str(e)}")
                st.info("💡 Vui lòng kiểm tra lại định dạng file CSV và thử lại.")