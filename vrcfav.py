#!/usr/bin/python3
import vutil
import traceback
import argparse

_v = "1.01"

def getId(s):
     a = s.find("wrld_")
     b = s.find("&", a)
     if (b==-1):
         return s[a:]
     else:
         return s[a:b]

def fav(url):
    r = vutil.rq("POST", "/favorites", {"type":"world", "favoriteId": url, "tags": [args.w]})
    if r[0]:
        print(f"INFO {url} has been added to {args.w}")
    elif r[1].status_code == 400:
        print(f"WARNING {url} - {r[1].json()['error']['message']}")
    else:
        print(f"ERROR {url} returned status code {r[1].status_code}")
        try:
            print(f"ERROR {r[1].json()['error']['message']}")
        except Exception:
            pass

def unfav(url):
    r = vutil.rq("DELETE", f"/favorites/{url}")
    if r[0]:
        print(f"INFO {url} has been removed")
    elif r[1].status_code == 400:
        print(f"WARNING {url} - {r[1].json()['error']['message']}")
    else:
        print(f"ERROR {url} returned status code {r[1].status_code}")
        try:
            print(f"ERROR {r[1].json()['error']['message']}")
        except Exception:
            pass

if __name__ == "__main__":

   example=f"""Examples:
   vrcfav <url>/<id>
   vrcfav -d <url>/<id>
   vrcfav -f <filename>
   vrcfav -w worlds3 <url>/<id>
   vrcfav -w "Really long name" -f <filename>
   vrcfav "https://vrchat.com/home/launch?worldId=wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd&instanceId=18692~hidden(usr_..."
   (not needed for when in a file but needed to escape commandline special symbols)

   File input is one url a line:
   https://vrchat.com/home/world/wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd
   https://vrchat.com/home/launch?worldId=wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd
   https://vrchat.com/home/launch?worldId=wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd&instanceId=54932
   https://vrchat.com/home/launch?worldId=wrld_4432ea9b-729c-46e3-8eaf-846aa0a37fdd&instanceId=18692~hidden(usr_...
   """

   parser = argparse.ArgumentParser(description=f'vrchatfav {_v} - Easily modify your worlds list from outside the game!', epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter)
   parser.add_argument('-f', action='store_true', help='process file instead of single url')
   parser.add_argument('-w', action='store', help='world folder name (default: worlds3)', default="worlds3")
   parser.add_argument('-d', action='store_true', help='remove world from favorites')
   parser.add_argument('url', type=str, help='worldId/link')
   args = parser.parse_args()

   try:
    if args.f:
        with open(args.url, 'r') as f:
            for line in f:
                if args.d:
                    unfav(getId(line.strip))
                else:
                    fav(getId(line.strip()))
                vutil.sleep.count()
    else:
        if args.d:
            unfav(getId(args.url))
        else:
            fav(getId(args.url))
   except Exception:
    traceback.print_exc()
