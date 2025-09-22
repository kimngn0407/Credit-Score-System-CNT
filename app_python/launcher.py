# -*- coding: utf-8 -*-
"""
Quick test and launch script for the AI Model Visualization Dashboard
"""

def test_models():
    """Test if models can be loaded successfully"""
    print("Testing model loading...")
    
    try:
        from model_loader import load_models
        
        loader = load_models(".")
        
        # Test LORA Adapter
        adapter_info = loader.get_adapter_summary()
        if "error" not in adapter_info:
            print("LORA Adapter loaded successfully")
            print(f"   - Base Model: {adapter_info.get('Base Model', 'N/A')}")
            print(f"   - LoRA Rank: {adapter_info.get('LoRA Rank (r)', 0)}")
        else:
            print("LORA Adapter failed to load")
            
        # Test LightGBM Model
        lgb_info = loader.get_lightgbm_summary()
        if "error" not in lgb_info:
            print("LightGBM Model loaded successfully")
            print(f"   - Trees: {lgb_info.get('Number of Trees', 0)}")
            print(f"   - Features: {lgb_info.get('Number of Features', 0)}")
        else:
            print("LightGBM Model failed to load")
            
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

def launch_app():
    """Launch the Streamlit application"""
    import subprocess
    import sys
    import os
    
    print("\nLaunching Streamlit Dashboard...")
    print("Dashboard will open at: http://localhost:8501")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Get the Python executable path
        python_exe = sys.executable
        
        # Run streamlit
        subprocess.run([
            python_exe, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error launching dashboard: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("AI Model Visualization Dashboard")
    print("=" * 60)
    
    # Test models first
    if test_models():
        print("\nAll models loaded successfully!")
        
        # Ask user if they want to launch
        launch = input("\nLaunch dashboard now? (y/n): ").lower().strip()
        
        if launch in ['y', 'yes', '']:
            launch_app()
        else:
            print("You can launch the dashboard later by running:")
            print("   python launcher.py")
            print("   or")
            print("   streamlit run app.py")
    else:
        print("\nSome models failed to load. Check the error messages above.")
        print("Make sure all model files are in the correct location:")
        print("   - adapter_config.json")
        print("   - adapter_model.safetensors") 
        print("   - lightgbm_model.txt")