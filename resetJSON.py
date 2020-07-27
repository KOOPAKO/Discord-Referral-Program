import json
from pathlib import Path

joinedServer = []
referralCode = {}
referralCount = {}



def dumpToJson():
    jJoinedServer = json.dumps(joinedServer)
    with open(Path('data/joinedServer.json'), 'w') as f:
        f.write(jJoinedServer)
        f.close()
    jreferralCode = json.dumps(referralCode)
    with open(Path('data/referralCode.json'), 'w') as f:
        f.write(jreferralCode)
        f.close()
    jreferralCount = json.dumps(referralCount)
    with open(Path('data/referralCount.json'), 'w') as f:
        f.write(jreferralCount)
        f.close()
dumpToJson()
