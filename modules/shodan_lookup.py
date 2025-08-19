import shodan
import socket

API_KEY = "YOUR_SHODAN_API_KEY"

def shodan_lookup(target):
    output = []
    if not target:
        return ["[!] No target provided."]
    output.append(f"[*] Running Shodan lookup on {target}")
    try:
        api = shodan.Shodan(API_KEY)
        ip = socket.gethostbyname(target)
        results = api.host(ip)
        output.append(f"[+] IP: {results.get('ip_str', 'N/A')}")
        output.append(f"[+] Organization: {results.get('org', 'N/A')}")
        output.append(f"[+] OS: {results.get('os', 'N/A')}")
        output.append(f"[+] Hostnames: {results.get('hostnames')}")
        output.append("Open Ports and Services:")
        for item in results.get('data', []):
            output.append(f" - Port {item.get('port')}: {item.get('product', 'N/A')} ({item.get('transport')})")
            if item.get('ssl', None):
                output.append(f"   SSL: {item['ssl'].get('versions', 'N/A')}")
    except shodan.APIError as e:
        output.append(f"[!] Shodan API error: {e}")
    except Exception as e:
        output.append(f"[!] Shodan lookup failed: {e}")
    return output