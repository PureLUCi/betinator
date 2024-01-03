import json

accounts = None
matches = None

with open("utility/accounts.json","r") as accounts:
    accounts = json.load(accounts)

with open("utility/matches.json","r") as matches:
    matches = json.load(matches)