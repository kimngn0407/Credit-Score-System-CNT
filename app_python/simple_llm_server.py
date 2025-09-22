#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple LLM Server for testing
"""
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import json

app = FastAPI()

class Query(BaseModel):
    messages: list

@app.post("/generate")
def generate_text(query: Query):
    """
    Mock LLM response for testing
    """
    # Extract user message
    user_message = ""
    for msg in query.messages:
        if msg.get("role") == "user":
            user_message = msg.get("content", "")
            break
    
    # Mock response based on content
    if "TỪ CHỐI" in user_message or "từ chối" in user_message.lower():
        response = """
Dựa trên phân tích SHAP values, hồ sơ vay này bị từ chối chủ yếu do các yếu tố sau:

1. **Thu nhập thấp (person_income: -1.9118)**: Với thu nhập 44,000 USD/năm, khách hàng có khả năng trả nợ hạn chế, đặc biệt khi vay 3,600 USD.

2. **Mục đích vay không phù hợp (loan_intent: -1.7893)**: Vay để cải thiện nhà ở (HOMEIMPROVEMENT) không được ưu tiên cao trong điều kiện tài chính hiện tại.

3. **Tuổi trẻ (person_age: -0.9083)**: 22 tuổi có ít kinh nghiệm tài chính và ổn định nghề nghiệp.

4. **Thuê nhà (person_home_ownership: -0.6261)**: Không có tài sản thế chấp, rủi ro cao hơn.

5. **Có lịch sử nợ xấu (cb_person_default_on_file: -0.5715)**: Yếu tố rủi ro quan trọng.

**Khuyến nghị**: Khách hàng nên tăng thu nhập, ổn định công việc và cải thiện lịch sử tín dụng trước khi nộp hồ sơ vay mới.
        """
    else:
        response = f"""
Đây là phản hồi mẫu từ LLM server local.

Bạn đã gửi: {user_message[:100]}...

Server đang hoạt động bình thường và sẵn sàng xử lý các yêu cầu thực tế.
        """
    
    return {"generated_text": response.strip()}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "LLM Server is running"}

if __name__ == "__main__":
    print("🚀 Starting Simple LLM Server...")
    print("📍 Server will run on: http://localhost:8000")
    print("🔗 Health check: http://localhost:8000/health")
    print("📝 API endpoint: http://localhost:8000/generate")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
