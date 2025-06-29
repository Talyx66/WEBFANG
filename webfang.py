import argparse
from modules import spider, headers, whois_lookup, dnsdumpster, shodan_lookup, urlscan

parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True)
parser.add_argument("--spider", action="store_true")
parser.add_argument("--headers", action="store_true")
parser.add_argument("--whois", action="store_true")
parser.add_argument("--dns", action="store_true")
parser.add_argument("--shodan", action="store_true")
parser.add_argument("--urlscan", action="store_true")
args = parser.parse_args()

if args.spider:
    spider.run(args.target)
if args.headers:
    headers.run(args.target)
if args.whois:
    whois_lookup.run(args.target)
if args.dns:
    dnsdumpster.run(args.target)
if args.shodan:
    shodan_lookup.run(args.target)
if args.urlscan:
    urlscan.run(args.target)
