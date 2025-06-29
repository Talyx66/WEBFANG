import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def run(target):
    print(f"[*] Running spider on {target}")
    visited = set()
    to_visit = set([f"http://{target}", f"https://{target}"])

    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        try:
            resp = requests.get(url, timeout=5)
            visited.add(url)
            print(f"Visited: {url} (Status: {resp.status_code})")

            soup = BeautifulSoup(resp.text, "html.parser")
            for link in soup.find_all("a", href=True):
                href = link['href']
                joined = urljoin(url, href)
                parsed = urlparse(joined)
                # Stay within the domain
                if parsed.netloc == urlparse(url).netloc:
                    if joined not in visited:
                        to_visit.add(joined)
        except Exception as e:
            print(f"[!] Error visiting {url}: {e}")
