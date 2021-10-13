#!/usr/bin/python3
import vutil
import requests
import time

currentWorld=""
instanceId =""

def getShareLink(saveThumb=True):
    r = vutil.rq("GET", f"/users/{vutil._userId}")
    #r = vutil.rq("GET", f"/users/{id}")
    if r[0]:
        r = r[1].json()
        global currentWorld
        global instanceId
        iid = r['instanceId'][:r['instanceId'].find("~")]
        if currentWorld != r['worldId'] or instanceId != iid:
            currentWorld = r['worldId']
            instanceId = iid
            r = vutil.rq("GET", f"/instances/{currentWorld}:{r['instanceId']}/shortName")
            if r[0]:
                shareUrl = f"https://vrch.at/{r[1].content.decode()}"
                r = vutil.rq("GET", f"/worlds/{currentWorld}")
                if r[0]:
                    if saveThumb == False:
                        return [shareUrl,""]
                    r = vutil.rq("GET", r[1].json()['imageUrl'], baseUrl="")
                    if r[0]:
                        with open(f"temp.{r[1].headers['Content-Type'].split('/')[1]}", 'wb') as f:
                            f.write(r[1].content)
                        return [shareUrl, f.name]
                    else:
                        return [shareUrl, ""]
        else:
            return ["", ""]
    return ["error0 - no current world found(most likely)", ""]

def rentryNew(text, url="", ecode=""):
    r = requests.post("https://rentry.co/api/new", {'csrfmiddlewaretoken': csrf, 'url':url, 'edit_code':ecode, 'text':text}, headers={"Referer": 'https://rentry.co'}, cookies={'csrftoken':csrf})
    if r.status_code == 200:
        r = r.json()
        return r['url'],r['edit_code']
    else:
        raise Exception(f"request returned status code {r.status_code}")

def rentryEdit(text, url, ecode):
    r = requests.post(f'https://rentry.co/api/edit/{url[url.rfind("/")+1:]}', {'csrfmiddlewaretoken': csrf, 'edit_code': ecode, 'text': text}, headers={"Referer": 'https://rentry.co'}, cookies={'csrftoken': csrf})
    if r.status_code != 200:
        raise Exception(f"request returned status code {r.status_code}")


text = "Join me for some world hopping!\n"
csrf = requests.get("https://rentry.co").cookies['csrftoken']

r = getShareLink(False)
if r[0] != "" and not r[0].startswith("e"):
    text += r[0]
if currentWorld == "" or currentWorld == "offline":
    url, ecode = rentryNew(text)
else:
    url, ecode = rentryNew(text + " (current world)")
print(f"INFO url: {url} edit code: {ecode}")
print(f"INFO While edit code is provided anything added will be overwritten by the program on update!(atleast while the program is running)")
print(r[0])

while True:
    r = getShareLink(False)
    if r[0] != "" and not r[0].startswith("e"):
        text += "\n" + r[0]
        print(r[0])
        rentryEdit(text + " (current world)", url, ecode)
    time.sleep(60) #multi-thread drifting
