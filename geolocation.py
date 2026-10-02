#!/usr/bin/env python3
import sys
import json
import urllib.request
import urllib.error

# ANSI Color Codes for Styling
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Custom CTF607 Banner
BANNER = f"""{CYAN}{BOLD}
   ____ _____ _____   __    ___ _____ 
  / ___|_   _|  ___| / /_  / _ \\___  |
 | |     | | | |_   | '_ \\| | | | / / 
 | |___  | | |  _|  | (_) | |_| |/ /  
  \\____| |_| |_|     \\___/ \\___//_/   
{RESET}{YELLOW}       [ IP Geolocation Tracker ]{RESET}
"""

def fetch_geolocation(target_ip=""):
    """
    Fetches geolocation details for the specified IP address.
    If no IP is passed, ip-api.com defaults to the caller's public IP.
    """
    fields = "status,message,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,query"
    url = f"http://ip-api.com/json/{target_ip}?fields={fields}"
    
    req = urllib.request.Request(
        url, 
        headers={"User-Agent": "CTF607-Tracker/1.0"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            payload = response.read().decode('utf-8')
            data = json.loads(payload)

        if data.get("status") != "success":
            print(f"{RED}[-] Query Failed: {data.get('message', 'Invalid IP address')}{RESET}")
            return

        # Output formatting
        print(f"{GREEN}{BOLD}[+] INTELLIGENCE RECOVERED FOR {data.get('query')}:{RESET}\n")
        
        details = [
            ("IP Address", data.get("query")),
            ("Country", f"{data.get('country')} ({data.get('countryCode')})"),
            ("Region", data.get("regionName")),
            ("City", data.get("city")),
            ("Postal Code", data.get("zip")),
            ("Coordinates", f"{data.get('lat')}, {data.get('lon')}"),
            ("Timezone", data.get("timezone")),
            ("ISP / Provider", data.get("isp")),
            ("Organization", data.get("org"))
        ]

        for label, val in details:
            print(f"  {BOLD}{label:<15}:{RESET} {val}")

        # Direct Google Maps Link
        maps_link = f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}"
        print(f"\n  {CYAN}{BOLD}Map Location  :{RESET} {maps_link}\n")

    except urllib.error.URLError as err:
        print(f"{RED}[!] Network connection error: {err.reason}{RESET}")
    except Exception as err:
        print(f"{RED}[!] Unexpected error: {err}{RESET}")

def main():
    print(BANNER)
    # Parse CLI argument if provided
    ip_address = sys.argv[1] if len(sys.argv) > 1 else ""
    fetch_geolocation(ip_address)

if __name__ == "__main__":
    main()