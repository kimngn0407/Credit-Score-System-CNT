"""
Quick URL updater for GPT-OSS endpoint
Usage: Just paste your new ngrok URL here and run
"""

def update_with_new_url():
    """Quick way to update endpoint URL"""
    
    print("🔧 QUICK ENDPOINT UPDATER")
    print("=" * 40)
    
    # ===== PASTE YOUR NEW NGROK URL HERE =====
    NEW_NGROK_URL = "https://14bea30668ae.ngrok-free.app"  # <-- CHANGE THIS
    # =========================================
    
    if "your-new-url" in NEW_NGROK_URL:
        print("❌ Please update NEW_NGROK_URL variable with your actual ngrok URL")
        print("")
        print("💡 Steps:")
        print("1. Check your ngrok terminal for the https:// URL")
        print("2. Edit this file and replace NEW_NGROK_URL")
        print("3. Run this script again")
        print("")
        print("Example:")
        print('NEW_NGROK_URL = "https://abc123def.ngrok-free.app"')
        return False
    
    # Add /generate if not present
    if not NEW_NGROK_URL.endswith("/generate"):
        NEW_NGROK_URL = NEW_NGROK_URL.rstrip("/") + "/generate"
    
    print(f"Testing: {NEW_NGROK_URL}")
    
    # Test the URL
    import requests
    try:
        response = requests.post(
            NEW_NGROK_URL,
            json={"messages": [{"role": "user", "content": "test"}]},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ URL is working!")
            
            # Update files
            import re
            
            files_to_update = ["model_loader.py", "simple_demo.py"]
            
            for filename in files_to_update:
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace old URLs with new one
                    old_patterns = [
                        r'https://[^"]*\.ngrok-free\.app[^"]*',
                        r'https://0f232a329a29\.ngrok-free\.app/generate'
                    ]
                    
                    for pattern in old_patterns:
                        content = re.sub(pattern, NEW_NGROK_URL, content)
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ Updated {filename}")
                    
                except Exception as e:
                    print(f"❌ Failed to update {filename}: {e}")
            
            print(f"\n🎉 SUCCESS!")
            print(f"• New endpoint: {NEW_NGROK_URL}")
            print(f"• Status: Working")
            print(f"• Files updated: model_loader.py, simple_demo.py")
            print(f"\n🚀 Restart Streamlit:")
            print(f"python -m streamlit run simple_demo.py")
            
            return True
            
        else:
            print(f"❌ URL returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"💥 Error testing URL: {e}")
        return False

if __name__ == "__main__":
    update_with_new_url()