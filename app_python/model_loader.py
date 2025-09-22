"""
Model Loader Module
Tải và quản lý LORA Adapter và LightGBM models
"""

import json
import os
import lightgbm as lgb
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    print("Warning: SHAP not available. Install with: pip install shap")

class ModelLoader:
    def __init__(self, model_dir: str = "."):
        self.model_dir = model_dir
        self.adapter_config = None
        self.lightgbm_model = None
        self.shap_explainer = None
        self.adapter_info = {}
        self.lgb_info = {}
        self.feature_names = ['person_age', 'person_income', 'person_home_ownership', 'person_emp_length', 
                             'loan_intent', 'loan_amnt', 'cb_person_default_on_file', 'cb_person_cred_hist_length']
        
    def load_adapter_config(self, config_path: str = "adapter_config.json") -> Dict[str, Any]:
        """Load LORA adapter configuration"""
        try:
            config_file = os.path.join(self.model_dir, config_path)
            with open(config_file, 'r', encoding='utf-8') as f:
                self.adapter_config = json.load(f)
            
            # Extract key information
            self.adapter_info = {
                "Base Model": self.adapter_config.get("base_model_name_or_path", "Unknown"),
                "PEFT Type": self.adapter_config.get("peft_type", "Unknown"),
                "Task Type": self.adapter_config.get("task_type", "Unknown"),
                "LoRA Rank (r)": self.adapter_config.get("r", 0),
                "LoRA Alpha": self.adapter_config.get("lora_alpha", 0),
                "LoRA Dropout": self.adapter_config.get("lora_dropout", 0),
                "Target Modules": self.adapter_config.get("target_modules", []),
                "Inference Mode": self.adapter_config.get("inference_mode", False),
                "Use DoRA": self.adapter_config.get("use_dora", False),
                "Use QLoRA": self.adapter_config.get("use_qalora", False),
            }
            
            return self.adapter_config
        except Exception as e:
            print(f"Error loading adapter config: {e}")
            return {}
    
    def load_lightgbm_model(self, model_path: str = "lightgbm_model.txt") -> Optional[lgb.Booster]:
        """Load LightGBM model"""
        try:
            model_file = os.path.join(self.model_dir, model_path)
            self.lightgbm_model = lgb.Booster(model_file=model_file)
            
            # Extract model information
            self.lgb_info = {
                "Number of Trees": self.lightgbm_model.num_trees(),
                "Number of Features": self.lightgbm_model.num_feature(),
                "Objective": self.lightgbm_model.params.get("objective", "Unknown"),
                "Boosting Type": self.lightgbm_model.params.get("boosting_type", "gbdt"),
                "Feature Names": self.lightgbm_model.feature_name(),
                "Number of Classes": self.lightgbm_model.num_model_per_iteration(),
            }
            
            # Create SHAP explainer if available
            if SHAP_AVAILABLE:
                try:
                    self.shap_explainer = shap.TreeExplainer(self.lightgbm_model)
                    print("✅ SHAP TreeExplainer created successfully")
                except Exception as e:
                    print(f"⚠️ Warning: Could not create SHAP explainer: {e}")
                    self.shap_explainer = None
            else:
                print("⚠️ SHAP not available. Install with: pip install shap")
                self.shap_explainer = None
            
            return self.lightgbm_model
        except Exception as e:
            print(f"Error loading LightGBM model: {e}")
            return None
    
    def get_adapter_summary(self) -> Dict[str, Any]:
        """Get LORA adapter summary information"""
        if not self.adapter_config:
            return {"error": "Adapter config not loaded"}
        
        return self.adapter_info
    
    def get_lightgbm_summary(self) -> Dict[str, Any]:
        """Get LightGBM model summary information"""
        if not self.lightgbm_model:
            return {"error": "LightGBM model not loaded"}
        
        return self.lgb_info
    
    def predict_lightgbm(self, data: np.ndarray) -> np.ndarray:
        """Make predictions using LightGBM model"""
        if not self.lightgbm_model:
            raise ValueError("LightGBM model not loaded")
        
        return self.lightgbm_model.predict(data)
    
    def calculate_shap_for_sample(self, sample_data: np.ndarray) -> Dict[str, Any]:
        """
        Calculate SHAP values for a single sample using TreeExplainer
        Returns real SHAP values instead of approximated ones
        """
        if not self.lightgbm_model:
            raise ValueError("LightGBM model not loaded")
        
        if not self.shap_explainer:
            raise ValueError("SHAP explainer not available. Install SHAP or check if model loaded correctly.")
        
        if sample_data.ndim == 1:
            sample_data = sample_data.reshape(1, -1)
        
        try:
            # Get SHAP values for the sample (in logit space)
            sample_shap_values = self.shap_explainer.shap_values(sample_data)[0]  # Get first (and only) sample
            expected_value = self.shap_explainer.expected_value
            
            # Get predictions in both spaces
            prediction_proba = self.lightgbm_model.predict(sample_data)[0]  # Probability space (0-1)
            prediction_raw = self.lightgbm_model.predict(sample_data, num_iteration=self.lightgbm_model.best_iteration)[0]  # Try to get raw
            
            # For verification, we need raw prediction (logit space)
            # SHAP works in logit space, so expected + shap_sum should equal raw prediction
            try:
                # Try to get raw prediction without sigmoid
                prediction_raw_logit = np.log(prediction_proba / (1 - prediction_proba))  # Convert back to logit
            except:
                prediction_raw_logit = prediction_proba  # Fallback
            
            prediction_label = int(prediction_proba > 0.5)
            
            # Create feature-SHAP dictionary
            feature_shap_dict = dict(zip(self.feature_names, sample_shap_values))
            sorted_features = sorted(feature_shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)
            
            # Get original sample values
            sample_dict = dict(zip(self.feature_names, sample_data[0]))
            
            # Calculate verification in logit space
            expected_plus_shap = expected_value + np.sum(sample_shap_values)
            
            return {
                'prediction_proba': float(prediction_proba),
                'prediction_raw_logit': float(prediction_raw_logit),
                'prediction_label': int(prediction_label),
                'expected_value': float(expected_value),
                'shap_values': {k: float(v) for k, v in feature_shap_dict.items()},
                'sorted_features': [(k, float(v)) for k, v in sorted_features],
                'sample_data': {k: float(v) for k, v in sample_dict.items()},
                'shap_sum': float(np.sum(sample_shap_values)),
                'verification': {
                    'expected_plus_shap': float(expected_plus_shap),
                    'raw_prediction_logit': float(prediction_raw_logit),
                    'difference_logit': float(abs(expected_plus_shap - prediction_raw_logit)),
                    'sigmoid_of_expected_plus_shap': float(1 / (1 + np.exp(-expected_plus_shap)))
                }
            }
        except Exception as e:
            raise ValueError(f"Error calculating SHAP values: {e}")
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Get feature importance from LightGBM model"""
        if not self.lightgbm_model:
            return pd.DataFrame()
        
        feature_names = self.lightgbm_model.feature_name()
        importance_gain = self.lightgbm_model.feature_importance(importance_type='gain')
        importance_split = self.lightgbm_model.feature_importance(importance_type='split')
        
        df = pd.DataFrame({
            'feature': feature_names,
            'importance_gain': importance_gain,
            'importance_split': importance_split
        })
        
        return df.sort_values('importance_gain', ascending=False)
    
    def generate_sample_data(self, n_samples: int = 5) -> pd.DataFrame:
        """Generate sample data for LightGBM prediction demo"""
        if not self.lightgbm_model:
            return pd.DataFrame()
        
        feature_names = self.lightgbm_model.feature_name()
        
        # Create sample data based on typical loan application features
        np.random.seed(42)
        sample_data = {
            'person_age': np.random.randint(18, 65, n_samples),
            'person_income': np.random.randint(25000, 150000, n_samples),
            'person_home_ownership': np.random.randint(0, 3, n_samples),  # 0: RENT, 1: OWN, 2: MORTGAGE
            'person_emp_length': np.random.randint(0, 15, n_samples),
            'loan_intent': np.random.randint(0, 6, n_samples),  # Different loan purposes
            'loan_amnt': np.random.randint(1000, 40000, n_samples),
            'cb_person_default_on_file': np.random.randint(0, 2, n_samples),  # 0: No, 1: Yes
            'cb_person_cred_hist_length': np.random.randint(2, 18, n_samples)
        }
        
        return pd.DataFrame(sample_data)

def load_models(model_dir: str = ".") -> ModelLoader:
    """Factory function to load both models"""
    loader = ModelLoader(model_dir)
    loader.load_adapter_config()
    loader.load_lightgbm_model()
    return loader

if __name__ == "__main__":
    # Test the model loader
    loader = load_models(".")
    
    print("=== LORA Adapter Info ===")
    print(json.dumps(loader.get_adapter_summary(), indent=2))
    
    print("\n=== LightGBM Model Info ===")
    print(json.dumps(loader.get_lightgbm_summary(), indent=2))
    
    print("\n=== Feature Importance ===")
    print(loader.get_feature_importance())
    
    print("\n=== Sample Prediction ===")
    sample_data = loader.generate_sample_data(3)
    print(sample_data)
    
    if loader.lightgbm_model:
        predictions = loader.predict_lightgbm(sample_data.values)
        print("Predictions:", predictions)