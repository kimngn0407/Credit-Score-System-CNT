# Loan System với AI Model Integration

Hệ thống cho vay tích hợp với AI model để dự đoán và đánh giá rủi ro tín dụng.

## Cấu trúc dự án

- `LoanSystem/` - Spring Boot application (Java)
- `loan-forecast-api/` - FastAPI service chứa AI model (Python)

## Cách chạy

### Sử dụng Docker Compose (Khuyến nghị)

```bash
# Chạy tất cả services
docker-compose up --build

# Chạy ở background
docker-compose up -d --build
```

### Chạy thủ công

#### 1. Chạy PostgreSQL
```bash
docker run -d --name postgres \
  -e POSTGRES_DB=LoanSystem \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=Ngan0407@! \
  -p 5432:5432 postgres:15
```

#### 2. Chạy Loan Forecast API
```bash
cd loan-forecast-api
pip install -r requirements.txt
python run_server.py
```

#### 3. Chạy Loan System
```bash
cd LoanSystem
./mvnw spring-boot:run
```

## API Endpoints

### Loan System (Spring Boot) - Port 8080

#### Inference
- `POST /api/inference/predict/{appId}` - Dự đoán loan cho application

#### Loan Forecast API Integration
- `POST /api/loan-forecast/predict` - Gọi trực tiếp model predict
- `POST /api/loan-forecast/explain` - Giải thích kết quả dự đoán
- `POST /api/loan-forecast/optimize` - Tối ưu hóa application
- `GET /api/loan-forecast/health` - Health check

### Loan Forecast API (FastAPI) - Port 8000

- `POST /predict` - Dự đoán loan
- `POST /explain` - Giải thích kết quả
- `POST /optimize` - Tối ưu hóa
- `GET /health` - Health check

## Cấu hình

### Loan System (application.properties)
```properties
# Loan Forecast API Configuration
loan.forecast.api.url=http://localhost:8000
loan.forecast.api.token=
```

### Loan Forecast API
- Model path: `mlp_loan_model.keras`
- API Token: Có thể cấu hình qua environment variable `API_TOKEN`

## Sử dụng

### 1. Tạo Application
```bash
curl -X POST http://localhost:8080/api/applications \
  -H "Content-Type: application/json" \
  -d '{
    "personAge": 25,
    "personIncome": 50000,
    "loanAmnt": 10000,
    "personHomeOwnership": "RENT",
    "cbPersonDefaultOnFile": "N",
    "loanIntent": "PERSONAL",
    "personEmpLength": 2.5,
    "cbPersonCredHistLength": 3
  }'
```

### 2. Dự đoán Loan
```bash
curl -X POST http://localhost:8080/api/inference/predict/1
```

### 3. Gọi trực tiếp Loan Forecast API
```bash
curl -X POST http://localhost:8080/api/loan-forecast/predict \
  -H "Content-Type: application/json" \
  -d '{
    "features": [10000.0, 50000.0, 25.0, 3.0, 2.5, 0.0, 0.0, 1.0]
  }'
```

## Features

- ✅ Tích hợp AI model qua API
- ✅ Dự đoán loan approval/rejection
- ✅ Giải thích kết quả dự đoán
- ✅ Tối ưu hóa application
- ✅ Health check cho cả hai services
- ✅ Docker containerization
- ✅ Database persistence

## Lưu ý

- Cần customize `extractFeatures()` method trong `InferenceService` để phù hợp với cấu trúc dữ liệu thực tế
- Model cần được train với đúng format features
- Có thể cấu hình API token để bảo mật

