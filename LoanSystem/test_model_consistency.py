#!/usr/bin/env python3
"""
Test script to verify model consistency across different environments:
1. Direct Python model loading
2. FastAPI endpoint
3. Web application

This script helps debug SHAP implementation and ensures consistent results.
"""

import requests
import json
import numpy as np
import lightgbm as lgb
import shap
from pathlib import Path

# Test data - using the same input across all environments
TEST_DATA = {
    "person_age": 25,
    "person_income": 50000,
    "person_home_ownership": "RENT",
    "person_emp_length": 2.0,
    "loan_intent": "EDUCATION",
    "loan_amnt": 10000,
    "cb_person_default_on_file": "N",
    "cb_person_cred_hist_length": 3.0
}

def test_direct_model():
    """Test direct model loading and prediction"""
    print("=== Testing Direct Model Loading ===")
    
    try:
        # Load model directly
        model_path = "credit-scoring-api/models/lightgbm_model.txt"
        if not Path(model_path).exists():
            print(f"❌ Model file not found: {model_path}")
            return None
            
        booster = lgb.Booster(model_file=model_path)
        
        # Prepare features in correct order
        feature_order = [
            "person_age", "person_income", "person_home_ownership", 
            "person_emp_length", "loan_intent", "loan_amnt", 
            "cb_person_default_on_file", "cb_person_cred_hist_length"
        ]
        
        # Convert test data to array
        x = np.array([[TEST_DATA[f] for f in feature_order]], dtype=float)
        
        # Get prediction
        score = float(booster.predict(x)[0])
        
        # Calculate SHAP values
        explainer = shap.TreeExplainer(booster)
        shap_values = explainer.shap_values(x)[0]
        expected_value = float(explainer.expected_value)
        shap_sum = float(np.sum(shap_values) + expected_value)
        
        # Create SHAP dictionary
        shap_dict = {feature_order[i]: float(shap_values[i]) for i in range(len(feature_order))}
        
        result = {
            "score": score,
            "shap_values": shap_dict,
            "shap_bias": expected_value,
            "shap_sum_check": shap_sum,
            "feature_values": {f: float(x[0][i]) for i, f in enumerate(feature_order)}
        }
        
        print(f"✅ Direct model prediction: {score:.6f}")
        print(f"✅ SHAP bias: {expected_value:.6f}")
        print(f"✅ SHAP sum check: {shap_sum:.6f}")
        print(f"✅ Feature values: {result['feature_values']}")
        print(f"✅ SHAP values: {shap_dict}")
        
        return result
        
    except Exception as e:
        print(f"❌ Direct model error: {e}")
        return None

def test_fastapi():
    """Test FastAPI endpoint"""
    print("\n=== Testing FastAPI Endpoint ===")
    
    try:
        # Test health endpoint first
        health_url = "http://localhost:8001/healthz"
        health_response = requests.get(health_url, timeout=5)
        
        if health_response.status_code == 200:
            print("✅ FastAPI health check passed")
            print(f"Health response: {health_response.json()}")
        else:
            print(f"❌ FastAPI health check failed: {health_response.status_code}")
            return None
        
        # Test prediction endpoint
        predict_url = "http://localhost:8001/predict"
        response = requests.post(predict_url, json=TEST_DATA, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ FastAPI prediction successful")
            print(f"Score: {result['score']:.6f}")
            print(f"Decision: {result['decision_en']} / {result['decision_vi']}")
            print(f"SHAP bias: {result['shap_bias']:.6f}")
            print(f"SHAP sum check: {result['shap_sum_check']:.6f}")
            print(f"SHAP values: {result['shap']}")
            return result
        else:
            print(f"❌ FastAPI prediction failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to FastAPI. Is it running on port 8001?")
        return None
    except Exception as e:
        print(f"❌ FastAPI error: {e}")
        return None

def test_web_backend():
    """Test web backend through Spring Boot"""
    print("\n=== Testing Web Backend ===")
    
    try:
        # Test health endpoint first
        health_url = "http://localhost:8080/actuator/health"
        health_response = requests.get(health_url, timeout=5)
        
        if health_response.status_code == 200:
            print("✅ Web backend health check passed")
        else:
            print(f"❌ Web backend health check failed: {health_response.status_code}")
            return None
        
        # Test prediction through web backend
        predict_url = "http://localhost:8080/api/applications/1"
        
        # Prepare data for web backend (it expects different format)
        web_data = {
            "personAge": TEST_DATA["person_age"],
            "personIncome": TEST_DATA["person_income"],
            "personHomeOwnership": TEST_DATA["person_home_ownership"],
            "personEmpLength": TEST_DATA["person_emp_length"],
            "loanIntent": TEST_DATA["loan_intent"],
            "loanAmnt": TEST_DATA["loan_amnt"],
            "cbPersonDefaultOnFile": TEST_DATA["cb_person_default_on_file"],
            "cbPersonCredHistLength": TEST_DATA["cb_person_cred_hist_length"]
        }
        
        response = requests.post(predict_url, json=web_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Web backend prediction successful")
            print(f"Score: {result.get('score', 'N/A')}")
            print(f"Decision: {result.get('decisionEn', 'N/A')} / {result.get('decisionVi', 'N/A')}")
            if 'shap' in result:
                print(f"SHAP values: {result['shap']}")
            return result
        else:
            print(f"❌ Web backend prediction failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to web backend. Is it running on port 8080?")
        return None
    except Exception as e:
        print(f"❌ Web backend error: {e}")
        return None

def compare_results(direct_result, fastapi_result, web_result):
    """Compare results from all three environments"""
    print("\n=== Comparing Results ===")
    
    if not direct_result:
        print("❌ No direct model result to compare")
        return
    
    if fastapi_result:
        print("\n--- Direct vs FastAPI ---")
        score_diff = abs(direct_result['score'] - fastapi_result['score'])
        print(f"Score difference: {score_diff:.10f}")
        
        if score_diff < 1e-10:
            print("✅ Scores match perfectly")
        else:
            print("❌ Scores differ!")
        
        # Compare SHAP values
        if 'shap' in fastapi_result:
            shap_match = True
            for feature, direct_shap in direct_result['shap_values'].items():
                fastapi_shap = fastapi_result['shap'].get(feature, 0)
                diff = abs(direct_shap - fastapi_shap)
                if diff > 1e-10:
                    print(f"❌ SHAP mismatch for {feature}: {direct_shap:.10f} vs {fastapi_shap:.10f}")
                    shap_match = False
                else:
                    print(f"✅ SHAP match for {feature}: {direct_shap:.10f}")
            
            if shap_match:
                print("✅ All SHAP values match")
            else:
                print("❌ Some SHAP values differ")
    
    if web_result:
        print("\n--- Direct vs Web Backend ---")
        if 'score' in web_result:
            score_diff = abs(direct_result['score'] - web_result['score'])
            print(f"Score difference: {score_diff:.10f}")
            
            if score_diff < 1e-10:
                print("✅ Scores match perfectly")
            else:
                print("❌ Scores differ!")

def main():
    """Main test function"""
    print("🔍 Model Consistency Test")
    print("=" * 50)
    print(f"Test data: {TEST_DATA}")
    print("=" * 50)
    
    # Test all environments
    direct_result = test_direct_model()
    fastapi_result = test_fastapi()
    web_result = test_web_backend()
    
    # Compare results
    compare_results(direct_result, fastapi_result, web_result)
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    main()