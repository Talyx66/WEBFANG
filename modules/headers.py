import requests

def scan(target):
    print(f"[*] Running headers lookup on {target}")
    try:
        # Ensure URL scheme
        if not target.startswith(('http://', 'https://')):
            url = 'http://' + target
        else:
            url = target
        
        response = requests.get(url, timeout=10)
        print(f"HTTP Status Code: {response.status_code}")
        print("Response Headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")
    except requests.RequestException as e:
        print(f"[!] Failed to fetch headers: {e}")
