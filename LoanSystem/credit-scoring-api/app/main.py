# app/main.py
import os
from pathlib import Path
import numpy as np
from fastapi import FastAPI, HTTPException
from lightgbm import Booster
import shap

from .schemas import CreditApplication, PredictResponse
from .utils import get_threshold

def resolve_model_path() -> str:
    env_path = os.getenv("MODEL_PATH", "").strip()
    candidates = []
    if env_path:
        candidates.append(Path(env_path))
    candidates.append(Path(__file__).resolve().parent.parent / "models" / "lightgbm_model.txt")
    candidates.append(Path.cwd() / "models" / "lightgbm_model.txt")
    for p in candidates:
        if p.is_file():
            return str(p)
    raise FileNotFoundError("Không tìm thấy lightgbm_model.txt. Hãy đặt vào models/ hoặc set MODEL_PATH.")

MODEL_PATH = resolve_model_path()

app = FastAPI(
    title="Credit Scoring API / API Chấm điểm Tín dụng",
    version="1.2.0",
    description=(
        "Nhận input thân thiện ('RENT', 'EDUCATION', '45,000'...) → tự chuẩn hoá, "
        "trả về score + quyết định (EN/VI) + SHAP values."
    ),
)

try:
    booster = Booster(model_file=MODEL_PATH)
    # Initialize SHAP TreeExplainer
    explainer = shap.TreeExplainer(booster)
except Exception as e:
    raise RuntimeError(f"Không thể nạp model từ {MODEL_PATH}: {e}")

FEATURE_ORDER = [
    "person_age",
    "person_income",
    "person_home_ownership",
    "person_emp_length",
    "loan_intent",
    "loan_amnt",
    "cb_person_default_on_file",
    "cb_person_cred_hist_length",
]

@app.get("/healthz")
def healthz():
    p = Path(MODEL_PATH)
    return {"status": "ok", "model_path": MODEL_PATH, "exists": p.is_file(), "cwd": str(Path.cwd())}

@app.post("/predict", response_model=PredictResponse)
def predict(payload: CreditApplication):
    try:
        # 1) Chuẩn hoá input theo đúng thứ tự cột của model
        x = np.array([[getattr(payload, f) for f in FEATURE_ORDER]], dtype=float)

        # 2) Dự đoán xác suất
        score = float(booster.predict(x)[0])

        # 3) Tính SHAP với TreeExplainer (giống như trong Python)
        shap_values = explainer.shap_values(x)[0]  # Get first (and only) sample
        expected_value = float(explainer.expected_value)
        
        # Create feature-SHAP dictionary
        shap_map = {FEATURE_ORDER[i]: float(shap_values[i]) for i in range(len(FEATURE_ORDER))}
        shap_bias = expected_value
        shap_sum_check = float(np.sum(shap_values) + expected_value)

        # 4) Quyết định
        thr = get_threshold()
        # FIXED: Model predicts default probability, so low score = low risk = approve
        approved = score < thr   # score thấp = rủi ro thấp -> duyệt
        decision_en = "APPROVED" if approved else "REJECTED"
        decision_vi = "ĐƯỢC VAY" if approved else "KHÔNG ĐƯỢC VAY"

        # 5) Trả kết quả (kèm SHAP)
        return PredictResponse(
            score=score,
            approved=approved,
            decision_en=decision_en,
            decision_vi=decision_vi,
            threshold=thr,
            shap=shap_map,
            shap_bias=shap_bias,
            shap_sum_check=shap_sum_check,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi suy luận: {e}")
