import shodan

# Insert your Shodan API key here
API_KEY = "YOUR_SHODAN_API_KEY"

def shodan_lookup(target: str):
    """
    Perform a Shodan lookup on the given target (IP/host).
    Returns structured results or error message.
    """
    print(f"[*] Running Shodan lookup on {target}...")

    try:
        api = shodan.Shodan(API_KEY)
        results = api.host(target)

        output = []
        output.append(f"IP: {results.get('ip_str', 'N/A')}")
        output.append(f"Organization: {results.get('org', 'N/A')}")
        output.append(f"Operating System: {results.get('os', 'N/A')}")
        output.append("Ports:")

        for item in results.get('data', []):
            port = item.get('port')
            product = item.get('product') or "Unknown Service"
            output.append(f" - {port}: {product}")

        return "\n".join(output)

    except shodan.APIError as e:
        return f"[!] Shodan API error: {e}"
    except Exception as e:
        return f"[!] Shodan lookup failed: {e}"


if __name__ == "__main__":
    # Example standalone usage
    target_ip = "8.8.8.8"  # Replace with any IP for testing
    print(shodan_lookup(target_ip))

