"""
Fix Streamlit deprecated use_container_width warnings
"""
import re

def fix_streamlit_warnings():
    """Replace use_container_width with width parameter"""
    
    print("🔧 FIXING STREAMLIT WARNINGS")
    print("=" * 40)
    
    try:
        # Read the file
        with open("simple_demo.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Count occurrences before
        before_count = content.count("use_container_width=True")
        print(f"📊 Found {before_count} instances of use_container_width=True")
        
        # Replace patterns
        replacements = [
            # For buttons and other components
            (r'use_container_width=True', 'width="stretch"'),
            (r'use_container_width=False', 'width="content"'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Write back
        with open("simple_demo.py", "w", encoding="utf-8") as f:
            f.write(content)
        
        # Count after
        after_count = content.count('width="stretch"')
        print(f"✅ Replaced with {after_count} instances of width='stretch'")
        print(f"✅ Fixed deprecated Streamlit warnings")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_api_endpoint_status():
    """Check current API endpoint status"""
    print(f"\n🔍 CHECKING API ENDPOINT STATUS")
    print("=" * 40)
    
    import requests
    
    endpoint = "https://0f232a329a29.ngrok-free.app/generate"
    
    try:
        print(f"Testing: {endpoint}")
        response = requests.post(
            endpoint,
            json={"messages": [{"role": "user", "content": "test"}]},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Endpoint is working!")
            return True
        elif response.status_code == 404:
            print("❌ Endpoint not found (404)")
            print("💡 Ngrok tunnel may have expired")
            return False
        else:
            print(f"⚠️ Status: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - server slow or not responding")
        return False
    except Exception as e:
        print(f"💥 Error: {e}")
        return False

if __name__ == "__main__":
    print("🛠️ FIXING STREAMLIT APP ISSUES")
    print("=" * 50)
    
    # Fix 1: Streamlit warnings
    streamlit_fixed = fix_streamlit_warnings()
    
    # Check 2: API endpoint status
    api_working = check_api_endpoint_status()
    
    print(f"\n📊 SUMMARY:")
    print(f"• Streamlit warnings: {'✅ Fixed' if streamlit_fixed else '❌ Failed'}")
    print(f"• API endpoint: {'✅ Working' if api_working else '❌ Offline'}")
    
    print(f"\n🚀 RECOMMENDATIONS:")
    if streamlit_fixed:
        print(f"✅ Streamlit warnings fixed - restart app to see clean output")
    
    if not api_working:
        print(f"💡 API endpoint offline - app will use template fallback (works great!)")
        print(f"💡 When you have new ngrok URL, run: python quick_test.py")
    
    print(f"\n🔄 Restart Streamlit: python -m streamlit run simple_demo.py")