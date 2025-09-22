"""
Simple test for ngrok endpoint
"""
import requests

def simple_test():
    """Simple test with basic request"""
    url = "https://0f232a329a29.ngrok-free.app/generate"
    
    print(f"🧪 SIMPLE TEST")
    print(f"URL: {url}")
    print("=" * 40)
    
    # Very simple test data
    simple_data = {
        "messages": [
            {
                "role": "user",
                "content": "Hello"
            }
        ]
    }
    
    try:
        print("📤 Testing with simple request...")
        response = requests.post(
            url,
            json=simple_data,
            headers={
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response: {response.text[:300]}...")
        
        if response.status_code == 200:
            print("✅ Basic connection works!")
            return True
        else:
            print("⚠️ Got response but not 200")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Timeout - server may be slow")
        return False
    except Exception as e:
        print(f"💥 Error: {e}")
        return False

def test_with_ngrok_headers():
    """Test with ngrok-specific headers"""
    url = "https://0f232a329a29.ngrok-free.app/generate"
    
    print(f"\n🔧 TESTING WITH NGROK HEADERS")
    print("=" * 40)
    
    simple_data = {
        "messages": [
            {
                "role": "user",
                "content": "Test"
            }
        ]
    }
    
    # Add ngrok warning bypass header
    headers = {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true",
        "User-Agent": "LoanApp/1.0"
    }
    
    try:
        print("📤 Testing with ngrok headers...")
        response = requests.post(
            url,
            json=simple_data,
            headers=headers,
            timeout=15
        )
        
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response preview: {response.text[:200]}...")
        
        if response.status_code == 200:
            print("✅ Works with ngrok headers!")
            return True
        else:
            print("⚠️ Still not working")
            return False
            
    except Exception as e:
        print(f"💥 Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTING NEW NGROK ENDPOINT")
    print("=" * 50)
    
    # Test 1: Simple
    simple_works = simple_test()
    
    # Test 2: With headers
    header_works = test_with_ngrok_headers()
    
    print("\n" + "=" * 50)
    print("📋 RESULTS:")
    
    if simple_works or header_works:
        print("✅ Endpoint is reachable!")
        print("🔄 Will update the app configuration")
    else:
        print("❌ Endpoint not responding")
        print("💡 Possible issues:")
        print("  • Server is starting up")
        print("  • Wrong endpoint path")
        print("  • Server needs different request format")
        print("  • Ngrok tunnel is inactive")
    
    print(f"\n📱 Your app is still working with template fallback")
    print(f"🔄 Run: python -m streamlit run simple_demo.py")