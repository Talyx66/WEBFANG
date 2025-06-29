import whois

def run(target):
    print(f"[*] Running WHOIS lookup on {target}")
    try:
        w = whois.whois(target)
        for key, value in w.items():
            print(f"{key}: {value}")
    except Exception as e:
        print(f"[!] WHOIS lookup failed: {e}")
