import requests
from bs4 import BeautifulSoup

def run(target):
    print(f"[*] Running DNSDumpster on {target}")

    session = requests.Session()
    url = "https://dnsdumpster.com/"
    try:
        # Get CSRF token
        resp = session.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        csrf = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]

        # Post target domain
        headers = {
            "Referer": url,
            "User-Agent": "Mozilla/5.0"
        }
        data = {
            "csrfmiddlewaretoken": csrf,
            "targetip": target
        }
        resp = session.post(url, headers=headers, data=data)

        # Parse results
        soup = BeautifulSoup(resp.text, "html.parser")
        tables = soup.find_all("table")
        if not tables:
            print("[!] No results found or scraping blocked.")
            return

        # Example: print the first table text
        print("[*] DNSDumpster Results:")
        print(tables[0].get_text(separator="\n"))

    except Exception as e:
        print(f"[!] DNSDumpster lookup failed: {e}")
