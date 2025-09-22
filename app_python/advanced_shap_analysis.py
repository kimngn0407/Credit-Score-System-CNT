"""
Advanced SHAP Analysis - Optimized for your environment
Phân tích SHAP chi tiết với visualization và explanation
"""
import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from model_loader import load_models

warnings.filterwarnings('ignore')

def logit_to_prob(logit):
    """Convert log-odds to probability, handling extreme values"""
    logit = np.clip(logit, -10, 10)  # Prevent overflow
    return 1 / (1 + np.exp(-logit))

def prob_to_logit(prob):
    """Convert probability to log-odds, handling edge cases"""
    prob = np.clip(prob, 1e-7, 1-1e-7)  # Prevent log(0)
    return np.log(prob / (1 - prob))

def explain_local_prediction_advanced(sample_data, loader):
    """
    Advanced local SHAP explanation using your existing model
    
    Args:
        sample_data: numpy array of feature values
        loader: ModelLoader instance with trained model and SHAP explainer
    
    Returns:
        dict: Detailed explanation results
    """
    
    if not hasattr(loader, 'shap_explainer') or loader.shap_explainer is None:
        print("❌ SHAP explainer not available. Please create it first.")
        return None
    
    if not hasattr(loader, 'lightgbm_model') or loader.lightgbm_model is None:
        print("❌ LightGBM model not available.")
        return None
    
    # Ensure sample_data is 2D
    if sample_data.ndim == 1:
        sample_data = sample_data.reshape(1, -1)
    
    print(f"🔍 ADVANCED SHAP LOCAL EXPLANATION")
    print("="*75)
    
    # Get model predictions
    prediction_proba = loader.lightgbm_model.predict(sample_data)[0]
    prediction_class = int(prediction_proba > 0.5)
    model_prediction_logit = prob_to_logit(prediction_proba)
    
    print(f"Model Prediction: {prediction_class} ({'Reject' if prediction_class == 0 else 'Approve'})")
    print(f"Model Probability: {prediction_proba:.4f} ({prediction_proba:.1%})")
    print(f"Model Log-odds: {model_prediction_logit:.4f}")
    
    # Calculate SHAP values
    try:
        shap_result = loader.calculate_shap_for_sample(sample_data)
        
        # Extract SHAP data
        shap_values = shap_result['shap_values']
        expected_value = shap_result['expected_value']
        expected_value_proba = shap_result.get('expected_value_proba', logit_to_prob(expected_value))
        shap_percentages = shap_result.get('shap_percentages', {})
        
        print(f"\n📊 SHAP BREAKDOWN (All calculations in log-odds space)")
        print("="*55)
        print(f"Baseline Log-odds:     {expected_value:.4f} → Prob: {expected_value_proba:.4f} ({expected_value_proba:.1%})")
        print(f"Model Log-odds:        {model_prediction_logit:.4f} → Prob: {prediction_proba:.4f} ({prediction_proba:.1%})")
        
        # Calculate verification
        total_shap_change = sum(shap_values.values())
        verification_logit = expected_value + total_shap_change
        difference_logit = model_prediction_logit - expected_value
        
        print(f"Difference (Pred - Base): {difference_logit:+.4f} log-odds")
        print(f"Total SHAP Change:        {total_shap_change:+.4f} log-odds")
        print(f"\n🔍 VERIFICATION (Log-odds space):")
        print(f"  Baseline + SHAP Total = {expected_value:.4f} + ({total_shap_change:+.4f}) = {verification_logit:.4f}")
        print(f"  Model Prediction      = {model_prediction_logit:.4f}")
        print(f"  Difference           = {abs(verification_logit - model_prediction_logit):.6f}")
        
        verification_ok = abs(verification_logit - model_prediction_logit) < 0.001
        print(f"  Status: {'✅ CHÍNH XÁC' if verification_ok else '❌ SAI'}")
        
        # Create detailed explanation table
        feature_names = loader.feature_names
        sample_values = sample_data[0] if sample_data.ndim > 1 else sample_data
        
        explanation_data = []
        for i, feature in enumerate(feature_names):
            shap_val = shap_values[feature]
            percentage = shap_percentages.get(feature, 0)
            
            explanation_data.append({
                'Feature': feature,
                'Feature_Value': sample_values[i],
                'SHAP_Value_Logit': shap_val,
                'Contribution_Pct': percentage,
                'Effect': 'Positive (+)' if shap_val > 0 else 'Negative (-)' if shap_val < 0 else 'Neutral'
            })
        
        explanation_df = pd.DataFrame(explanation_data)
        explanation_df['Abs_SHAP'] = np.abs(explanation_df['SHAP_Value_Logit'])
        explanation_df = explanation_df.sort_values('Abs_SHAP', ascending=False).drop('Abs_SHAP', axis=1)
        
        print(f"\n📋 DETAILED SHAP EXPLANATION TABLE")
        print("="*100)
        print(f"{'Feature':<25} {'Value':<12} {'SHAP (logit)':<15} {'Contrib%':<10} {'Effect':<12}")
        print("-"*100)
        
        for idx, row in explanation_df.iterrows():
            feature_val = row['Feature_Value']
            if isinstance(feature_val, (int, float)):
                if abs(feature_val - round(feature_val)) < 0.001:
                    val_str = f"{int(round(feature_val))}"
                else:
                    val_str = f"{feature_val:.2f}"
            else:
                val_str = str(feature_val)[:10]
            
            print(f"{row['Feature']:<25} {val_str:<12} {row['SHAP_Value_Logit']:<+15.6f} {row['Contribution_Pct']:<+10.1f} {row['Effect']:<12}")
        
        # Summary statistics
        positive_features = explanation_df[explanation_df['SHAP_Value_Logit'] > 0]
        negative_features = explanation_df[explanation_df['SHAP_Value_Logit'] < 0]
        
        positive_sum = positive_features['SHAP_Value_Logit'].sum() if len(positive_features) > 0 else 0
        negative_sum = negative_features['SHAP_Value_Logit'].sum() if len(negative_features) > 0 else 0
        
        print(f"\n📈 SUMMARY STATISTICS")
        print("="*50)
        print(f"Positive Contributions (logit): {positive_sum:+.6f} ({len(positive_features)} features)")
        print(f"Negative Contributions (logit): {negative_sum:+.6f} ({len(negative_features)} features)")
        print(f"Net Effect (logit): {positive_sum + negative_sum:+.6f}")
        
        # Convert to probability space for interpretation
        baseline_plus_positive = logit_to_prob(expected_value + positive_sum)
        baseline_plus_negative = logit_to_prob(expected_value + negative_sum)
        
        print(f"\n🎯 PROBABILITY INTERPRETATION:")
        print(f"  Starting point (baseline): {expected_value_proba:.1%}")
        print(f"  After positive features:   {baseline_plus_positive:.1%} ({baseline_plus_positive-expected_value_proba:+.1%})")
        print(f"  After negative features:   {baseline_plus_negative:.1%} ({baseline_plus_negative-expected_value_proba:+.1%})")
        print(f"  Final prediction:          {prediction_proba:.1%}")
        
        return {
            'explanation_df': explanation_df,
            'shap_result': shap_result,
            'prediction_proba': prediction_proba,
            'model_prediction_logit': model_prediction_logit,
            'expected_value': expected_value,
            'expected_value_proba': expected_value_proba,
            'verification_ok': verification_ok,
            'positive_sum': positive_sum,
            'negative_sum': negative_sum
        }
        
    except Exception as e:
        print(f"❌ Error in SHAP calculation: {e}")
        return None

def create_advanced_visualizations(explanation_result, sample_index=0):
    """Create advanced SHAP visualizations"""
    
    if explanation_result is None:
        print("❌ No explanation data to visualize")
        return
    
    explanation_df = explanation_result['explanation_df']
    prediction_proba = explanation_result['prediction_proba']
    expected_value_proba = explanation_result['expected_value_proba']
    
    # Set up the plot style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # 1. Feature Contribution Bar Chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Top 10 features by absolute SHAP value
    top_features = explanation_df.head(10).copy()
    
    # Create colors
    colors = ['darkgreen' if x > 0 else 'darkred' for x in top_features['SHAP_Value_Logit']]
    
    # Create horizontal bars
    bars = ax1.barh(range(len(top_features)), top_features['SHAP_Value_Logit'],
                    color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    # Set labels
    ax1.set_yticks(range(len(top_features)))
    ax1.set_yticklabels(top_features['Feature'], fontsize=11)
    ax1.set_xlabel('SHAP Value (Log-odds)', fontsize=12)
    ax1.set_title(f'Top 10 Feature Contributions (Sample #{sample_index})\nSHAP Values in Log-odds Space',
                  fontsize=14, pad=20)
    ax1.axvline(x=0, color='black', linestyle='-', alpha=0.5, linewidth=1)
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Add percentage labels
    for i, (bar, row) in enumerate(zip(bars, top_features.itertuples())):
        width = bar.get_width()
        pct_label = f"{row.Contribution_Pct:+.1f}%"
        
        if abs(width) > 0.01:  # Only show label if bar is large enough
            x_pos = width + (0.005 if width > 0 else -0.005)
            ha = 'left' if width > 0 else 'right'
            
            ax1.text(x_pos, bar.get_y() + bar.get_height()/2, pct_label,
                    ha=ha, va='center', fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
    
    # 2. Probability Journey Visualization
    # Calculate step-by-step probability changes
    cumulative_logit = explanation_result['expected_value']
    waterfall_data = []
    
    # Starting point (baseline)
    waterfall_data.append({
        'name': 'Baseline',
        'prob': expected_value_proba,
        'cumulative_prob': expected_value_proba,
        'color': 'gray'
    })
    
    # Add top 6 features
    top_6_features = explanation_df.head(6)
    for _, row in top_6_features.iterrows():
        old_prob = logit_to_prob(cumulative_logit)
        cumulative_logit += row['SHAP_Value_Logit']
        new_prob = logit_to_prob(cumulative_logit)
        
        waterfall_data.append({
            'name': row['Feature'][:12],
            'prob': new_prob,
            'cumulative_prob': new_prob,
            'color': 'darkgreen' if row['SHAP_Value_Logit'] > 0 else 'darkred'
        })
    
    # Final result
    waterfall_data.append({
        'name': 'Final',
        'prob': prediction_proba,
        'cumulative_prob': prediction_proba,
        'color': 'darkblue'
    })
    
    # Create probability journey plot
    x_positions = np.arange(len(waterfall_data))
    probabilities = [d['prob'] for d in waterfall_data]
    colors = [d['color'] for d in waterfall_data]
    
    # Line plot connecting probabilities
    ax2.plot(x_positions, probabilities, 'ko-', linewidth=2, markersize=8, alpha=0.7)
    
    # Bar chart showing final probabilities
    bars2 = ax2.bar(x_positions, probabilities, color=colors, alpha=0.6, width=0.6)
    
    # Add labels
    for i, (bar, data) in enumerate(zip(bars2, waterfall_data)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{height:.1%}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    ax2.set_title(f'Probability Journey: Baseline → Final Prediction\nStep-by-step probability changes',
                  fontsize=14, pad=20)
    ax2.set_xlabel('Components', fontsize=12)
    ax2.set_ylabel('Probability of Approval', fontsize=12)
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels([d['name'] for d in waterfall_data], rotation=45, ha='right')
    ax2.set_ylim(0, 1)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    return fig

def run_advanced_analysis():
    """Run advanced SHAP analysis with your existing models"""
    
    print("🚀 STARTING ADVANCED SHAP ANALYSIS")
    print("="*60)
    
    # Load your existing model
    try:
        loader = load_models('.')
        print("✅ Models loaded successfully")
        
        # Check if SHAP explainer exists
        if not hasattr(loader, 'shap_explainer') or loader.shap_explainer is None:
            print("🔧 Creating SHAP explainer...")
            success = loader.create_custom_shap_explainer(background_size=100)
            if not success:
                print("❌ Failed to create SHAP explainer")
                return
        
        # Generate sample data for analysis
        print("\n📊 Generating sample data...")
        sample_data = loader.generate_sample_data(1)
        
        print(f"Sample data shape: {sample_data.shape}")
        print(f"Sample values: {sample_data.values[0]}")
        
        # Run advanced explanation
        print("\n🔍 Running advanced SHAP explanation...")
        explanation_result = explain_local_prediction_advanced(sample_data.values, loader)
        
        if explanation_result:
            print("\n📊 Creating visualizations...")
            fig = create_advanced_visualizations(explanation_result, sample_index=1)
            
            print("\n✅ Advanced SHAP analysis completed!")
            print(f"🎯 Final recommendation: {'APPROVE' if explanation_result['prediction_proba'] > 0.5 else 'REJECT'}")
            print(f"📈 Confidence: {max(explanation_result['prediction_proba'], 1-explanation_result['prediction_proba']):.1%}")
            
        else:
            print("❌ Advanced explanation failed")
            
    except Exception as e:
        print(f"❌ Error in advanced analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Run the advanced analysis
    run_advanced_analysis()
    
    print("\n" + "="*60)
    print("🎯 USAGE INSTRUCTIONS:")
    print("1. run_advanced_analysis() - Complete analysis with your data")
    print("2. explain_local_prediction_advanced(sample_data, loader) - Analyze specific sample")
    print("3. create_advanced_visualizations(result) - Create charts")
    print("="*60)