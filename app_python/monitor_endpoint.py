"""
Monitor GPT-OSS endpoint until it's ready
"""
import requests
import time
import sys
import json

def monitor_endpoint(url, interval=10, max_attempts=30):
    """Monitor endpoint until it responds or timeout"""
    print(f"🔍 MONITORING ENDPOINT")
    print(f"URL: {url}")
    print(f"Check interval: {interval}s")
    print(f"Max attempts: {max_attempts}")
    print("=" * 50)
    
    test_data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ]
    }
    
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Attempt {attempt}/{max_attempts}: ", end="", flush=True)
            
            response = requests.post(
                url,
                json=test_data,
                headers={
                    "Content-Type": "application/json",
                    "ngrok-skip-browser-warning": "true"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print("✅ SUCCESS!")
                    print(f"\n🎉 ENDPOINT IS READY!")
                    print(f"• URL: {url}")
                    print(f"• Status: Working")
                    print(f"• Response keys: {list(result.keys())}")
                    
                    if "generated_text" in result:
                        print(f"• Sample response: {result['generated_text'][:100]}...")
                    
                    print(f"\n🚀 YOUR APP IS READY!")
                    print(f"• Streamlit: http://localhost:8501")
                    print(f"• GPT-OSS: Will now work automatically")
                    print(f"• No restart needed - just refresh the page")
                    
                    return True
                    
                except json.JSONDecodeError:
                    print("✅ Working (non-JSON response)")
                    return True
                    
            elif response.status_code == 404:
                print("❌ 404 (Not Found)")
            elif response.status_code == 500:
                print("❌ 500 (Server Error)")
            else:
                print(f"❌ {response.status_code}")
                
        except requests.exceptions.Timeout:
            print("⏰ Timeout")
        except requests.exceptions.ConnectionError:
            print("🌐 Connection Error")
        except Exception as e:
            print(f"💥 {e}")
        
        if attempt < max_attempts:
            print(f"   Waiting {interval}s...")
            time.sleep(interval)
    
    print(f"\n❌ TIMEOUT after {max_attempts} attempts")
    print(f"💡 Your GPT-OSS server may need more time to start")
    print(f"💡 App still works with template fallback")
    return False

if __name__ == "__main__":
    url = "https://14bea30668ae.ngrok-free.app/generate"
    
    print("👀 GPT-OSS ENDPOINT MONITOR")
    print("=" * 40)
    print("🎯 Waiting for your GPT-OSS server to be ready...")
    print("⏹️  Press Ctrl+C to stop monitoring")
    print("")
    
    try:
        success = monitor_endpoint(url, interval=10, max_attempts=20)
        
        if not success:
            print(f"\n💡 Manual check:")
            print(f"python test_endpoint.py {url}")
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Monitoring stopped by user")
        print(f"💡 Run again: python monitor_endpoint.py")