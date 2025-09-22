import os
from typing import Dict, Any, List, Tuple

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# ==== Cấu hình qua ENV ====
BASE_MODEL = os.getenv("BASE_MODEL", "unsloth/gpt-oss-20b-unsloth-bnb-4bit")
ADAPTER_PATH = os.getenv("ADAPTER_PATH", "/app/llm_adapter")
MAX_NEW_TOKENS = int(os.getenv("GEN_MAX_NEW_TOKENS", "400"))
TEMPERATURE = float(os.getenv("GEN_TEMPERATURE", "0.2"))
TOP_P = float(os.getenv("GEN_TOP_P", "0.9"))

# 4-bit cho V100 16GB
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,   # V100 dùng float16
)

_tokenizer = None
_model = None

def load_llm():
    """Lazy-load LLM + LoRA adapter (1 lần)."""
    global _tokenizer, _model
    if _model is not None:
        return _tokenizer, _model

    _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
    base = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        trust_remote_code=True,
        quantization_config=bnb_config,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    _model = PeftModel.from_pretrained(base, ADAPTER_PATH, is_trainable=False)
    _model.eval()
    return _tokenizer, _model

# Nhãn tiếng Việt cho feature
FEATURE_VI = {
    "person_income": "Thu nhập (person_income)",
    "loan_amnt": "Số tiền vay (loan_amnt)",
    "person_age": "Tuổi (person_age)",
    "cb_person_cred_hist_length": "Lịch sử tín dụng (cb_person_cred_hist_length)",
    "person_home_ownership": "Tình trạng sở hữu nhà (person_home_ownership)",
    "person_emp_length": "Thời gian làm việc (person_emp_length)",
    "loan_intent": "Mục đích vay (loan_intent)",
    "cb_person_default_on_file": "Lịch sử nợ xấu (cb_person_default_on_file)",
}

def _format_profile(profile: Dict[str, Any]) -> str:
    keys = [
        "person_age","person_income","person_home_ownership","person_emp_length",
        "loan_intent","loan_amnt","cb_person_default_on_file","cb_person_cred_hist_length"
    ]
    return "\n".join([f"- {k}: {profile.get(k)}" for k in keys if k in profile])

def _topk_shap(shap: Dict[str, float], k: int) -> List[Tuple[str, float]]:
    return sorted(shap.items(), key=lambda x: abs(x[1]), reverse=True)[:max(1, k)]

def build_prompt_vi(model_output: Dict[str, Any], profile_pretty: str, top_k: int) -> str:
    score = model_output.get("score")
    thr = model_output.get("threshold")
    approved = bool(model_output.get("approved"))
    decision = "CHẤP THUẬN" if approved else "TỪ CHỐI"

    shap = model_output.get("shap", {})
    ranked = _topk_shap(shap, top_k)

    bullets = []
    for key, val in ranked:
        name = FEATURE_VI.get(key, key)
        bullets.append(f"{name}: {val:+.4f}")

    # Gợi ý rule-based ngắn để LLM tham chiếu
    heuristics = []
    if shap.get("person_income", 0.0) < 0:
        heuristics.append("Xem xét tăng thu nhập thêm 20–30% so với hiện tại.")
    if shap.get("loan_amnt", 0.0) < 0:
        heuristics.append("Xem xét giảm số tiền vay xuống khoảng 70–80% so với hiện tại.")
    if shap.get("cb_person_cred_hist_length", 0.0) > 0:
        heuristics.append("Lịch sử tín dụng ổn định là lợi thế.")
    if not heuristics:
        heuristics.append("Duy trì hồ sơ tài chính lành mạnh và lịch sử tín dụng tốt.")

    heur_text = "\n".join([f"- {h}" for h in heuristics])

    return f"""Bạn là chuyên gia thẩm định tín dụng. Viết kết luận tiếng Việt, súc tích, đúng bố cục dưới đây.

[THÔNG TIN HỒ SƠ]
{profile_pretty}

[KẾT QUẢ MÔ HÌNH]
- Xác suất rủi ro (score): {score:.4f}
- Ngưỡng (threshold): {thr:.4f}
- Quyết định: {"ĐƯỢC VAY" if approved else "TỪ CHỐI"}

[ĐÓNG GÓP SHAP (raw score; + tăng rủi ro, - giảm rủi ro)]
{chr(10).join(f"- {b}" for b in bullets)}

[YÊU CẦU TRÌNH BÀY]
- Dòng đầu: "Quyết định: {decision} - …" + 1 câu tổng quan (yếu tố tiêu cực/tích cực).
- 6–8 gạch đầu dòng, mỗi dòng: "<nhãn>: ±0.0000 - diễn giải ngắn".
  * Dấu “+” = góp phần tăng rủi ro → xu hướng từ chối.
  * Dấu “-” = góp phần giảm rủi ro → xu hướng chấp thuận.
- Cuối: "Lời khuyên:" 1–2 câu, tham khảo gợi ý dưới.

[GỢI Ý THAM KHẢO]
{heur_text}

Xuất đúng định dạng:
Quyết định: …
- …
- …
Lời khuyên: …
"""

def generate_vi(model_output: Dict[str, Any], profile_raw: Dict[str, Any], top_k: int) -> str:
    tok, model = load_llm()
    prompt = build_prompt_vi(model_output, _format_profile(profile_raw), top_k)
    inputs = tok(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            temperature=TEMPERATURE,
            top_p=TOP_P,
            do_sample=True,
            pad_token_id=tok.eos_token_id,
            eos_token_id=tok.eos_token_id,
        )
    text = tok.decode(out[0], skip_special_tokens=True)
    return text[len(prompt):].strip()
