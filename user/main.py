import requests, os
from settings import get_setting, set_setting

ip = "127.0.0.1"
port = "4321"

print("Welcome to the LSAuthentication program")

def main():
    if not get_setting("email")['success']:
        print("It seems like you don't have an account...")
        set_setting("email", input("What's your email? "))
    if not get_setting("uuid")['success']:
        headers = {
            "email": get_setting("email")['data'],
            "source": "app",
            "sent": "True"
        }

        c = requests.get(f"http://{ip}:{port}/api/v1/uuid/get", headers=headers).json()
        if c['status'] == 0: set_setting("uuid", c['uuid'])
        elif c['code'] == 403: exit("Signup with a new email. It has become invalid")

    os.system('clear')
    print(f"Logged in as {get_setting('email')['data']}: ({get_setting('uuid')['data']})")
    headers = {
        "email": get_setting("email")['data'],
        "uuid": get_setting("uuid")['data'],
        "source": "app",
        "sent": "True"
    }

    if input("Request Token? (any key / exit) ").lower() == "exit": exit()
    b = requests.get(f'http://{ip}:{port}/api/v1/token/get', headers=headers).json()
    if b['status'] == 0: print(f"Token: {b['token']}")
    else: print(b)

def mainnoutput():
    def main():
        if not get_setting("email")['success']: set_setting("email", input("What's your email? "))
        if not get_setting("uuid")['success']:
            headers = {
                "email": get_setting("email")['data'],
                "source": "app",
                "sent": "True"
            }

            c = requests.get(f"http://{ip}:{port}/api/v1/uuid/get", headers=headers).json()
            if c['status'] == 0:
                set_setting("uuid", c['uuid'])
            elif c['code'] == 403:
                exit("Signup with a new email. It has become invalid")

        headers = {
            "email": get_setting("email")['data'],
            "uuid": get_setting("uuid")['data'],
            "source": "app",
            "sent": "True"
        }

        b = requests.get(f'http://{ip}:{port}/api/v1/token/get', headers=headers).json()
        if b['status'] == 0:
            print(f"Token: {b['token']}")
        else:
            print(b)

main()