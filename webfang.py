import argparse
from modules import spider, headers, whois_lookup, dnsdumpster, shodan_lookup, urlscan

import re  # add this line here

def detect_target_type(target):
    if re.match(r"[^@]+@[^@]+\.[^@]+", target):
        return "email"
    elif re.match(r"^[0-9a-zA-Z_.-]+$", target) and "." not in target:
        return "username"
    elif re.match(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", target):
        return "ip"
    elif "." in target:
        return "domain"
    else:
        return "unknown"

parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True)
parser.add_argument("--spider", action="store_true")
parser.add_argument("--headers", action="store_true")
parser.add_argument("--whois", action="store_true")
parser.add_argument("--dns", action="store_true")
parser.add_argument("--shodan", action="store_true")
parser.add_argument("--urlscan", action="store_true")
args = parser.parse_args()

target_type = detect_target_type(args.target)

if args.spider or target_type == "domain":
    spider.run(args.target)
if args.headers or target_type == "domain":
    headers.run(args.target)
if args.whois or target_type == "domain":
    whois_lookup.run(args.target)
if args.dns or target_type == "domain":
    dnsdumpster.run(args.target)
if args.shodan or target_type == "domain" or target_type == "ip":
    shodan_lookup.run(args.target)
if args.urlscan or target_type == "domain":
    urlscan.run(args.target)
if target_type == "email":
    print("[*] Detected email target")
    # Call your email-related modules here
elif target_type == "username":
    print("[*] Detected username target")
    # Call username-related modules here (if any)
elif target_type == "domain":
    print("[*] Detected domain target")
    spider.run(args.target)
    whois_lookup.run(args.target)
    dnsdumpster.run(args.target)
    shodan_lookup.run(args.target)
    urlscan.run(args.target)
elif target_type == "ip":
    print("[*] Detected IP target")
    shodan_lookup.run(args.target)
else:
    print("[-] Unknown target type. Please specify manually.")
