# app/schemas.py
from pydantic import BaseModel, Field, field_validator
from typing import Any, Dict

class CreditApplication(BaseModel):
    # Nhập “thân thiện” (chuỗi có dấu phẩy, nhãn chữ / tiếng Việt)
    person_age: Any = Field(..., description="Tuổi, ví dụ: 27 hoặc '27'")
    person_income: Any = Field(..., description="Thu nhập, ví dụ: 45000 hoặc '45,000'")
    person_home_ownership: Any = Field(..., description="0/1/2 hoặc 'RENT'/'OWN'/'MORTGAGE' (hỗ trợ TV)")
    person_emp_length: Any = Field(..., description="Số năm làm việc, ví dụ: 1 hoặc '1.0'")
    loan_intent: Any = Field(..., description="0..5 hoặc 'EDUCATION','PERSONAL',... (hỗ trợ TV)")
    loan_amnt: Any = Field(..., description="Khoản vay, ví dụ: 7000 hoặc '7,000'")
    cb_person_default_on_file: Any = Field(..., description="0/1 hoặc 'Y'/'N' (hỗ trợ TV)")
    cb_person_cred_hist_length: Any = Field(..., description="Tuổi lịch sử tín dụng, ví dụ: 9 hoặc '9.0'")

    # Tiền xử lý trước khi ép kiểu
    @field_validator("person_age", "person_emp_length", "cb_person_cred_hist_length", mode="before")
    @classmethod
    def _num_plain(cls, v: Any):
        from .utils import parse_number_like
        return parse_number_like(v)

    @field_validator("person_income", "loan_amnt", mode="before")
    @classmethod
    def _money_like(cls, v: Any):
        from .utils import parse_number_like
        return parse_number_like(v)

    @field_validator("person_home_ownership", mode="before")
    @classmethod
    def _home_map(cls, v: Any):
        from .utils import map_home_ownership
        return map_home_ownership(v)

    @field_validator("loan_intent", mode="before")
    @classmethod
    def _intent_map(cls, v: Any):
        from .utils import map_loan_intent
        return map_loan_intent(v)

    @field_validator("cb_person_default_on_file", mode="before")
    @classmethod
    def _default_map(cls, v: Any):
        from .utils import map_default_on_file
        return map_default_on_file(v)

class PredictResponse(BaseModel):
    score: float                    # Xác suất vỡ nợ (default probability)
    approved: bool
    decision_en: str               # "APPROVED"/"REJECTED"
    decision_vi: str               # "ĐƯỢC VAY"/"KHÔNG ĐƯỢC VAY"
    threshold: float
    note_vi: str = "Quy tắc: duyệt nếu score < threshold (score thấp = rủi ro thấp)."
    shap: Dict[str, float]         # SHAP cho từng feature
    shap_bias: float               # Bias (base value)
    shap_sum_check: float          # Tổng tất cả shap + bias (để đối chiếu)
