import json


if __name__ == '__main__':
    try:
        with open('cookies.json') as f:
            cookies = json.load(f)
    except FileNotFoundError:
        print('File not found')

    cookies = [cookie for cookie in cookies if 'olx' in cookie['domain']]

    with open('olx_cookies.json', 'w') as f:
        json.dump(cookies, f, indent=2)