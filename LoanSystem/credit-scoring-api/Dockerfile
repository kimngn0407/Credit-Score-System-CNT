FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Cài đặt các thư viện cần thiết cho wheel (numpy/lightgbm dùng wheel, không cần build)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy yêu cầu & cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source và model
COPY app ./app
COPY models ./models

# Cấu hình mặc định
ENV MODEL_PATH=/app/models/lightgbm_model.txt
ENV DECISION_THRESHOLD=0.5

EXPOSE 8000

# Chạy uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
