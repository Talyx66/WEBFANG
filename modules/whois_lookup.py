import whois

def run(target):
    output = []
    output.append(f"[*] Running WHOIS lookup on {target}")

    try:
        w = whois.whois(target)

        # Check if we got any data
        if not w or w.status is None:
            output.append("[-] No WHOIS data found.")
            return output

        # Iterate over key/value pairs
        for key, value in w.items():
            try:
                if value:
                    # Handle lists cleanly
                    val_str = ', '.join(value) if isinstance(value, list) else str(value)
                    output.append(f"[+] {key}: {val_str}")
                else:
                    output.append(f"[-] {key}: No data")
            except Exception as e:
                output.append(f"[!] Error reading {key}: {e}")

    except Exception as e:
        output.append(f"[!] WHOIS lookup failed: {e}")

    return output
