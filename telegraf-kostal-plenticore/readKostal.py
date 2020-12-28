#!/usr/bin/python3

##readKostal.py
## 01.12.2020
## A. Behnke
#####
##
## https://stackoverflow.com/questions/59053539/api-call-portation-from-java-to-python-kostal-plenticore-inverter?answertab=active#tab-top
##
## Library for Cryptodome.Cipher: pip3 install pycryptodome
## apt install python3-pycryptodome

import sys
import random
import string
import base64
import json
import requests
import hashlib
import os
import hmac
from Cryptodome.Cipher import AES
import binascii

## IP or DNS of the Plenticore device.
plenticore = 'wechselrichter.xxxxxx.local'



## USER_TYPE must be "user" or "master"
USER_TYPE = "user"
PASSWD = 'Axxxxxxxxxxxxx7/'
BASE_URL = "http://" + plenticore + "/api/v1"
AUTH_START = "/auth/start"
AUTH_FINISH = "/auth/finish"
AUTH_CREATE_SESSION = "/auth/create_session"
ME = "/auth/me"

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def getPBKDF2Hash(password, bytedSalt, rounds):
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytedSalt, rounds)


u = randomString(12)
u = base64.b64encode(u.encode('utf-8')).decode('utf-8')

step1 = {
  "username": USER_TYPE,
  "nonce": u
}
step1 = json.dumps(step1)

url = BASE_URL + AUTH_START
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
response = requests.post(url, data=step1, headers=headers)
response = json.loads(response.text)
i = response["nonce"]
e = response['transactionId']
o = response['rounds']
a = response['salt']
bitSalt = base64.b64decode(a)



r = getPBKDF2Hash(PASSWD,bitSalt,o)
s = hmac.new(r, "Client Key".encode('utf-8'), hashlib.sha256).digest()
c = hmac.new(r, "Server Key".encode('utf-8'), hashlib.sha256).digest()
_ = hashlib.sha256(s).digest()
d = "n=user,r="+u+",r="+i+",s="+a+",i="+str(o)+",c=biws,r="+i
g = hmac.new(_, d.encode('utf-8'), hashlib.sha256).digest()
p = hmac.new(c, d.encode('utf-8'), hashlib.sha256).digest()
f = bytes(a ^ b for (a, b) in zip(s, g))
proof = base64.b64encode(f).decode('utf-8')

step2 = {
  "transactionId": e,
  "proof": proof
}
step2 = json.dumps(step2)

url = BASE_URL + AUTH_FINISH
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
response = requests.post(url, data=step2, headers=headers)
response = json.loads(response.text)
token = response['token']
signature = response['signature']

y = hmac.new(_, "Session Key".encode('utf-8'), hashlib.sha256)
y.update(d.encode('utf-8'))
y.update(s)
P = y.digest()
protocol_key = P
t = os.urandom(16)

e2 = AES.new(protocol_key,AES.MODE_GCM,t)
e2, authtag = e2.encrypt_and_digest(token.encode('utf-8'))

step3 = {
  "transactionId": e,
  "iv": base64.b64encode(t).decode('utf-8'),
  "tag": base64.b64encode(authtag).decode("utf-8"),
  "payload": base64.b64encode(e2).decode('utf-8')
}
step3 = json.dumps(step3)

headers = { 'Content-type': 'application/json', 'Accept': 'application/json' }
url = BASE_URL + AUTH_CREATE_SESSION
response = requests.post(url, data=step3, headers=headers)
response = json.loads(response.text)
sessionId = response['sessionId']

#create a new header with the new Session-ID for all further requests
headers = { 'Content-type': 'application/json', 'Accept': 'application/json', 'authorization': "Session " + sessionId }
url = BASE_URL + ME
response = requests.get(url = url, headers = headers)
response = json.loads(response.text)
authOK = response['authenticated']
if not authOK:
    print("authorization NOT OK")
    sys.exit()



datareq = [
    {
# Werte direkt am Kostal Wechselrichter (Netzanschluss- Seite)   
        "moduleid": "devices:local",
        "processdataids": [
# Gesamterzeugung DC
            "Dc_P",
#            "DigitalIn",
#            "EM_State",
# gemessene Werte der Netzversorgung am Wechselrichter pro Phase
#            "Grid_L1_I",
#            "Grid_L1_P",
#            "Grid_L2_I",
#            "Grid_L2_P",
#            "Grid_L3_I",
#            "Grid_L3_P",
            "Grid_P",
#            "Grid_Q",
#            "Grid_S",
#            "HomeBat_P",
# Bezug aus dem Netz W (gemessen am Wechselrichter)
            "HomeGrid_P",
# Bezug aus Eigenerzeugung (PV + Baterie)
            "HomeOwn_P",
# Bezug aus Eigenerzeugung PV
            "HomePv_P",
# Eigenverbrauch
            "Home_P",
#            "Inverter:State",
#            "Iso_R",
# Absoluter Wert der 70% Abregelungsgrenze
            "LimitEvuAbs",
            "LimitEvuRel",
#            "WorkTime"
        ]
    },
    {
# Werte direkt am Kostal Wechselrichter: Ausgang AC nach Wechselrichter           
        "moduleid": "devices:local:ac",
        "processdataids": [
#            "CosPhi",
            "Frequency",
            "InvIn_P",
# Aktuelle Erzeugung gesamt AC am Wechselrichter (identisch zu "P")
            "InvOut_P",
# Aktuelle Erzeugung Phase 1 AC am Wechselrichter 
            "L1_I",
            "L1_P",
            "L1_U",
# Aktuelle Erzeugung Phase 1 AC am Wechselrichter 
            "L2_I",
            "L2_P",
            "L2_U",
# Aktuelle Erzeugung Phase 1 AC am Wechselrichter 
            "L3_I",
            "L3_P",
            "L3_U",
# Aktuelle Erzeugung gesamt AC am Wechselrichter 
            "P"
#,            
#            "Q",
#            "ResidualCDc_I",
#            "S"
        ]
    },
    {
# Werte vom SEM Powermeter 
        "moduleid": "devices:local:powermeter",
        "processdataids": [
#            "CosPhi",
            "Frequency",
            "L1_I",
# Hausverbrauch Phase 1 in W
            "L1_P",
#            "L1_Q",
#            "L1_S",
            "L1_U",
            "L2_I",
# Hausverbrauch Phase 2 in W
            "L2_P",
#            "L2_Q",
#            "L2_S",
            "L2_U",
            "L3_I",
# Hausverbrauch Phase 3 in W
            "L3_P",
#            "L3_Q",
#            "L3_S",
            "L3_U",
# Hausverbrauch gesamt in W
            "P"
#,
#            "Q",
#            "S"
        ]
    },
# Werte auf der DC Seite des Wechselrichters    
# DC Strang 1
        { "moduleid": "devices:local:pv1", "processdataids": ['I','U','P'] }
# DC Strang 2
        ,{ "moduleid": "devices:local:pv2", "processdataids": ['I','U','P'] }
# DC Strang 3  (nicht benutzt)      
#        ,{ "moduleid": "devices:local:pv3", "processdataids": ['I','U','P'] }
]

url = BASE_URL + "/processdata"
datareq = json.dumps(datareq)
response = requests.post(url = url, data=datareq, headers = headers)
response = json.loads(response.text)

## add device name to json
## response = response + [ {"plenticore-device": plenticore} ]



len_response = len(response)
x1 = 0
# Anpassung JSON an Grafana
s0 = '['
for i in response:
    s0 += "{ "+ json.dumps(i['moduleid'], indent=4) + " : {"
    s1 = ''

    ii = i['processdata']
    x2 = 0
    s2 = ''
    for j in ii:
        s2 = json.dumps(j['id'], indent=4) + ": "+ json.dumps(j['value'], indent=4)
        if x2 < len(ii)-1: s2 += ","
        s0 += s2
        x2 += 1
    s1 += "}}"
    if x1 < len(response)-1: s1 += ","
    x1 += 1
    s0 += s1
    

s0 += ']'
s0 = json.loads(s0)
print(json.dumps(s0, indent=4))

