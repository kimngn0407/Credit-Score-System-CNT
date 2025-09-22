# Credit Scoring API (FastAPI + LightGBM)

## Chạy local
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Docker
docker build -t credit-scoring-api:latest .
docker run -p 8000:8000 \
  -e DECISION_THRESHOLD=0.5 \
  -e MODEL_PATH=/app/models/lightgbm_model.txt \
  credit-scoring-api:latest

## Gọi thử
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "person_age": 30,
    "person_income": 15000,
    "person_home_ownership": 1,
    "person_emp_length": 5,
    "loan_intent": 2,
    "loan_amnt": 5000,
    "cb_person_default_on_file": 0,
    "cb_person_cred_hist_length": 6
  }'
