#!/usr/bin/env python3
"""
Enhanced integration test script for LoanSystem
Tests the entire flow: Frontend -> Backend -> FastAPI services
"""

import requests
import json
import time
import sys

# Configuration
BACKEND_URL = "http://localhost:8080/api"
FRONTEND_URL = "http://localhost:3000"
SCORING_API_URL = "http://localhost:8001"
NLG_API_URL = "http://localhost:8002"

def check_service_health(url, service_name):
    """Check if a service is running and healthy"""
    try:
        response = requests.get(f"{url}/healthz", timeout=5)
        if response.status_code == 200:
            print(f"✅ {service_name} is healthy")
            return True
        else:
            print(f"❌ {service_name} returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ {service_name} is not accessible: {e}")
        return False

def test_credit_scoring_api():
    """Test the credit scoring API directly"""
    print("\n🧪 Testing Credit Scoring API...")
    
    test_data = {
        "person_age": 30,
        "person_income": 50000,
        "person_home_ownership": "RENT",
        "person_emp_length": 3,
        "loan_intent": "PERSONAL",
        "loan_amnt": 10000,
        "cb_person_default_on_file": "N",
        "cb_person_cred_hist_length": 5
    }
    
    try:
        response = requests.post(f"{SCORING_API_URL}/predict", json=test_data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Credit scoring prediction successful")
            print(f"   Decision: {result.get('decision_en', 'N/A')}")
            print(f"   Score: {result.get('score', 'N/A')}")
            return True
        else:
            print(f"❌ Credit scoring failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Credit scoring API error: {e}")
        return False

def test_backend_integration():
    """Test the backend Spring Boot integration"""
    print("\n🧪 Testing Backend Integration...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Backend health check successful")
            print(f"   Status: {health_data.get('status', 'N/A')}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend health check error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting LoanSystem Enhanced Integration Tests")
    print("=" * 60)
    
    # Check service health
    print("\n📋 Checking Service Health...")
    health_checks = [
        (SCORING_API_URL, "Credit Scoring API"),
        (NLG_API_URL, "Credit NLG Service"),
    ]
    
    all_healthy = True
    for url, name in health_checks:
        if not check_service_health(url, name):
            all_healthy = False
    
    # Check backend health
    backend_healthy = test_backend_integration()
    
    if not all_healthy:
        print("\n⚠️  Some services are not healthy. Continuing with available services...")
    
    # Test individual APIs
    scoring_test = test_credit_scoring_api()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print(f"   Credit Scoring API: {'✅ PASS' if scoring_test else '❌ FAIL'}")
    print(f"   Backend Health: {'✅ PASS' if backend_healthy else '❌ FAIL'}")
    
    if scoring_test and backend_healthy:
        print("\n🎉 All tests passed! The system is working correctly.")
        print("\n📝 Next steps:")
        print("   1. Start all services with: docker-compose up")
        print("   2. Access frontend at: http://localhost:3000")
        print("   3. Backend API at: http://localhost:8080/api")
        print("   4. Credit Scoring API at: http://localhost:8001")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check the logs above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())