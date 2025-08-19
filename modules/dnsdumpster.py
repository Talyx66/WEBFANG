import requests
from concurrent.futures import ThreadPoolExecutor

COMMON_SUBDOMAINS = [
    'www','mail','ftp','dev','api','ns1','ns2','admin','portal','beta','shop','blog','secure'
]

def probe_subdomain(sub, target):
    fqdn = f"{sub}.{target}"
    try:
        r = requests.get(f"http://{fqdn}", timeout=2)
        return f"[+] {fqdn} reachable"
    except:
        return f"[-] {fqdn} not reachable"

def dns_bruteforce(target):
    output = []
    if not target:
        return ["[!] No target provided."]
    output.append(f"[*] Running advanced DNS brute-force on {target}")
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(lambda sub: probe_subdomain(sub, target), COMMON_SUBDOMAINS)
        output.extend(results)
    except Exception as e:
        output.append(f"[!] DNS brute-force failed: {e}")
    return output