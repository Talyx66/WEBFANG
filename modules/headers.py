import requests

COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': '*/*'
}

def scan(target):
    output = []
    if not target:
        return ["[!] No target provided."]
    output.append(f"[*] Fetching HTTP headers from {target}")
    try:
        if not target.startswith("http"):
            target = "http://" + target
        resp = requests.get(target, headers=COMMON_HEADERS, timeout=5)
        output.append(f"[+] Status Code: {resp.status_code}")
        output.append(f"[+] Content-Type: {resp.headers.get('Content-Type')}")
        output.append(f"[+] Server: {resp.headers.get('Server', 'N/A')}")
        output.append(f"[+] X-Powered-By: {resp.headers.get('X-Powered-By', 'N/A')}")
        for h,v in resp.headers.items():
            output.append(f" - {h}: {v}")
    except Exception as e:
        output.append(f"[!] Headers scan failed: {e}")
    return output
