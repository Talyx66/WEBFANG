import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

COMMON_SUBDOMAINS = ['www','mail','ftp','dev','api','ns1','ns2','admin','portal','beta','shop','blog','secure']

def subdomain_enum(target):
    output = []
    if not target:
        return ["[!] No target provided."]
    output.append(f"[*] Performing multi-threaded subdomain enumeration for {target}")
    def probe(sub):
        fqdn = f"{sub}.{target}"
        try:
            r = requests.get(f"http://{fqdn}", timeout=2)
            return f"[+] {fqdn} reachable"
        except:
            return f"[-] {fqdn} not reachable"
    try:
        with ThreadPoolExecutor(max_workers=15) as executor:
            results = executor.map(probe, COMMON_SUBDOMAINS)
        output.extend(results)
    except Exception as e:
        output.append(f"[!] Subdomain enumeration failed: {e}")
    return output

def crawl(target):
    output = []
    if not target:
        return ["[!] No target provided."]
    output.append(f"[*] Crawling {target} for all links and metadata")
    try:
        if not target.startswith("http"):
            target = "http://" + target
        resp = requests.get(target, timeout=5)
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a') if a.get('href')]
        images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
        output.append(f"[+] Found {len(links)} links and {len(images)} images")
        for link in links[:50]:  # limit output
            output.append(f" - Link: {link}")
        for img in images[:50]:
            output.append(f" - Image: {img}")
    except Exception as e:
        output.append(f"[!] Spider crawl failed: {e}")
    return output