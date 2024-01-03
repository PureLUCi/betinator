from pwned import meridian
from utility import settings

from threading import Thread


print("👋🏼 Welcome to \"Betinator\" - Property of CR3W")

meridianSessions = []
for account in settings.accounts:
    if(account["bookie"] == "meridianRS"):
        meridianSession = meridian.LogIn(account["username"],account["password"])
        if meridianSession is not None:
            meridianSessions.append(meridianSession)

if(len(meridianSessions)<1):
    print("❌ Meridian","No accounts available... Exiting...")
    exit()     

print("\n🥵 Account availability:\n👉🏼 Meridian accounts:",len(meridianSessions))

if meridian.CheckIfMatchIsAvailable(meridianSessions[0]) == False:
    meridianSessions = []


while True:
    teamToBetOn = int(input("\n🤑 Enter team to bet on ( 1 or 2 ): "))
    for meridianSession in meridianSessions:
        Thread(target=meridian.PlaceBet,args=(meridianSession,teamToBetOn)).start()
    exit()