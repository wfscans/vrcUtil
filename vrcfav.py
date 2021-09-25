#!/usr/bin/python3
import os
import requests
import json
import traceback
import base64
import pickle
import argparse
import time

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
_sleep = limitCounter()
_v = "1.00"

def rq(method, url, body=None, header={}):
    if method == "GET":
        r = _s.get(url, headers=header)
    elif method == "POST":
        r = _s.post(url, data=body)
    elif method == "PUT":
        r = _s.put(url)
    else:
        raise Exception("invalid request type given")
    if r.status_code != 200:
        return [False, r]
    else:
        return [True, r]

def getId(s):
     a = s.find("wrld_")
     b = s.find("&", a)
     if (b==-1):
         return s[a:]
     else:
         return s[a:b]

def login():
    print("Please login:")
    r = rq("GET", "https://api.vrchat.cloud/api/1/auth/user", header={'Authorization':f'Basic {base64.b64encode((input("Username ") + ":" + input("Password ")).encode()).decode()}'})
    if not r[0]:
        raise Exception("failed to login")
    else:
        print(f"INFO logged-in as {json.loads(r[1].content)['displayName']}")
    with open(_configPath, 'wb') as f:
        pickle.dump(_s.cookies, f)

def fav(url):
    r = rq("POST", "https://api.vrchat.cloud/api/1/favorites", {"type":"world", "favoriteId": url, "tags": [args.w]})
    if r[0]:
        print(f"INFO {getId(url.strip())} has beened added to {args.w}")
    elif r[1].status_code == 400:
        print(f"WARNING {getId(url.strip())} - {json.loads(r[1].content)['error']['message']}")
    else:
        print(f"ERROR {getId(url.strip())} returned status code {r[1].status_code}")
        try:
            print(f"ERROR {json.loads(r[1].content)['error']['message']}")
        except Exception:
            pass


if __name__ == "__main__":

   example=f"""Examples:
   vrcfav <url>
   vrcfav -f <filename>
   vrcfav -w worlds3 <url>
   vrcfav -w "Really long name" -f <filename>
   vrcfav "https://vrchat.com/home/launch?worldId=wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd&instanceId=18692~hidden(usr_..."

   File input is one url a line:
   https://vrchat.com/home/world/wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd
   https://vrchat.com/home/launch?worldId=wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd
   https://vrchat.com/home/launch?worldId=wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd&instanceId=54932
   https://vrchat.com/home/launch?worldId=wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd&instanceId=18692~hidden(usr_...
   """

   parser = argparse.ArgumentParser(description=f'vrchatfav {_v} - Easily add world(s) to your world list from outside the game!', epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter)
   parser.add_argument('-f', action='store_true', help='process file instead of single url')
   parser.add_argument('-w', action='store', help='world folder name (default: worlds3)', default="worlds3")
   parser.add_argument('url', type=str, help='url for either the series or chapter')
   args = parser.parse_args()

   #print(args.f) #false if not given
   #print(args.w) #if not given will be "worlds3"
   #print(args.url) #url/filename

   if os.path.exists(_configPath):
    with open(_configPath, 'rb') as f:
        _s.cookies = pickle.load(f)
    r = rq("GET", "https://api.vrchat.cloud/api/1/auth/user")
    if not r[0]:
        if r[1].status_code == 401:
            print("WARNING cached login expired")
            login()
        else:
            raise Exception(f"failed to verify auth token from {_configPath}")
    print(f"INFO logged-in as {json.loads(r[1].content)['displayName']}")
   else:
    login()

   try:
    if args.f:
        with open(args.url, 'r') as f:
            for line in f:
                fav(getId(line.strip()))
                _sleep.count()
    else:
        fav(getId(args.url))
   except Exception:
    traceback.print_exc()

   #if not rq("PUT", "https://api.vrchat.cloud/api/1/logout")[0]:
   # print("ERROR Failed to logout")
