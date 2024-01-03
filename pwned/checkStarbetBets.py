import requests

def Check():

    headers = {
        'authority': 'apilive.starbet.rs',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'dnt': '1',
        'origin': 'https://starbet.rs',
        'referer': 'https://starbet.rs/',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    params = {
        'SLID': '167118',
    }

    response = requests.get('https://apilive.starbet.rs/api/LiveOdds/GetAll', params=params, headers=headers)

    matches = response.json()
    lookingFor = "Birmingham : Leicester"

    for match in matches:
        if match["H"]["ParNaziv"] == lookingFor:
            print(match["H"])
        else:
            continue
        for letter in ["H","M","P","R","S"]:
            print(match[letter])

# Golovi se nalaze u R, kao G:"2-1" na primer


