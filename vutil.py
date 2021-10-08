#python3
import os
import requests
import base64
import pickle
import time
import getpass

class limitCounter:
 def __init__(self, maxcount=10):
  self.sleepCount = 0
  self.sleepCountMax = maxcount
 def count(self):
  if self.sleepCount >= self.sleepCountMax:
   print("INFO night night zzz...(5)")
   time.sleep(5)
   self.sleepCount = 0
  else:
   self.sleepCount += 1

_s = requests.session()
_s.headers['User-Agent'] = "wfscans/vrcutil"
_configPath = os.path.expanduser("~/.vrchatpickle") #*Should* work on linux/windows/mac
_userId = ""
sleep = limitCounter()
_v = "1.01"

def rq(method, url, body=None, header={}, baseUrl="https://api.vrchat.cloud/api/1"):
    if method == "GET":
        r = _s.get(baseUrl + url, headers=header)
    elif method == "POST":
        r = _s.post(baseUrl + url, data=body)
    elif method == "PUT":
        r = _s.put(baseUrl + url)
    elif method == "DELETE":
        r = _s.delete(baseUrl + url)
    else:
        raise Exception("invalid request type given")
    if r.status_code != 200:
        return [False, r]
    else:
        return [True, r]

def login():
    print("Please login:")
    r = rq("GET", "/auth/user", header={'Authorization':f'Basic {base64.b64encode((input("Username ") + ":" + getpass.getpass()).encode()).decode()}'})
    if not r[0]:
        raise Exception("failed to login")
    else:
        print(f"INFO logged-in as {r[1].json()['displayName']}")
        _userId = r[1].json()['id']
    with open(_configPath, 'wb') as f:
        pickle.dump(_s.cookies, f)

if os.path.exists(_configPath):
 with open(_configPath, 'rb') as f:
  _s.cookies = pickle.load(f)
 r = rq("GET", "/auth/user")
 if not r[0]:
  if r[1].status_code == 401:
   print("WARNING cached login expired")
   login()
  else:
   raise Exception(f"failed to verify auth token from {_configPath}")
 print(f"INFO logged-in as {r[1].json()['displayName']}")
 _userId = r[1].json()['id']
else:
 login()
