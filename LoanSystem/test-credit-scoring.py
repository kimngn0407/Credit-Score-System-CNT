#!/usr/bin/env python3
"""
Test script for Credit Scoring API
"""
import requests
import json
import sys

# Test data
test_data = {
    "person_age": 27,
    "person_income": 45000,
    "person_home_ownership": "RENT",
    "person_emp_length": 1,
    "loan_intent": "EDUCATION", 
    "loan_amnt": 7000,
    "cb_person_default_on_file": "N",
    "cb_person_cred_hist_length": 9
}

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:8001/healthz", timeout=10)
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"Health check error: {e}")
        return False

def test_predict():
    """Test predict endpoint"""
    try:
        response = requests.post(
            "http://localhost:8001/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        print(f"Predict request: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Score: {result.get('score')}")
            print(f"Decision: {result.get('decision_vi')}")
            print(f"Approved: {result.get('approved')}")
            return True
        else:
            print(f"Predict failed: {response.text}")
            return False
    except Exception as e:
        print(f"Predict error: {e}")
        return False

def main():
    print("🧪 Testing Credit Scoring API...")
    print("=" * 50)
    
    # Test health
    print("\n1. Testing health endpoint...")
    health_ok = test_health()
    
    # Test predict
    print("\n2. Testing predict endpoint...")
    predict_ok = test_predict()
    
    print("\n" + "=" * 50)
    if health_ok and predict_ok:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
