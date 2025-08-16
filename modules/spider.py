import requests
from bs4 import BeautifulSoup
import tldextract

def subdomain_enum(domain):
    output = [f"[*] Enumerating subdomains for {domain}"]
    try:
        # This is a placeholder. Real brute force + API integration recommended.
        subdomains = ["www", "mail", "dev", "test"]
        for sub in subdomains:
            output.append(f"[+] {sub}.{domain}")
    except Exception as e:
        output.append(f"[!] Subdomain enumeration failed: {e}")
    return output

def crawl(url):
    output = [f"[*] Crawling {url}"]
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        links = set()
        for a in soup.find_all("a", href=True):
            links.add(a['href'])
        output.append(f"[+] Found {len(links)} links.")
        for link in list(links)[:20]:
            output.append(f"    - {link}")
    except Exception as e:
        output.append(f"[!] Spider crawl failed: {e}")
    return output
