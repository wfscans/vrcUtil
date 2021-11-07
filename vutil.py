import os
import requests, time, pickle
import base64
import getpass

version = "1.5"
configPath = os.path.expanduser("~/.vrchatpickle") #*Should* work on linux/windows/mac
baseUrl = "https://api.vrchat.cloud/api/1"

class Session:
     def __init__(self, maxcount=30):
      self.sleepCount = 0
      self.sleepCountMax = maxcount
      self.s = requests.session()
      self.s.headers['User-Agent'] = "wfscans/vrcutil"
      self.userId= ""
     def count(self):
      if self.sleepCount >= self.sleepCountMax:
       print("night night zzz...(5)")
       time.sleep(5)
       self.sleepCount = 0
      else:
       self.sleepCount += 1
     def mod(self, args):
        if args[0].startswith("/"):
            l = list(args)
            l[0] = baseUrl + l[0]
            return tuple(l)
     def get(self, *args, **kwargs):
      self.count()
      args = self.mod(args)
      return self.s.get(*args, **kwargs)
     def post(self, *args, **kwargs):
      self.count()
      args = self.mod(args)
      return self.s.post(*args, **kwargs)
     def put(self, *args, **kwargs):
      self.count()
      args = self.mod(args)
      return self.s.put(*args, **kwargs)
     def delete(self, *args, **kwargs):
      self.count()
      args = self.mod(args)
      return self.s.delete(*args, **kwargs)
     def head(self, *args, **kwargs):
      self.count()
      args = self.mod(args)
      return self.s.head(*args, **kwargs)

def login():
    print("Please login")
    r = s.get(f"/auth/user", headers={'Authorization':f'Basic {base64.b64encode((input("Username: ") + ":" + getpass.getpass()).encode()).decode()}'})
    if r.status_code != 200:
        raise Exception("failed to login")
    else:
        print(f"INFO logged-in as {r.json()['displayName']}")
        s.userId = r.json()['id']
    with open(configPath, 'wb') as f:
        pickle.dump(s.s.cookies, f)

def logout():
    s.put(f"/logout")
    os.remove(configPath)
    print("INFO logged out")

s = Session()

if os.path.exists(configPath):
    with open(configPath, 'rb') as f:
        s.s.cookies = pickle.load(f)
    r = s.get(f"/auth/user")
    if r.status_code == 401:
        print("WARNING cached login expired")
        login()
    elif r.status_code != 200:
        raise Exception(f"failed to verify auth token from {configPath}")
    print(f"INFO logged-in as {r.json()['displayName']}")
    s.userId = r.json()['id']
else:
    login()
