import os
import time
import sys
import uuid
import string
import random
import re
import time
from datetime import datetime, timezone
from os import system as sm
from sys import platform as pf
from time import sleep as sp
from colorama import init, Fore, Style
try:
    import requests
    import bs4
    import rich
    from rich import print as rp
    from rich.panel import Panel as pan
    from requests import get as gt
    from requests import post as pt
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    sm('python -m pip install requests bs4 rich')

# Colors
R = "[bold red]"
G = "[bold green]"
Y = "[bold yellow]"
B = "[bold blue]"
M = "[bold magenta]"
P = "[bold violet]"
C = "[bold cyan]"
W = "[bold white]"

r = "\033[1;31m"
g = "\033[1;32m"
y = "\033[1;33m"
b = "\033[1;34m"
m = "\033[1;35m"
c = "\033[1;36m"
w = "\033[1;37m"
# Color definitions using Rich
R = "[bold red]"
G = "[bold green]"
Y = "[bold yellow]"
B = "[bold blue]"
M = "[bold magenta]"


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_dashboard1():
    clear_console()
    remaining_time = get_time_remaining()
    rp(f"{B}{'='*50}")
    rp(f"{G}Approval Key: {FIXED_APPROVAL_KEY}")
    rp(f"{Y}Time remaining: {remaining_time}")
    rp(f"{B}{'='*50}")

def delete_approval_key():
    try:
        if os.path.exists(APPROVAL_KEY_FILE):
            os.remove(APPROVAL_KEY_FILE)
        if os.path.exists(KEY_TIMESTAMP_FILE):
            os.remove(KEY_TIMESTAMP_FILE)
        rp(f"{G}Approval key and timestamp deleted successfully.")
    except Exception as e:
        rp(f"{R}Error deleting approval key: {e}")

def delete_access_key():
    try:
        if os.path.exists(AUTH_KEY_FILE):
            os.remove(AUTH_KEY_FILE)
        rp(f"{G}Previous access key deleted successfully.")
    except Exception as e:
        rp(f"{R}Error deleting access key: {e}")

def is_key_expired():
    if not os.path.exists(KEY_TIMESTAMP_FILE):
        return True
    try:
        with open(KEY_TIMESTAMP_FILE, 'r') as f:
            timestamp = float(f.read().strip())
        return (time.time() - timestamp) > 86400  # 1 day
    except Exception as e:
        rp(f"{R}Error checking key expiration: {e}")
        return True

def get_time_remaining():
    if not os.path.exists(KEY_TIMESTAMP_FILE):
        return "Unknown"
    try:
        with open(KEY_TIMESTAMP_FILE, 'r') as f:
            timestamp = float(f.read().strip())
        remaining_seconds = 86400 - (time.time() - timestamp)  # 24 hours
        if remaining_seconds > 0:
            hours = remaining_seconds // 3600
            minutes = (remaining_seconds % 3600) // 60
            seconds = remaining_seconds % 60
            return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
        else:
            return "Expired"
    except Exception as e:
        rp(f"{R}Error calculating time remaining: {e}")
        return "Unknown"

def is_device_approved():
    if os.path.exists(APPROVAL_KEY_FILE):
        try:
            with open(APPROVAL_KEY_FILE, 'r') as f:
                stored_key = f.read().strip()
            return stored_key == FIXED_APPROVAL_KEY and not is_key_expired()
        except Exception as e:
            rp(f"{R}Error checking device approval: {e}")
            return False
    return False

def is_api_reachable():
    try:
        response = requests.get(API_URL)
        return response.status_code == 200
    except requests.RequestException:
        rp(f"{Y}TOOL IS UNDER MAINTENANCE")
        return False

def validate_key(key):
    url = f'{API_URL}{key}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            if 'token' in result and result['token'] == key:
                return True
        return False
    except requests.RequestException as e:
        rp(f"{R}Error validating key: {e}")
        return False

def approve_key():
    if not is_api_reachable():
        rp(f"{R}API is not reachable. Exiting the script.")
        exit()

    if is_device_approved():
        rp(f"{G}This device is already approved.")
        
        try:
            with open(APPROVAL_KEY_FILE, 'r') as f:
                current_key = f.read().strip()
            if not validate_key(current_key):
                rp(f"{R}Your device is not approved. Please generate a new access key.")
                delete_approval_key()
                exit()
            else:
                clear_console()  
                show_dashboard()
                return
        except Exception as e:
            rp(f"{R}Error reading or validating stored key: {e}")
            exit()

    rp(f"{G}Your device approval key is: {FIXED_APPROVAL_KEY}")
    rp(f"{G}Please give this access key to the tool owner.")

    
    if not os.path.exists(AUTH_KEY_FILE):
        rp(f"{R}No access key file found. Exiting.")
        exit()

    try:
        with open(AUTH_KEY_FILE, 'r') as f:
            key_to_check = f.read().strip()
        if validate_key(key_to_check):
            save_approval_key(key_to_check)
            rp(f"{G}Key approved successfully.")
            time.sleep(86400) 
            delete_approval_key()
            rp(f"{G}Approval key deleted after 24 hours.")
            clear_console()
            show_dashboard()
        else:
            rp(f"{R}Your device is not approved. ")
            exit()
    except Exception as e:
        rp(f"{R}Error processing key approval: {e}")

def insert_approval_key():
    new_key = input("Enter the new fixed approval key: ").strip()
    if new_key:
        try:
            with open(AUTH_KEY_FILE, 'w') as f:
                f.write(new_key)
            global FIXED_APPROVAL_KEY
            FIXED_APPROVAL_KEY = new_key
            rp(f"{G}Fixed approval key updated successfully.")
        except Exception as e:
            rp(f"{R}Error updating fixed approval key: {e}")



def randc():
    return random.choice([G, Y])

BASE_URL = "https://dropmail.me/api/graphql/web-test-wgq6m5i"
BASE_URL2 = "https://www.1secmail.com/api/v1/"


def logo():
    rp(pan(f"""{randc()} 
 𝗧𝗼𝗼𝗹 𝗧𝘆𝗽𝗲: RPW TOOLS (APPROVAL)
 𝐓𝐨𝐨𝐥 𝐕𝐞𝐫𝐬𝐢𝐨𝐧: 1
 𝗧𝗼𝗼𝗹 𝗢𝘄𝗻𝗲𝗿: Leinathan Añabo Oremor
 𝗡𝗲𝘁𝘄𝗼𝗿𝗸: All Network
 """,
           title=f"{Y}RPW TOOLS",
           border_style="bold yellow"))
           
#approval details dashboard
def approval_details():
    rp(pan(f"""{randc()}       
  𝐃𝐞𝐯𝐢𝐜𝐞 𝐀𝐜𝐜𝐞𝐬𝐬𝐊𝐞𝐲:{FIXED_APPROVAL_KEY}
  𝗞𝗲𝘆 𝗘𝘅𝗽𝗶𝗿𝗮𝘁𝗶𝗼𝗻:{get_time_remaining()}
""",
           title=f"{Y}𝐀𝐜𝐜𝐞𝐬𝐬 𝐊𝐞𝐲 𝐃𝐞𝐭𝐚𝐢𝐥𝐬",
           border_style="bold yellow"))

# Clear function
def clear():
    if pf in ['win32', 'win64']:
        sm('cls')
    else:
        sm('clear')
    logo()




def other_tools_menu():
    rp(f"{G}Other tools menu function not yet implemented.")
        

EMAIL_FOLDER = "email"
TEMPMail_FILE = os.path.join(EMAIL_FOLDER, "tempmail.txt")

def ensure_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def save_email_to_file(email, id_, expires_at):
    ensure_folder_exists(EMAIL_FOLDER)
    now = datetime.now(timezone.utc).isoformat()
    expires_at_dt = datetime.fromisoformat(expires_at).replace(tzinfo=timezone.utc)
    expiration_time = expires_at_dt.isoformat()
    with open(TEMPMail_FILE, "w") as file:
        file.write(f"{email} - time: {now} expires: {expiration_time}\n")

def random_mail():
    query = "mutation { introduceSession { id, expiresAt, addresses { address } } }"
    response = requests.post(BASE_URL, json={"query": query})
    response.raise_for_status()
    data = response.json()
    return [data['data']['introduceSession']['addresses'][0]['address'],
            data['data']['introduceSession']['id'],
            data['data']['introduceSession']['expiresAt']]

def get_mails(id_):
    query = f"query ($id: ID!) {{ session(id: $id) {{ mails {{ rawSize, fromAddr, toAddr, downloadUrl, text, headerSubject }} }} }}"
    variables = {"id": id_}
    response = requests.post(BASE_URL, json={"query": query, "variables": variables})
    response.raise_for_status()
    data = response.json()
    return data['data']['session']['mails']

def ms_to_time(duration):
    milliseconds = int(duration % 1000 / 100)
    seconds = int(duration / 1000 % 60)
    minutes = int(duration / 60000 % 60)
    hours = int(duration / 3600000 % 24)
    return f"{hours}h {minutes}m {seconds}s {milliseconds}ms"

def format_size(size_in_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    index = 0
    while size_in_bytes >= 1024 and index < len(units) - 1:
        size_in_bytes /= 1024
        index += 1
    return f"{size_in_bytes:.2f} {units[index]}"


def email_menu():
    email_info = None

    while True:
        
        rp(pan(f"1. Generate Random Email Address\n"
               f"2. Check Mailbox\n"
               f"3. Fetch Single Message\n"
               f"0. Back\n",
               title="V1 [DROPMAIL]",
               border_style="bold yellow"))

        choice = input("Enter choice (1-3): ")

        if choice == '1':
            email, id_, expires_at = random_mail()
            if email:
                expires_at_dt = datetime.fromisoformat(expires_at).replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                time_diff = expires_at_dt - now
                print(f"EMAIL: {email}")
                print(f"ID: {id_}")
                print(f"Expires in: {ms_to_time(time_diff.total_seconds() * 1000)}")
                email_info = {"email": email, "id": id_, "expires_at": expires_at}
                save_email_to_file(email, id_, expires_at)

        elif choice == '2':
            if email_info:
                print("Fetching Messages...")
                mails = get_mails(email_info["id"])
                print("Messages:")
                for i, mail in enumerate(mails):
                    print(f"EMAIL [{i + 1}]")
                    print(f"From: {mail['fromAddr']}")
                    print(f"To: {mail['toAddr']}")
                    print(f"Message: {mail['text']}")
                    print(f"Size: {format_size(mail['rawSize'])}")
                    print(f"Header: {mail['headerSubject']}")
                    print(f"Download: {mail['downloadUrl']}")
                    print("---")
            else:
                print("Generate an email address first.")

        elif choice == '3':
            if email_info:
                try:
                    message_id = int(input("Enter Message ID: "))
                    if message_id > 0:
                        mails = get_mails(email_info["id"])
                        if message_id <= len(mails):
                            mail = mails[message_id - 1]
                            print("Message Details:")
                            print(f"From: {mail['fromAddr']}")
                            print(f"Subject: {mail['headerSubject']}")
                            print(f"Date: {mail.get('date', 'No date available')}")
                            print(f"Body (text): {mail['text']}")
                            print(f"Body (html): {mail.get('htmlBody', 'No HTML body available')}")
                        else:
                            print("Invalid message ID.")
                    else:
                        print("Please provide a valid message ID.")
                except ValueError:
                    print("Please enter a numeric value for the message ID.")
            else:
                print("Generate an email address first.")

        elif choice == '0':
            break

        else:
            print("Invalid choice. Please select a number between 0 and 3.")




BASE_URL2 = "https://www.1secmail.com/api/v1/"

def generate_random_mailboxes(count):
    response = requests.get(f"{BASE_URL2}?action=genRandomMailbox&count={count}")
    return response.json()

def get_messages(login, domain):
    response = requests.get(f"{BASE_URL2}?action=getMessages&login={login}&domain={domain}")
    return response.json()

def read_message(login, domain, message_id):
    response = requests.get(f"{BASE_URL2}?action=readMessage&login={login}&domain={domain}&id={message_id}")
    return response.json()

def save_emails_to_file(emails):
    if not os.path.exists('email'):
        os.makedirs('email')
    
    file_path = os.path.join('email', 'genmail.txt')
    
    with open(file_path, 'a') as file:
        for email in emails:
            file.write(email + '\n')

def save_message_to_file(message):
    file_path = os.path.join('email', 'message.txt')
    
    with open(file_path, 'a') as file:
        file.write(f"From: {message.get('from', 'N/A')}\n")
        file.write(f"Subject: {message.get('subject', 'N/A')}\n")
        file.write(f"Date: {message.get('date', 'N/A')}\n")
        file.write(f"Body (text): {message.get('textBody', 'N/A')}\n")
        file.write(f"Body (html): {message.get('htmlBody', 'N/A')}\n")
        file.write("="*40 + "\n")

def tempmailv2_menu():
   
    print(Fore.YELLOW + Style.BRIGHT + "V2 [1SECMAIL]".center(50))
    print(Fore.GREEN + Style.BRIGHT + "1. Generate Random Email Addresses".ljust(50))
    print(Fore.GREEN + Style.BRIGHT + "2. Check Mailbox".ljust(50))
    print(Fore.GREEN + Style.BRIGHT + "3. Fetch Single Message".ljust(50))
    print(Fore.RED + Style.BRIGHT + "4. Exit".ljust(50))
   

def tempmailv2():
    while True:
        tempmailv2_menu()
        choice = input(Fore.YELLOW + "Enter your choice (1/2/3/4): ")

        if choice == '1':
            count = int(input(Fore.YELLOW + "Number of emails to generate (1-70): "))
            if 1 <= count <= 70:
                emails = generate_random_mailboxes(count)
                print(Fore.GREEN + Style.BRIGHT + "Generated Emails:")
                for email in emails:
                    print(Fore.YELLOW + email)
                
                save_emails_to_file(emails)
            else:
                print(Fore.RED + "Invalid number of emails. Please enter a number between 1 and 70.")
        
        elif choice == '2':
            login = input(Fore.YELLOW + "Login (username): ")
            domain = input(Fore.YELLOW + "Domain (e.g., 1secmail.com): ")
            if login and domain:
                messages = get_messages(login, domain)
                print(Fore.GREEN + Style.BRIGHT + "Messages:")
                for message in messages:
                    print(Fore.YELLOW + f"ID: {message['id']}, From: {message['from']}, Subject: {message['subject']}, Date: {message['date']}")
                    save_message_to_file(message)
            else:
                print(Fore.RED + "Please provide both login and domain.")
        
        elif choice == '3':
            login = input(Fore.YELLOW + "Login (username): ")
            domain = input(Fore.YELLOW + "Domain (e.g., 1secmail.com): ")
            message_id = int(input(Fore.YELLOW + "Message ID: "))
            if login and domain and message_id:
                message = read_message(login, domain, message_id)
                print(Fore.GREEN + Style.BRIGHT + "Message Details:")
                print(Fore.YELLOW + f"From: {message.get('from', 'N/A')}")
                print(Fore.YELLOW + f"Subject: {message.get('subject', 'N/A')}")
                print(Fore.YELLOW + f"Date: {message.get('date', 'N/A')}")
                print(Fore.YELLOW + f"Body (text): {message.get('textBody', 'N/A')}")
                print(Fore.YELLOW + f"Body (html): {message.get('htmlBody', 'N/A')}")
                save_message_to_file(message)
            else:
                print(Fore.RED + "Please provide login, domain, and message ID.")
        
        elif choice == '4':
            print(Fore.RED + "Exiting...")
            break
        
        else:
            print(Fore.RED + "Invalid choice. Please enter 1, 2, 3, or 4.")


def main():
    while True:
        clear()
        rp(pan(f"{Y}[1] {G}TEMP-MAIL\n"
                f"{Y}[2] {G}OTHER TOOLS\n"
                f"{Y}[0] {G}EXIT\n",
                title=f"{Y}Main Menu",
                border_style="bold yellow"))

        choice = input("Enter your choice: ")

        if choice == '1':
            tempmail()
        elif choice == '2':
            other_tools_menu()
        elif choice == '0':
            break
        else:
            rp(f"{R}Invalid choice. Please select a valid option.")

def tempmail():
    while True:
        clear()
        

        choice = input("Enter your choice: ")

        if choice == '1':
            email_menu()
        elif choice == '2':
            tempmailv2()  
        elif choice == '0':
            break
        else:
            rp(f"{R}Invalid choice. Please select a valid option.")
import requests
import os
from colorama import Fore, Style


BASE_URL2 = "https://www.1secmail.com/api/v1/"

def generate_random_mailboxes(count):
    response = requests.get(f"{BASE_URL2}?action=genRandomMailbox&count={count}")
    return response.json()

def get_messages(login, domain):
    response = requests.get(f"{BASE_URL2}?action=getMessages&login={login}&domain={domain}")
    return response.json()

def read_message(login, domain, message_id):
    response = requests.get(f"{BASE_URL2}?action=readMessage&login={login}&domain={domain}&id={message_id}")
    return response.json()

def save_emails_to_file(emails):
    if not os.path.exists('email'):
        os.makedirs('email')
    
    file_path = os.path.join('email', 'genmail.txt')
    
    with open(file_path, 'a') as file:
        for email in emails:
            file.write(email + '\n')

def save_message_to_file(message):
    file_path = os.path.join('email', 'message.txt')
    
    with open(file_path, 'a') as file:
        file.write(f"From: {message.get('from', 'N/A')}\n")
        file.write(f"Subject: {message.get('subject', 'N/A')}\n")
        file.write(f"Date: {message.get('date', 'N/A')}\n")
        file.write(f"Body (text): {message.get('textBody', 'N/A')}\n")
        file.write(f"Body (html): {message.get('htmlBody', 'N/A')}\n")
        file.write("="*40 + "\n")

url = 'https://prod.api.vodex.ai/api/v1/trigger-demo-call'
headers = {
    'authority': 'prod.api.vodex.ai',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://vodex.ai',
    'referer': 'https://vodex.ai/',
    'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
}

def trigger_demo_call(phone, email, first_name, last_name):
    data = {
        "phone": phone,
        "email": email,
        "firstName": first_name,
        "lastName": last_name
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status() 
        return response.json()  
    except requests.RequestException as e:
        return {"error": str(e)}

from colorama import Fore, Style, init


init()

def main_call():
    print(Fore.CYAN + "RFC TOOLS SPAM CALL" + Style.RESET_ALL)

    
    phone = input(Fore.GREEN + "Phone Number (default: 639161131834): " + Style.RESET_ALL) or "639161131834"
    email = input(Fore.GREEN + "Email Address (default: example@gmail.com): " + Style.RESET_ALL) or "example@gmail.com"
    first_name = input(Fore.GREEN + "First Name (default: RFC TOOLS): " + Style.RESET_ALL) or "RFC TOOLS"
    last_name = input(Fore.GREEN + "Last Name (default: (RFC)): " + Style.RESET_ALL) or "(RFC)"

    if input(Fore.YELLOW + "Trigger Demo Call? (yes/no): " + Style.RESET_ALL).strip().lower() == 'yes':
        response_data = trigger_demo_call(phone, email, first_name, last_name)

        if "error" in response_data:
            print(Fore.RED + f"Error: {response_data['error']}" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "Campaign run started successfully" + Style.RESET_ALL)
            print(Fore.GREEN + "Response Data:" + Style.RESET_ALL)
            print(response_data) 
            
            try:
                api_res = response_data.get("data", {}).get("data", {}).get("apiRes", {})
                successful_calls = api_res.get("successful", [])
                if successful_calls:
                    print(Fore.GREEN + "Successful Calls:" + Style.RESET_ALL)
                    for call in successful_calls:
                        print(Fore.BLUE + f"Call UUID: {call.get('call_uuid')}" + Style.RESET_ALL)
                        print(Fore.BLUE + f"Mobile Number: {call.get('mobile_number')}" + Style.RESET_ALL)
                        print(Fore.BLUE + f"Status: {call.get('status')}" + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + "No successful calls found." + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Failed to parse response data: {str(e)}" + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "Demo call not triggered." + Style.RESET_ALL)
        
def format_number(number):
    if number.startswith('0'):
        return f'+63{number[1:]}'
    elif number.startswith('63'):
        return f'+{number}'
    else:
        return number

def send_otp(number):
    formatted_number = format_number(number)
    url = "https://graphql.toktok.ph:2096/auth/graphql/"
    headers = {
        'accept': '*/*',
        'authorization': '',
        'Content-Type': 'application/json',
        'Host': 'graphql.toktok.ph:2096',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.9.1'
    }
    body = {
        "operationName": "loginRegister",
        "variables": {
            "input": {
                "mobile": formatted_number,
                "appFlavor": "C"
            }
        },
        "query": "mutation loginRegister($input: LoginRegisterInput!) {\nloginRegister(input: $input)\n}\n"
    }

    try:
        response = requests.post(url, json=body, headers=headers)
        if response.json().get('data', {}).get('loginRegister') == "REGISTER":
            return True
        else:
            return False
    except Exception as e:
        print(Fore.RED + f'Error sending OTP: {e}')
        return False

def main_sms():
    number = input("Phone Number: ").strip()
    amount = int(input("Number of Messages: ").strip())
    sleep = int(input("Sleep Time (seconds): ").strip())

    if number and amount > 0 and sleep > 0:
        success_count = 0
        failure_count = 0
        
        print(Fore.CYAN + f"Bombing to: {number}")
        for i in range(amount):
            result = send_otp(number)
            if result:
                success_count += 1
                print(Fore.GREEN + f"Message {i + 1}: Success")
            else:
                failure_count += 1
                print(Fore.RED + f"Message {i + 1}: Failed")
            time.sleep(sleep)
        
        print(Fore.CYAN + f"Successfully bombed {success_count} times to {number}. Failed attempts: {failure_count}")
    else:
        print(Fore.YELLOW + "Please provide a valid number, amount, and sleep time.")


def send_spam(username, message, spam_count):
    device_id = '23d7346e-7d22-4256-80f3-dd4ce3fd8878'
    for i in range(spam_count):
        try:
            response = requests.post('https://ngl.link/api/submit', json={
                'username': username,
                'question': message,
                'deviceId': device_id,
                'gameSlug': '',
                'referrer': '',
            })
            
            if response.status_code == 200:
                print(Fore.GREEN + f"Message {i + 1}: Sent successfully.")
            else:
                print(Fore.RED + f"Message {i + 1}: Failed to send. Status code: {response.status_code}")
        except Exception as e:
            print(Fore.YELLOW + f"Message {i + 1}: Error: {e}")

    print(Fore.CYAN + f"Successfully spammed {spam_count} times to {username}.")

def ngl_main():
    
    username = input(Fore.YELLOW + "Enter NGL Username: " + Style.RESET_ALL)
    message = input(Fore.YELLOW + "Enter Message to Spam: " + Style.RESET_ALL)
    
   
    try:
        spam_count = int(input(Fore.YELLOW + "Enter Number of Messages: " + Style.RESET_ALL))
        if spam_count < 1:
            raise ValueError("Number of messages must be at least 1.")
    except ValueError as e:
        print(Fore.RED + f"Invalid number of messages: {e}")
        exit(1)

    send_spam(username, message, spam_count)
             
                                      
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


ACCOUNT_FOLDER = 'account'
ACCOUNT_FILE = os.path.join(ACCOUNT_FOLDER, 'spotify.txt')


os.makedirs(ACCOUNT_FOLDER, exist_ok=True)

def create_spotify_account():
    try:
        response = requests.get("https://freespotify-1w2c.onrender.com/spotify/create")
        if response.status_code == 200:
            data = response.json()
            email = data.get('email')
            password = data.get('password')
            save_account(email, password)
            return (f"{Colors.GREEN}Free Spotify account created successfully!{Colors.RESET}\n"
                    f"Email: {Colors.YELLOW}{email}{Colors.RESET}\n"
                    f"Password: {Colors.YELLOW}{password}{Colors.RESET}")
        else:
            return f"{Colors.RED}An error occurred while creating the Spotify account. Please try again later.{Colors.RESET}"
    except requests.RequestException as e:
        return (f"{Colors.RED}Failed to create the Spotify account. Please try again later.{Colors.RESET}\n"
                f"Error: {e}")

def save_account(email, password):
    with open(ACCOUNT_FILE, 'a') as file:
        file.write(f"Email: {email}\nPassword: {password}\n\n")

def main_spotify():
    while True:
        print(f"{Colors.BLUE}Spotify Menu{Colors.RESET}")
        print(f"{Colors.YELLOW}1. Create a Free Spotify Account{Colors.RESET}")
        print(f"{Colors.YELLOW}2. Exit{Colors.RESET}")
        choice = input(f"{Colors.CYAN}Enter your choice (1 or 2): {Colors.RESET}").strip()

        if choice == "1":
            print(f"{Colors.CYAN}Please wait for a few minutes...{Colors.RESET}")
            result = create_spotify_account()
            print(result)
        elif choice == "2":
            print(f"{Colors.GREEN}Exiting...{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}Invalid choice. Please select 1 or 2.{Colors.RESET}")
               
account_dir = 'account'
account_file = os.path.join(account_dir, 'microsoft.txt')


os.makedirs(account_dir, exist_ok=True)

def create_micro_team():
    try:
        response = requests.get("https://freemicro-zgz7.onrender.com/teams/create")
        print(Fore.CYAN + f"Response Status Code: {response.status_code}" + Style.RESET_ALL)  # Debug output
        if response.status_code == 200:
            data = response.json()
            print(Fore.CYAN + f"Response JSON: {data}" + Style.RESET_ALL)  # 
            email = data.get('email')
            password = data.get('password')
            if email and password:
                account_info = (Fore.GREEN + "Micro team created successfully!" + Style.RESET_ALL +
                                f"\nEmail: {email}\nPassword: {password}")
                
            
                with open(account_file, 'a') as f:
                    f.write(f"Email: {email}\nPassword: {password}\n\n")
                
                return account_info
            else:
                return Fore.RED + "Failed to retrieve account details from the response." + Style.RESET_ALL
        else:
            return Fore.RED + "An error occurred while creating the micro team. Please try again later." + Style.RESET_ALL
    except requests.RequestException as e:
        return Fore.RED + f"Failed to create the micro team. Please try again later.\nError: {e}" + Style.RESET_ALL


def microsoft_menu():
    print(Fore.CYAN + "Free Micro Account Creator" + Style.RESET_ALL)
    print(Fore.YELLOW + "1. Create Micro Team" + Style.RESET_ALL)
    print(Fore.YELLOW + "2. Exit" + Style.RESET_ALL)
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        print(Fore.BLUE + "Please wait for a minute while we create your micro team..." + Style.RESET_ALL)
        time.sleep(2) 
        result = create_micro_team()
        print(result)
    elif choice == '2':
        print(Fore.GREEN + "Exiting. Have a great day!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid choice. Please enter 1 or 2." + Style.RESET_ALL)
        microsoft_menu()
 
#description guide
def description_guide():
    clear_console()
    logo()
    approval_details()
    rp(pan(f"""
**Menu 1: Create Spotify Account**
- This option allows the user to create a new Spotify account.
- Once the account is created, the details of the new account will be displayed in the console.
- The account details will also be automatically saved to a file named `spotify.txt` located in the `account` folder.

**Menu 2: Create Microsoft Account**
- This option allows the user to create a new Microsoft account.
- The details of the new account will not be displayed in the console.
- The account details will be automatically saved to a file named `spotify.txt` located in the `account` folder.

Thank you for using the tool!
""", title=f"{Y}Description Guide", border_style="bold yellow"))
    input("Press Enter to return to the main menu...")
     
             

def show_dashboard():
    while True:
        clear()
        approval_details()
        rp(pan(f"{Y}[1] {G}TEMP-MAIL\n"
                f"{Y}[2] {G}SPAM CALL/SMS/NGL\n"
                f"{Y}[3] {G}AUTO CREATE\n"
                f"{Y}[0] {G}EXIT\n",
                title=f"{Y}Main Menu",
                border_style="bold yellow"))

        choice = input("Enter your choice: ")

        if choice == '1':
            tempmail()
        elif choice == '2':
            spam_callsms()
        elif choice == '3':
            auto_create()
        elif choice == '0':
            break
        else:
            rp(f"{R}Invalid choice. Please select a valid option.")

def tempmail():
    while True:
        clear()
        approval_details()
        rp(pan(f"{Y}[1] {G}DROPMAIL\n"
                f"{Y}[2] {G}1SECMAIL\n"
                f"{Y}[0] {G}BACK\n",
                title=f"{Y}Temporary Email",
                border_style="bold yellow"))

        choice = input("Enter your choice: ")

        if choice == '1':
            email_menu()
        elif choice == '2':
            tempmailv2()  
        elif choice == '0':
            break
        else:
            rp(f"{R}Invalid choice. Please select a valid option.")

def spam_callsms():
    while True:
        clear()
        approval_details()
        rp(pan(f"{Y}[1] {G}SPAM CALL\n"
                f"{Y}[2] {G}SPAM SMS\n"
                f"{Y}[3] {G}SPAM NGL\n"
                f"{Y}[0] {G}BACK\n",
                title=f"{Y}SPAM TOOLS",
                border_style="bold yellow"))

        choice = input("Enter your choice: ")

        if choice == '1':
            main_call()
        elif choice == '2':
            main_sms()
        elif choice == '3':
        	ngl_main()
        elif choice == '0':
            break
        else:
            rp(f"{R}Invalid choice. Please select a valid option.")            

def auto_create():
    while True:
        clear()
        approval_details()
        rp(pan(f"{Y}[1] {G}SPOTIFY ACCOUNT\n"
                f"{Y}[2] {G}MICROSOFT ACCOUNT\n"
                 f"{Y}[3] {G}GUIDE\n"
                f"{Y}[0] {G}BACK\n",
                title=f"{Y}AUTO CREATE ACCOUNT",
                border_style="bold yellow"))

        choice = input("Enter your choice: ")

        if choice == '1':
            main_spotify()
        elif choice == '2':
            microsoft_menu()
        elif choice == '3':
        	description_guide()
        elif choice == '0':
            break
        else:
            rp(f"{R}Invalid choice. Please select a valid option.")            
                                                                                                                        
                                                
def main():
    if FIXED_APPROVAL_KEY is None:
        rp(f"{R}Fixed approval key could not be loaded. Exiting.")
        exit()

    if not is_api_reachable():
        rp(f"{G}                          -RFCP TEAM")
        exit()

    while True:
        user_choice = input("Do you want to generate a new access key? (yes/no): ").strip().lower()
        if user_choice == 'yes':
            if os.path.exists(AUTH_KEY_FILE):
                delete_access_key()  
            generated_key = generate_access_key()
            save_access_key(generated_key)
        elif user_choice == 'no':
            if not os.path.exists(AUTH_KEY_FILE):
                rp(f"{R}No access key has been generated. Please generate a key first.")
                continue
            with open(AUTH_KEY_FILE, 'r') as f:
                generated_key = f.read().strip()
            rp(f"{G}Using the previously generated access key.")
        else:
            rp(f"{R}Invalid choice. Please enter 'yes' or 'no'.")
            continue
        break

    clear_console()
    approve_key()

if __name__ == "__main__":
    main()
#
