from typing import Dict, Any
from pydantic import BaseModel, Field

class ModelOutput(BaseModel):
    score: float
    threshold: float
    approved: bool
    shap: Dict[str, float] = Field(..., description="SHAP theo feature từ model chấm điểm")

class NarrativeRequest(BaseModel):
    # Hồ sơ gốc (thân thiện) để in ra trong prompt
    profile_raw: Dict[str, Any]
    model_output: ModelOutput
    # Tuỳ chọn: lấy Top-K SHAP lớn nhất theo |giá trị|
    top_k: int = 8

class NarrativeResponse(BaseModel):
    decision_vi: str
    score: float
    threshold: float
    narrative_vi: str
