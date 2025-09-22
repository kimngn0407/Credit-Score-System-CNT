# AI Model Visualization Dashboard

Ứng dụng Python để hiển thị trực quan và phân tích 2 models AI:
- **LORA Adapter Model**: Model fine-tuning sử dụng Low-Rank Adaptation
- **LightGBM Model**: Model gradient boosting cho binary classification

## 🚀 Cài đặt và Chạy

### Phương pháp 1: Sử dụng file bat (Windows)
```bash
# Double-click file run_app.bat hoặc chạy trong command prompt:
run_app.bat
```

### Phương pháp 2: Chạy thủ công
```bash
# Activate virtual environment
.venv\Scripts\activate

# Run Streamlit app
streamlit run app.py
```

## 📊 Tính năng

### 1. **Model Overview** 📋
- Tổng quan về cả 2 models
- Trạng thái load model
- Thông tin cơ bản

### 2. **LORA Adapter Analysis** 🧠
- Chi tiết cấu hình LORA
- Thông số LoRA (rank, alpha, dropout)
- Target modules và advanced features
- Base model information

### 3. **LightGBM Model Analysis** 🌳
- Thông tin model (số trees, features, classes)
- Danh sách features
- Model parameters

### 4. **Feature Importance** 📊
- Biểu đồ feature importance (by gain & split)
- Top features ranking
- Interactive visualizations

### 5. **Prediction Demo** 🎯
- Interface để test predictions
- Input parameters cho loan application
- Real-time prediction với probability
- Risk assessment gauge

## 🗂️ Cấu trúc Files

```
app_python/
├── adapter_config.json          # LORA adapter configuration
├── adapter_model.safetensors    # LORA model weights
├── lightgbm_model.txt          # LightGBM model file
├── model_loader.py             # Model loading utilities
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── run_app.bat                 # Windows batch script
└── README.md                   # This file
```

## 🛠️ Yêu cầu hệ thống

- Python 3.8+
- Windows (cho file .bat) hoặc Linux/Mac
- Ít nhất 4GB RAM
- Internet connection (cho việc load base models lần đầu)

## 📝 Ghi chú

- Ứng dụng sẽ chạy trên `http://localhost:8501`
- LightGBM model được sử dụng cho loan default prediction
- LORA adapter được cấu hình cho causal language modeling task
- Tất cả visualizations đều interactive với Plotly

## 🔧 Troubleshooting

Nếu gặp lỗi khi chạy:

1. **Lỗi import**: Kiểm tra virtual environment đã được activate
2. **Lỗi file not found**: Đảm bảo các file model (.json, .safetensors, .txt) ở đúng thư mục
3. **Lỗi memory**: Có thể cần tăng RAM hoặc close các ứng dụng khác

## 📞 Support

Nếu cần hỗ trợ, hãy kiểm tra:
- Console output để xem error messages
- Đảm bảo tất cả dependencies đã được cài đặt đúng
- File paths và permissions