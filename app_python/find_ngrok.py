"""
Auto-detect running ngrok tunnels
"""
import requests
import json

def find_ngrok_tunnels():
    """Try to find running ngrok tunnels"""
    print("🔍 SEARCHING FOR NGROK TUNNELS")
    print("=" * 40)
    
    try:
        # Ngrok API endpoint (local)
        response = requests.get("http://localhost:4040/api/tunnels", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            tunnels = data.get('tunnels', [])
            
            if tunnels:
                print(f"✅ Found {len(tunnels)} ngrok tunnel(s):")
                
                for i, tunnel in enumerate(tunnels, 1):
                    public_url = tunnel.get('public_url', '')
                    config = tunnel.get('config', {})
                    addr = config.get('addr', '')
                    
                    print(f"\n{i}. {public_url}")
                    print(f"   → {addr}")
                    
                    # If it's HTTPS, suggest as GPT-OSS endpoint
                    if public_url.startswith('https://'):
                        suggested_url = f"{public_url}/generate"
                        print(f"   🎯 Suggested GPT-OSS: {suggested_url}")
                        
                        # Auto-test this endpoint
                        print(f"   🧪 Testing...")
                        test_result = quick_test_endpoint(suggested_url)
                        if test_result:
                            return suggested_url
                
                return tunnels[0].get('public_url', '') + '/generate'
            else:
                print("❌ No tunnels found")
                return None
        else:
            print("❌ Ngrok API not accessible")
            return None
            
    except Exception as e:
        print(f"💥 Error: {e}")
        print("💡 Make sure ngrok is running with web interface on port 4040")
        return None

def quick_test_endpoint(url):
    """Quick test without verbose output"""
    try:
        response = requests.post(
            url,
            json={"messages": [{"role": "user", "content": "test"}]},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"   ✅ Working!")
            return True
        else:
            print(f"   ❌ Status: {response.status_code}")
            return False
    except:
        print(f"   ❌ Not responding")
        return False

def main():
    """Main function"""
    suggested_url = find_ngrok_tunnels()
    
    if suggested_url:
        print(f"\n🎯 RECOMMENDED ACTION:")
        print(f"python endpoint_manager.py --update {suggested_url}")
    else:
        print(f"\n💡 MANUAL CHECK:")
        print(f"1. Check your ngrok terminal for the https:// URL")
        print(f"2. Test with: python test_endpoint.py https://your-url.ngrok-free.app/generate")
        print(f"3. Update with: python endpoint_manager.py --update https://your-url.ngrok-free.app/generate")

if __name__ == "__main__":
    main()