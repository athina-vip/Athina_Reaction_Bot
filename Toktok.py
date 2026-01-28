import requests
import threading
import random
import time
import sys
import os
import concurrent.futures
import urllib3

# SSL Warning တွေကို ပိတ်ထားခြင်း (Network Error မတက်အောင်)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- PREMIUM ANSI COLORS ---
R = '\033[1;31m'
G = '\033[1;32m'
Y = '\033[1;33m'
B = '\033[1;34m'
C = '\033[1;36m'
W = '\033[1;37m'
P = '\033[1;35m'
BC = '\033[1m'
ST = '\033[0m'

# --- GITHUB PROXY URL ---
PROXY_URL = "https://raw.githubusercontent.com/athina-vip/Athina_Reaction_Bot/main/Proxy.txt"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear()
    banner = f"""
{C}  ╔══════════════════════════════════════════════════════════════╗
  ║{Y}  █████╗ ████████╗██╗  ██╗██╗███╗   ██╗ █████╗  {P} [ ATHINA# ]  {C}║
  ║{Y} ██╔══██╗╚══██╔══╝██║  ██║██║████╗  ██║██╔══██╗ {P} [   V1.0  ]  {C}║
  ║{Y} ███████║   ██║   ███████║██║██╔██╗ ██║███████║ {P} [   BETA  ]  {C}║
  ║{Y} ██╔══██║   ██║   ██╔══██║██║██║╚██╗██║██╔══██║ {P} [  STRONG ]  {C}║
  ║{Y} ██║  ██║   ██║   ██║  ██║██║██║ ╚████║██║  ██║ {P} [  ACTIVE ]  {C}║
  ╠══════════════════════════════════════════════════════════════╣
  ║{W}             ATHINA TIKTOK REPORT TOOL BETA                   {C}║
  ║{B}       AUTO-SYNC PROXY | BYPASS SECURITY | MULTI-THREAD       {C}║
  ╚══════════════════════════════════════════════════════════════╝{ST}
    """
    print(banner)

def loading_animation(text):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for _ in range(10):
        for char in chars:
            sys.stdout.write(f'\r  {BC}{P}[{char}] {W}{text}...{ST}')
            sys.stdout.flush()
            time.sleep(0.05)
    print(f"\n  {G}[√] {text} SUCCESS!{ST}")

def fetch_proxies():
    try:
        # SSL verify=False ထည့်ထားခြင်းဖြင့် Connection error ကိုကျော်လွှားသည်
        response = requests.get(PROXY_URL, timeout=20, verify=False)
        if response.status_code == 200:
            proxies = response.text.splitlines()
            return [p.strip() for p in proxies if p.strip()]
        else: return []
    except Exception as e:
        print(f"  {R}[!] Fetch Error: {e}{ST}")
        return []

def send_report(target_url, proxy, cookie, r_id):
    api = "https://www.tiktok.com/api/report/action/"
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/119.0.0.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) Safari/605.1.15"
        ]),
        "Cookie": cookie,
        "Referer": "https://www.tiktok.com/",
        "Accept": "application/json"
    }
    proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
    
    # Target ID ခွဲထုတ်ခြင်း
    target_id = target_url.split("/")[-1].split("?")[0].replace("@", "")
    
    data = {
        "object_id": target_id,
        "reason": random.choice([9001, 9010, 9007]),
        "target_url": target_url,
        "device_id": str(random.randint(6000000000000000000, 7999999999999999999)),
        "app_name": "tiktok_web"
    }

    try:
        res = requests.post(api, headers=headers, json=data, proxies=proxies, timeout=12, verify=False)
        if res.status_code == 200:
            print(f"  {G}[SUCCESS]{W} Report #{r_id:03} {C}» {W}{proxy[:18]:<18} {G}[SENT]{ST}")
        else:
            print(f"  {Y}[DENIED]{W}  Report #{r_id:03} {R}» {W}{proxy[:18]:<18} {R}[BLOCK]{ST}")
    except:
        pass

def main():
    print_banner()
    
    print(f"  {BC}{Y}┌──({W}Setup Configuration{Y})")
    target = input(f"  {Y}├──[>] {W}Target Account URL : {G}")
    cookie = input(f"  {Y}├──[>] {W}Your Session Cookie: {G}")
    threads_limit = int(input(f"  {Y}└──[>] {W}Thread Power (1-100): {G}"))

    print()
    loading_animation("SYNCHRONIZING PROXY DATABASE")
    proxies = fetch_proxies()

    if not proxies:
        print(f"  {R}[!] FATAL ERROR: Could not connect to Proxy. Please check internet.{ST}")
        return

    print(f"  {C}[i] Total Active Proxies: {W}{len(proxies)}{ST}")
    print(f"  {BC}{R}[!!!] INITIATING MASS ATTACK ON TARGET [!!!]{ST}\n")
    time.sleep(1)

    print(f"  {BC}{W}{'STATUS':<10} {'REPORT ID':<12} {'PROXY ADDRESS':<20}{ST}")
    print(f"  {C}──────────────────────────────────────────────────{ST}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads_limit) as executor:
        futures = [executor.submit(send_report, target, proxy, cookie, i+1) for i, proxy in enumerate(proxies)]
        concurrent.futures.wait(futures)

    print(f"\n  {BC}{G}╔════════════════════════════════════════════════╗")
    print(f"  ║ {W}   MASS REPORTING COMPLETED SUCCESSFULLY!      {G}║")
    print(f"  ╚════════════════════════════════════════════════╝{ST}\n")

if __name__ == "__main__":
    main()
