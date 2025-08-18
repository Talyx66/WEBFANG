import whois
import socket
import datetime

def run(target):
    output = []
    if not target:
        return ["[!] No target provided."]
    output.append(f"[*] Running WHOIS lookup on {target}")
    try:
        w = whois.whois(target)
        for key, value in w.items():
            if isinstance(value, list):
                output.append(f"{key}: {', '.join(map(str, value))}")
            else:
                output.append(f"{key}: {value}")
        # Extra info
        try:
            ip = socket.gethostbyname(target)
            output.append(f"[+] Resolved IP: {ip}")
        except:
            output.append(f"[-] Could not resolve IP")
        output.append(f"[+] Lookup timestamp: {datetime.datetime.now()}")
    except Exception as e:
        output.append(f"[!] WHOIS lookup failed: {e}")
    return output
