import requests
import time

API_KEY = "YOUR_URLSCAN_API_KEY"  # Replace with your actual API key

headers = {
    "API-Key": API_KEY,
    "Content-Type": "application/json"
}

def run(target):
    print(f"[*] Running URLScan on {target}")
    
    data = {
        "url": f"http://{target}",
        "visibility": "public"
    }

    try:
        # Submit scan
        response = requests.post("https://urlscan.io/api/v1/scan/", headers=headers, json=data)
        if response.status_code != 200:
            print(f"[!] URLScan submission failed: {response.status_code} {response.text}")
            return

        result = response.json()
        uuid = result.get("uuid")
        if not uuid:
            print("[!] No UUID returned from URLScan")
            return

        print(f"[*] Submitted. UUID: {uuid}")
        print("[*] Waiting 15 seconds for scan to complete...")
        time.sleep(15)

        # Fetch results
        result_url = f"https://urlscan.io/api/v1/result/{uuid}/"
        result_resp = requests.get(result_url)
        if result_resp.status_code == 200:
            result_data = result_resp.json()
            print("[*] URLScan Result Summary:")
            print(" - Page Title:", result_data.get("page", {}).get("title"))
            print(" - IP Address:", result_data.get("page", {}).get("ip"))
            print(" - ASN:", result_data.get("page", {}).get("asnname"))
            print(" - Domain:", result_data.get("page", {}).get("domain"))
            print(" - URL:", result_data.get("page", {}).get("url"))
        else:
            print(f"[!] Failed to fetch URLScan result: {result_resp.status_code}")
    except Exception as e:
        print(f"[!] URLScan error: {e}")
