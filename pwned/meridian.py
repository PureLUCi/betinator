import math
import time
import requests
import re
import hashlib
import random
from datetime import datetime, timedelta
from utility import settings


def LogIn(username,password):
    sender = requests.session()
    account = {}

    for accountObject in settings.accounts:
        if accountObject["username"] == username:
            account["betAmount"] = accountObject["betAmount"]
            account["proxy"] = {"http":"http://"+accountObject["proxy"]}


    response = sender.post("https://meridianbet.rs/cdn-cgi/challenge-platform/h/g/jsd/r/8381759dea4d4131",proxies=account["proxy"])
    response = sender.get('https://meridianbet.rs/sr/kladjenje/fudbal/češka',proxies=account["proxy"])
    try:
        hex_api_key = re.search(r'APM_BI_M_BKEM_BY = "(.+)";var OLD_WEBSITE_URL', response.text).group(1)
    except:
        print("❌ Failed to get API key... [ Are you using a VPN or a proxy for a wrong country? ]")
        return None
    api_key = bytes.fromhex(hex_api_key).decode()
    timestamp = (datetime.utcnow() + timedelta(hours=1)).strftime("%Y%m%d%H")
    bearer = api_key + timestamp
    sha256 = hashlib.sha256()
    sha256.update(bearer.encode())
    apikey = sha256.hexdigest()

    if apikey is None:
        return None
    payload = {
        'type': 'CheckLoginAction',
        'action': {},
    }    
    clientsessionID = str(int(datetime.now().timestamp())+math.floor(1e5*random.random()))
    sender.cookies.update({"clientsessionid":clientsessionID})

    headers = {
        "authorization":apikey,
        'content-type': 'application/json',
        'authority': 'meridianbet.rs',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
    }
    try:
        sender.post("https://meridianbet.rs/rest/mob/exec",json=payload,headers=headers,proxies=account["proxy"])
    except:
        return None

    payload = {
        'type': 'LoginAction',
        'action': {
            'username': username,
            'password': password,
            'clientApp': 'FULLSCREEN_V3',
        },
    }
    try:
        response = sender.post("https://meridianbet.rs/rest/mob/exec",json=payload,headers=headers,proxies=account["proxy"])
    except:
        return None


    if "result" not in response.json():
        print("❌",username,"account has false credentials or login failed...")
        return None

    account["sessionId"] = response.json()["result"]["sessionId"]
    account["token"] = response.json()["result"]["token"]
    account["playerID"] = response.json()["result"]["playerID"]
    account["apiKey"] = apikey
    account["username"]= username
    account["password"]= password

    return (sender,account)

def CheckIfMatchIsAvailable(session):
    response = session[0].get("https://meridianbet.rs/sails/events/single-live-page/58?filterPositions=0,0,0&type=time",proxies=session[1]["proxy"])
    events = response.json()["events"]

    for event in events:
        if(event["name"].lower() == settings.matches["meridianRS"]["home"]+" - "+settings.matches["meridianRS"]["away"]):
            print("✅",event["name"],"match found!")
            return response
    print("\n\n❌ MERIDIAN:",settings.matches["meridianRS"]["home"]+" - "+settings.matches["meridianRS"]["away"],"match not found...")
    return False

def GetEvent(session,rival):
    response = CheckIfMatchIsAvailable(session)
    events = response.json()["events"]
    eventStruct = {}


    for event in events:
        if(event["name"].lower() == settings.matches["meridianRS"]["home"]+" - "+settings.matches["meridianRS"]["away"]):
            try:
                eventStruct["id"] = event["liveShortMarkets"][2]["id"]
            except:
                print("❌",event["name"],"Option to bet next goal on team is not available...")
                return (None,None)
            for selection in event["liveShortMarkets"][2]["selection"]:
                if(selection["name"]==rival):
                    eventStruct["price"]=selection["price"]
            if "price" not in eventStruct.keys():
                if(rival == "[[Rival1]]"):
                    rival = "1"
                elif (rival == "[[Rival2]]"):
                    rival = "2"
                for selection in event["liveShortMarkets"][2]["selection"]:
                    if(selection["name"]==rival):
                        eventStruct["price"]=selection["price"]
            return (eventStruct,rival)
    return (None,None)

def PlaceBet(session,team):
    start = time.time()
    if team == 1:
        rival = "[[Rival1]]"
    else:
        rival = "[[Rival2]]"

    headers = {
        "authorization":session[1]["apiKey"],
        'content-type': 'application/json',
        'authority': 'meridianbet.rs',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
    }

    matchStruct,rival = GetEvent(session,rival)
    if(matchStruct is None):
        print("❌",session[1]["username"],"account failed to get match...")
        return None

    if matchStruct is None:
        print("❌",session[1]["username"],"account failed to get match...")
        return None
    if "price" not in matchStruct.keys():
        print("❌",session[1]["username"],"No price for match...")
        return None

    # Set bet
    payload = {"type":"TicketAddItemAction","action":{"selection":{"gameID":matchStruct["id"],"no":"0","name":rival,"price":matchStruct["price"],"trend":1,"shortcut":"","isSpreadGame":False}}}
    response = session[0].post("https://meridianbet.rs/rest/mob/exec",json=payload, headers=headers,proxies=session[1]["proxy"])
    if response.status_code !=200:
        if(response.status_code == 401):
            print("❌",session[1]["username"],"account is logged out...")
            session = LogIn(session[1]["username"],session[1]["password"])
            if session is None:
                print("❌",session[1]["username"],"account failed to log in...")
                return None
            PlaceBet(session,team)
        print("❌ Bet failed...")
        return None
    #print("✅ Bet slip created!")

    # set bet amount
    payload = {"type":"TicketSetMoneyAction","action":{"money":session[1]["betAmount"]}} # Read from config
    response = session[0].post("https://meridianbet.rs/rest/mob/exec",json=payload,headers=headers,proxies=session[1]["proxy"])
    if response.status_code !=200:
        print("❌ Bet failed...")
        return None
    #print("✅ Bet amount set!")

    payload = {"type":"TicketSubmitAction","action":{"bonusAccount":False,"acceptAllChanges":True,"clientApp":"FULLSCREEN_V3"}}
    response = session[0].post("https://meridianbet.rs/rest/mob/exec",json=payload,headers=headers,proxies=session[1]["proxy"])

    retries = 20
    while retries > 0:
        payload = {"type":"GetTicketAction","action":{}}
        response = session[0].post("https://meridianbet.rs/rest/mob/exec",json=payload,headers=headers,proxies=session[1]["proxy"])
        if("error" in response.json()["result"]["payinStatus"].keys()):
            print("❌",session[1]["username"],"Bet failed, error:",response.json()["result"]["payinStatus"]["error"])
            exit()

    """         payload = {"type":"CheckHistorySearchStatusAction","action":{}}
        lastTicket = session[0].post("https://meridianbet.rs/rest/mob/exec",json=payload,headers=headers,proxies=session[1]["proxy"])
        print(lastTicket)
        if(lastTicket.json()["result"]["tickets"][0] != response["result"]["ticket"]["id"]):
            time.sleep(1)
            retries -=1
            continue
        break """

    print("✅ Bet placed!")
    print("🕐",session[1]["username"],int(time.time()-start),"seconds")
    return 200