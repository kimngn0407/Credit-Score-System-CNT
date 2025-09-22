import os
from fastapi import FastAPI, HTTPException, Header
from .schemas import NarrativeRequest, NarrativeResponse
from .llm import generate_vi
import torch

REQUIRE_API_KEY = os.getenv("NLG_API_KEY", "").strip()  # nếu set -> bắt buộc header

app = FastAPI(
    title="Credit NLG Service (GPU)",
    version="1.0.0",
    description="Nhận (output từ model chấm điểm + hồ sơ) → sinh văn bản giải thích tiếng Việt."
)

@app.get("/healthz")
def healthz():
    gpu = torch.cuda.is_available()
    name = torch.cuda.get_device_name(0) if gpu else None
    return {"status": "ok", "gpu": gpu, "gpu_name": name}

@app.post("/nlg", response_model=NarrativeResponse)
def nlg(req: NarrativeRequest, x_api_key: str = Header(default=None, alias="X-API-KEY")):
    # Bảo vệ đơn giản bằng API key (tuỳ chọn)
    if REQUIRE_API_KEY and x_api_key != REQUIRE_API_KEY:
        raise HTTPException(401, "Unauthorized")

    try:
        text = generate_vi(req.model_output.model_dump(), req.profile_raw, req.top_k)
        decision_vi = "ĐƯỢC VAY" if req.model_output.approved else "TỪ CHỐI"
        return NarrativeResponse(
            decision_vi=decision_vi,
            score=req.model_output.score,
            threshold=req.model_output.threshold,
            narrative_vi=text
        )
    except Exception as e:
        raise HTTPException(500, f"Lỗi sinh văn bản: {e}")
