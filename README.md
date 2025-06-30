WEBFANG
This is my very first Command-line interface tool created. Please leave reviews, and Happy Hunting

  
**WebFang** is an OSINT + Reconnaissance toolkit for ethical hackers and red teamers.
It performs passive and active recon using spidering, WHOIS, DNS, Shodan, and header fingerprinting.

![screenshot 1](WEBFANG%20Screenshots/WEBFANG1.png)

![screenshot 2](WEBFANG%20Screenshots/WEBFANG2.png)

![screenshot 3](WEBFANG%20Screenshots/WEBFANG3.png)

![screenshot 4](WEBFANG%20Screenshots/webfang11.png)

Features:
-Web Spider
-DNS & WHOIS Lookup
-Shodan & URLScan Integration  (Get your API key from Shodan.io)
-Header fingerprinting
-Modular and extensible

Usage
```bash
python3 webfang.py --target example.com --spider --dns --whois --headers --shodan
```

Setup
```bash
git clone https://github.com/Talyx66/WEBFANG.git
cd WebFang
chmod +x setup.sh
./setup.sh
```
