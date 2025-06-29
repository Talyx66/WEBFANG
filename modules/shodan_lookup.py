import shodan

API_KEY = "YOUR_SHODAN_API_KEY"  # Replace with your Shodan API key

def run(target):
    print(f"[*] Running Shodan lookup on {target}")
    try:
        api = shodan.Shodan(API_KEY)
        results = api.host(target)
        print(f"IP: {results.get('ip_str')}")
        print(f"Organization: {results.get('org')}")
        print(f"Operating System: {results.get('os')}")
        print("Ports:")
        for item in results.get('data', []):
            print(f" - {item.get('port')}: {item.get('product')}")
    except shodan.APIError as e:
        print(f"[!] Shodan API error: {e}")
    except Exception as e:
        print(f"[!] Shodan lookup failed: {e}")
