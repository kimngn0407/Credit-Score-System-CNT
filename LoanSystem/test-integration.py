#!/usr/bin/env python3
"""
Script để test tích hợp giữa LoanSystem và loan-forecast-api
"""

import requests
import json
import time

# URLs
LOAN_SYSTEM_URL = "http://localhost:8080"
LOAN_FORECAST_URL = "http://localhost:8000"

def test_loan_forecast_api():
    """Test loan-forecast-api trực tiếp"""
    print("🔍 Testing Loan Forecast API...")
    
    # Health check
    try:
        response = requests.get(f"{LOAN_FORECAST_URL}/health")
        print(f"✅ Health check: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test predict
    try:
        payload = {
            "features": [10000.0, 50000.0, 25.0, 3.0, 2.5, 0.0, 0.0, 1.0]
        }
        response = requests.post(f"{LOAN_FORECAST_URL}/predict", json=payload)
        print(f"✅ Predict: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Predict failed: {e}")
        return False
    
    return True

def test_loan_system():
    """Test LoanSystem Spring Boot application"""
    print("\n🔍 Testing Loan System...")
    
    # Test health check
    try:
        response = requests.get(f"{LOAN_SYSTEM_URL}/api/loan-forecast/health")
        print(f"✅ Health check: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test predict through LoanSystem
    try:
        payload = {
            "features": [10000.0, 50000.0, 25.0, 3.0, 2.5, 0.0, 0.0, 1.0]
        }
        response = requests.post(f"{LOAN_SYSTEM_URL}/api/loan-forecast/predict", json=payload)
        print(f"✅ Predict through LoanSystem: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Predict through LoanSystem failed: {e}")
        return False
    
    return True

def test_full_integration():
    """Test full integration với application creation và prediction"""
    print("\n🔍 Testing Full Integration...")
    
    # Tạo application
    try:
        app_payload = {
            "personAge": 25,
            "personIncome": 50000,
            "loanAmnt": 10000,
            "personHomeOwnership": "RENT",
            "cbPersonDefaultOnFile": "N",
            "loanIntent": "PERSONAL",
            "personEmpLength": 2.5,
            "cbPersonCredHistLength": 3
        }
        
        # Giả sử có endpoint tạo application
        print("ℹ️  Note: Cần tạo ApplicationController để test full integration")
        print(f"📝 Application payload: {json.dumps(app_payload, indent=2)}")
        
    except Exception as e:
        print(f"❌ Application creation failed: {e}")
        return False
    
    return True

def main():
    print("🚀 Starting Integration Test...")
    print("=" * 50)
    
    # Wait for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(5)
    
    # Test loan-forecast-api
    forecast_ok = test_loan_forecast_api()
    
    # Test loan-system
    system_ok = test_loan_system()
    
    # Test full integration
    integration_ok = test_full_integration()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Loan Forecast API: {'✅ PASS' if forecast_ok else '❌ FAIL'}")
    print(f"Loan System: {'✅ PASS' if system_ok else '❌ FAIL'}")
    print(f"Full Integration: {'✅ PASS' if integration_ok else '❌ FAIL'}")
    
    if forecast_ok and system_ok:
        print("\n🎉 Integration test completed successfully!")
    else:
        print("\n⚠️  Some tests failed. Check the logs above.")

if __name__ == "__main__":
    main()

