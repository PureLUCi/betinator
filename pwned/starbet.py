import requests
import checkStarbetBets

lakurdaCookie = None

with open("cookies/starbet/lakurda.V3","r") as f:
    raw = f.read()
    raw = raw.splitlines()
    lakurdaCookie = {
        'style':"null",
        '.AspNet.ApplicationCookie':raw[0],
        'ASP.NET_SessionId':raw[1]
    }

headers = {
    'authority': 'starbet.rs',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json; charset=UTF-8',
    'dnt': '1',
    'origin': 'https://starbet.rs',
    'referer': 'https://starbet.rs/Bet',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

data = '{\'post\': \'{"Uplata":"20","BrPar":1,"Fiks":1,"Sis":"","TiketParovi":[{"Sifra":"1112","PN":"Paraguay U23 : Panama U23","Z1":"","T1":"2","K1":"20","Z2":"","T2":"","K2":"","Z3":"","T3":"","K3":"","TP1":"Gost Gol 4","TP2":"","TP3":"","TID1":"6161-688-4_00","TID2":0,"TID3":0,"T1ID":688,"T2ID":"","T3ID":"","L":"1","G1":4,"G2":0,"G3":0,"DatumNaIgranje":"2023-12-18T22:00:00.0000000+01:00","SID":0,"PID":3867291}],"TicketSequence":1702938343222,"IsEdited":null,"Id":null,"betType":"2","IsFreeBet":false,"VaucherID":0,"uuid":"3c879b49-195a-4e3a-b558-0520b45cf246","PrifakjamPromenetiKvoti":true}\'}'.encode()

response = requests.post('https://starbet.rs/Oblozuvanje.aspx/TiketUploadWeb', cookies=lakurdaCookie, headers=headers, data=data)

print(response.json())

checkStarbetBets.Check()