# modules/urlscan.py
import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Replace with your actual URLScan API key
API_KEY = "YOUR_URLSCAN_API_KEY"

HEADERS = {
    "API-Key": API_KEY,
    "Content-Type": "application/json"
}

def fast_scan(target):
    """Fast HTTP scan for immediate feedback."""
    print(f"[*] Running fast scan on {target}")
    results = []
    try:
        url = f"http://{target}"
        resp = requests.get(url, timeout=10)
        results.append(f"[+] Status Code: {resp.status_code}")
        results.append(f"[+] Content Length: {len(resp.text)}")
        results.append(f"[+] Server: {resp.headers.get('Server', 'Unknown')}")
        results.append(f"[+] Content-Type: {resp.headers.get('Content-Type', 'Unknown')}")
    except requests.RequestException as e:
        results.append(f"[!] Fast scan failed: {e}")
    return results

def api_scan(target):
    """Advanced scan using URLScan API asynchronously."""
    print(f"[*] Running URLScan API on {target}")
    results = []
    data = {"url": f"http://{target}", "visibility": "public"}

    try:
        # Submit scan
        response = requests.post("https://urlscan.io/api/v1/scan/", headers=HEADERS, json=data)
        if response.status_code != 200:
            results.append(f"[!] URLScan submission failed: {response.status_code} {response.text}")
            return results

        uuid = response.json().get("uuid")
        if not uuid:
            results.append("[!] No UUID returned from URLScan")
            return results

        results.append(f"[*] Submitted. UUID: {uuid}")
        results.append("[*] Waiting 15 seconds for scan to complete...")
        time.sleep(15)

        # Fetch results
        result_url = f"https://urlscan.io/api/v1/result/{uuid}/"
        result_resp = requests.get(result_url)
        if result_resp.status_code == 200:
            result_data = result_resp.json()
            page = result_data.get("page", {})
            results.append(f"[+] Page Title: {page.get('title', 'N/A')}")
            results.append(f"[+] IP Address: {page.get('ip', 'N/A')}")
            results.append(f"[+] ASN: {page.get('asnname', 'N/A')}")
            results.append(f"[+] Domain: {page.get('domain', 'N/A')}")
            results.append(f"[+] URL: {page.get('url', 'N/A')}")
        else:
            results.append(f"[!] Failed to fetch URLScan result: {result_resp.status_code}")
    except Exception as e:
        results.append(f"[!] URLScan API error: {e}")

    return results

def scan(target, mode="fast"):
    """Unified function for GUI integration."""
    if mode == "fast":
        return fast_scan(target)
    elif mode == "api":
        # Run API scan in thread for async behavior
        with ThreadPoolExecutor() as executor:
            future = executor.submit(api_scan, target)
            return future.result()
    else:
        return [f"[!] Unknown scan mode: {mode}"]
