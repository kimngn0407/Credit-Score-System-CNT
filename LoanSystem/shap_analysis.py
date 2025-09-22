#!/usr/bin/env python3
"""
Detailed SHAP analysis script based on the user's provided code snippet.
This script helps debug SHAP implementation and ensures consistency.
"""

import numpy as np
import lightgbm as lgb
import shap
import json
from pathlib import Path

def load_model_and_explainer():
    """Load the LightGBM model and create SHAP explainer"""
    model_path = "credit-scoring-api/models/lightgbm_model.txt"
    
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    # Load the model
    booster = lgb.Booster(model_file=model_path)
    
    # Create SHAP explainer
    explainer = shap.TreeExplainer(booster)
    
    return booster, explainer

def analyze_shap_values(booster, explainer, test_data):
    """Analyze SHAP values for given test data"""
    
    # Feature order (must match the model's training order)
    feature_order = [
        "person_age", "person_income", "person_home_ownership", 
        "person_emp_length", "loan_intent", "loan_amnt", 
        "cb_person_default_on_file", "cb_person_cred_hist_length"
    ]
    
    # Convert test data to numpy array
    x = np.array([[test_data[f] for f in feature_order]], dtype=float)
    
    print("=== Input Data ===")
    for i, feature in enumerate(feature_order):
        print(f"{feature}: {x[0][i]}")
    
    # Get prediction
    prediction = booster.predict(x)[0]
    print(f"\n=== Prediction ===")
    print(f"Raw prediction: {prediction:.10f}")
    
    # Calculate SHAP values
    shap_values = explainer.shap_values(x)[0]
    expected_value = explainer.expected_value
    
    print(f"\n=== SHAP Analysis ===")
    print(f"Expected value (bias): {expected_value:.10f}")
    print(f"SHAP values: {shap_values}")
    
    # Calculate sum check
    shap_sum = np.sum(shap_values) + expected_value
    print(f"SHAP sum check: {shap_sum:.10f}")
    print(f"Prediction vs SHAP sum difference: {abs(prediction - shap_sum):.10f}")
    
    # Create feature-SHAP mapping
    feature_shap_map = {}
    for i, feature in enumerate(feature_order):
        feature_shap_map[feature] = float(shap_values[i])
    
    print(f"\n=== Feature SHAP Values ===")
    for feature, shap_val in feature_shap_map.items():
        print(f"{feature}: {shap_val:.10f}")
    
    # Analyze feature importance
    print(f"\n=== Feature Importance (by absolute SHAP value) ===")
    sorted_features = sorted(feature_shap_map.items(), key=lambda x: abs(x[1]), reverse=True)
    for feature, shap_val in sorted_features:
        print(f"{feature}: {shap_val:.10f} (abs: {abs(shap_val):.10f})")
    
    return {
        'prediction': float(prediction),
        'expected_value': float(expected_value),
        'shap_values': shap_values.tolist(),
        'feature_shap_map': feature_shap_map,
        'shap_sum_check': float(shap_sum)
    }

def test_multiple_samples():
    """Test SHAP consistency across multiple samples"""
    print("\n" + "="*60)
    print("TESTING MULTIPLE SAMPLES")
    print("="*60)
    
    booster, explainer = load_model_and_explainer()
    
    # Test multiple samples
    test_samples = [
        {
            "person_age": 25,
            "person_income": 50000,
            "person_home_ownership": "RENT",
            "person_emp_length": 2.0,
            "loan_intent": "EDUCATION",
            "loan_amnt": 10000,
            "cb_person_default_on_file": "N",
            "cb_person_cred_hist_length": 3.0
        },
        {
            "person_age": 35,
            "person_income": 75000,
            "person_home_ownership": "OWN",
            "person_emp_length": 8.0,
            "loan_intent": "PERSONAL",
            "loan_amnt": 15000,
            "cb_person_default_on_file": "N",
            "cb_person_cred_hist_length": 7.0
        },
        {
            "person_age": 45,
            "person_income": 120000,
            "person_home_ownership": "MORTGAGE",
            "person_emp_length": 15.0,
            "loan_intent": "HOMEIMPROVEMENT",
            "loan_amnt": 25000,
            "cb_person_default_on_file": "Y",
            "cb_person_cred_hist_length": 12.0
        }
    ]
    
    results = []
    for i, sample in enumerate(test_samples):
        print(f"\n--- Sample {i+1} ---")
        result = analyze_shap_values(booster, explainer, sample)
        results.append(result)
    
    return results

def verify_shap_properties():
    """Verify SHAP properties and consistency"""
    print("\n" + "="*60)
    print("VERIFYING SHAP PROPERTIES")
    print("="*60)
    
    booster, explainer = load_model_and_explainer()
    
    # Test with a simple sample
    test_data = {
        "person_age": 30,
        "person_income": 60000,
        "person_home_ownership": "RENT",
        "person_emp_length": 5.0,
        "loan_intent": "PERSONAL",
        "loan_amnt": 12000,
        "cb_person_default_on_file": "N",
        "cb_person_cred_hist_length": 5.0
    }
    
    result = analyze_shap_values(booster, explainer, test_data)
    
    # Verify SHAP properties
    print(f"\n=== SHAP Property Verification ===")
    
    # Property 1: Sum of SHAP values + expected value = prediction
    shap_sum = result['shap_sum_check']
    prediction = result['prediction']
    property1_check = abs(shap_sum - prediction) < 1e-10
    print(f"Property 1 (Sum = Prediction): {'✅ PASS' if property1_check else '❌ FAIL'}")
    print(f"  Difference: {abs(shap_sum - prediction):.2e}")
    
    # Property 2: SHAP values should be finite
    shap_values = np.array(result['shap_values'])
    property2_check = np.all(np.isfinite(shap_values))
    print(f"Property 2 (Finite values): {'✅ PASS' if property2_check else '❌ FAIL'}")
    
    # Property 3: Expected value should be finite
    property3_check = np.isfinite(result['expected_value'])
    print(f"Property 3 (Finite expected value): {'✅ PASS' if property3_check else '❌ FAIL'}")
    
    return result

def main():
    """Main analysis function"""
    print("🔍 SHAP Analysis and Consistency Check")
    print("="*60)
    
    try:
        # Load model and explainer
        booster, explainer = load_model_and_explainer()
        print("✅ Model and explainer loaded successfully")
        
        # Test single sample
        test_data = {
            "person_age": 25,
            "person_income": 50000,
            "person_home_ownership": "RENT",
            "person_emp_length": 2.0,
            "loan_intent": "EDUCATION",
            "loan_amnt": 10000,
            "cb_person_default_on_file": "N",
            "cb_person_cred_hist_length": 3.0
        }
        
        print("\n--- Single Sample Analysis ---")
        result = analyze_shap_values(booster, explainer, test_data)
        
        # Test multiple samples
        test_multiple_samples()
        
        # Verify SHAP properties
        verify_shap_properties()
        
        print("\n" + "="*60)
        print("🏁 Analysis completed!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

