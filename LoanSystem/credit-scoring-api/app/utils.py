import json
import os
from typing import Dict, Any

def _load_mapping(env_name: str, default_obj: Dict[str, int]) -> Dict[str, int]:
    raw = os.getenv(env_name, "").strip()
    if not raw:
        return default_obj
    try:
        obj = json.loads(raw)
        # normalize keys to upper for robust matching
        return {str(k).upper(): int(v) for k, v in obj.items()}
    except Exception:
        return default_obj

# Mặc định (có thể sửa bằng biến môi trường dạng JSON)
HOME_OWNERSHIP_MAP = _load_mapping(
    "HOME_OWNERSHIP_MAP_JSON",
    {
        "MORTGAGE": 0,
        "OWN": 1,
        "RENT": 2,
        # tiếng Việt tương đương
        "THẾ_CHẤP": 0, "SO_HUU": 1, "SỞ_HỮU": 1, "THUÊ": 2
    },
)

LOAN_INTENT_MAP = _load_mapping(
    "LOAN_INTENT_MAP_JSON",
    {
        "EDUCATION": 0,
        "MEDICAL": 1,
        "PERSONAL": 2,
        "VENTURE": 3,
        "DEBTCONSOLIDATION": 4,  # viết liền để dễ map
        "HOMEIMPROVEMENT": 5,
        # bản Việt hoá phổ biến
        "GIÁO_DỤC": 0, "Y_TẾ": 1, "CÁ_NHÂN": 2, "KHỞI_NGHIỆP": 3,
        "HỢP_NHẤT_NỢ": 4, "SỬA_CHỮA_NHÀ": 5
    },
)

DEFAULT_ON_FILE_MAP = _load_mapping(
    "DEFAULT_ON_FILE_MAP_JSON",
    {
        "N": 0,
        "Y": 1,
        "NO": 0,
        "YES": 1,
        # tiếng Việt
        "KHÔNG": 0, "CO": 1, "CÓ": 1
    },
)

def parse_number_like(s: Any) -> float:
    """
    Chấp nhận số, chuỗi có dấu phẩy/thanh phân tách.
    Ví dụ: "45,000" -> 45000 ;  "7,000" -> 7000
    """
    if isinstance(s, (int, float)):
        return float(s)
    if s is None:
        raise ValueError("Giá trị số bị thiếu")
    if isinstance(s, list):
        # Nếu là list, lấy phần tử đầu tiên
        if len(s) == 0:
            raise ValueError("List rỗng")
        s = s[0]
    s = str(s).strip()
    # bỏ dấu phẩy/dấu chấm phân tách nghìn
    s = s.replace(",", "").replace(" ", "")
    return float(s)

def map_home_ownership(v: Any) -> int:
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, list):
        if len(v) == 0:
            return 2  # mặc định RENT=2
        v = v[0]
    key = str(v).upper().replace(" ", "_")
    return HOME_OWNERSHIP_MAP.get(key, HOME_OWNERSHIP_MAP.get(key.replace("_", ""), 2))  # mặc định RENT=2

def map_loan_intent(v: Any) -> int:
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, list):
        if len(v) == 0:
            return 2  # mặc định PERSONAL=2
        v = v[0]
    key = str(v).upper().replace(" ", "")
    key_us = key.replace("_", "")
    return LOAN_INTENT_MAP.get(key, LOAN_INTENT_MAP.get(key_us, 2))  # mặc định PERSONAL=2

def map_default_on_file(v: Any) -> int:
    if isinstance(v, (int, float)):
        return int(v)
    if isinstance(v, list):
        if len(v) == 0:
            return 0  # mặc định N=0
        v = v[0]
    key = str(v).upper().strip()
    return DEFAULT_ON_FILE_MAP.get(key, 0)  # mặc định N=0

def get_threshold() -> float:
    try:
        return float(os.getenv("DECISION_THRESHOLD", "0.5"))
    except Exception:
        return 0.5
