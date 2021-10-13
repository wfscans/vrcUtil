import vutil
import vrcfav
import os
import json
import argparse

def getFavgroup(groupType):
    #groupType:world,friend,avatar
    f = []
    offset = 0
    r = vutil.rq("GET", f"/favorites?type={groupType}&n=100&offset=0")
    while r[1].content != b"[]":
        f.extend(r[1].json())
        offset+=100
        vutil.sleep.count()
        r = vutil.rq("GET", f"/favorites?type={groupType}&n=100&offset={offset}")
    return f

def search(sType):
    f = []
    offset = 0
    r = vutil.rq("GET", f"/{sType}?releaseStatus=all&organization=vrchat&sort=updated&order=descending&user=me&n=100&offset=0")
    while r[1].content != b"[]":
        f.extend(r[1].json())
        offset+=100
        vutil.sleep.count()
        r = vutil.rq("GET", f"/{sType}?releaseStatus=all&organization=vrchat&sort=updated&order=descending&user=me&n=100&offset={offset}")
    return f

def friends():
    f = []
    offset = 0
    r = vutil.rq("GET", "/auth/user/friends?n=100&offset=0&offline=flase")
    while r[1].content != b"[]":
        f.extend(r[1].json())
        offset+=100
        vutil.sleep.count()
        r = vutil.rq("GET", f"/auth/user/friends?n=100&offset={offset}&offline=flase")
    offset = 0
    vutil.sleep.count()
    r = vutil.rq("GET", "/auth/user/friends?n=100&offset=0&offline=true")
    while r[1].content != b"[]":
        f.extend(r[1].json())
        offset+=100
        vutil.sleep.count()
        r = vutil.rq("GET", f"/auth/user/friends?n=100&offset={offset}&offline=true")
    return f

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1

def backup():
    u = vutil.rq("GET", "/auth/user")[1].json()
    uu = vutil.rq("GET", "/auth/user")[1].json()['username']
    groupNames = vutil.rq("GET", "/favorite/groups?n=100")[1].json()

    os.makedirs(f"{uu}_backup",exist_ok=True)
    print(f"INFO Creating {uu}_backup in current directory")

    with open(f"{uu}_backup/groupNames.json", 'w') as f:
        f.write(json.dumps(groupNames, indent=4))
    print(f"INFO Backed up group names")

    with open(f"{uu}_backup/user.json", 'w') as f:
        f.write(json.dumps(u, indent=4))
    print(f"INFO Backed up user information")

    fr = friends()
    fg = getFavgroup("friend")
    with open(f"{uu}_backup/friends.json", 'w') as f:
        f.write(json.dumps(fr,indent=4))
    print(f"INFO Backed up friend list")
    with open(f"{uu}_backup/friendGrouped.json", 'w') as f:
        f.write(json.dumps(fg,indent=4))
    print(f"INFO Backed up grouped friends")

    with open(f"{uu}_backup/friends_simple.txt", 'w') as f:
     ft = ""
     for fren in fr:
        i = find(fg, 'favoriteId', fren['id'])
        if i != -1:
            ft += f"{fren['displayName']} - {fg[i]['tags'][0]}\n"
        else:
            ft += fren['displayName'] + "\n"
        for group in ['group_0','group_1', 'group_2']:
            i = find(groupNames, 'name', group)
            if i != -1:
                ft = ft.replace(group, groupNames[i]['displayName'])
     f.write(ft)

    with open(f"{uu}_backup/favWorlds.json", 'w') as f:
        f.write(json.dumps(getFavgroup('world'),indent=4))
    print(f"INFO Backed up world favorites")
    with open(f"{uu}_backup/myWorlds.json", 'w') as f:
        f.write(json.dumps(search("worlds"),indent=4))
    print(f"INFO Backed up user created world info")

    with open(f"{uu}_backup/avatars.json", 'w') as f:
        f.write(json.dumps(getFavgroup('avatar'),indent=4))
    print(f"INFO Backed up avatar favorites")
    with open(f"{uu}_backup/myAvatars.json", 'w') as f:
        f.write(json.dumps(search("avatars"),indent=4))
    print(f"INFO Backed up user created avatar info")

def restore():
    with open(f"{args.r}/groupNames.json", 'r') as f:
        fo = json.loads(f.read())
        print("INFO setting group names")
        for group in fo:
            r = vutil.rq("PUT", f"/favorite/group/{group['type']}/{group['name']}/{vutil._userId}", body={'displayName': group['displayName'], 'visibility': group['visibility']})
            if r[0]:
                print(f"INFO {group['name']} changed to name {group['displayName']} with visibility {group['visibility']}")
            elif r[1].status_code == 400:
                print(f"WARNING {url} - {r[1].json()['error']['message']}")
            else:
                print(f"ERROR {group['name']} failed to update status code {r[1].status_code}")
                try:
                    print(f"ERROR {r[1].json()['error']['message']}")
                except:
                    pass

        with open(f"{args.r}/favWorlds.json", 'r') as f:
            fo = json.loads(f.read())
            fo.reverse()
        print("INFO setting up world favorites")
        for world in fo:
            vrcfav.fav(world['favoriteId'],world['tags'][0])

        with open(f"{args.r}/avatars.json", 'r') as f:
            fo = json.loads(f.read())
            fo.reverse()
        print("INFO setting up avatar favorites")
        for fav in fo:
            vrcfav.fav(fav['favoriteId'],fav['tags'][0],'avatar')

        fo = input("Would you like to your uploaded worlds that were marked as public to be added to your favorites?(y/n):")

        if fo.lower() == "y":
            print("INFO adding your uploaded public worlds to the first world list")
            with open(f"{args.r}/myWorlds.json", 'r') as f:
                fo = json.loads(f.read())
            for world in fo:
                if world['releaseStatus'] == "public":
                    vrcfav.fav(world['id'],'worlds1')
                else:
                    print(f"WARNING {world['name']} was not set to public - {world['id']}")

        fo = input("Would you like to your uploaded avatars that were marked as public to be added to your favorites?(y/n):")

        if fo.lower() == "y":
            print("INFO adding your uploaded public avatars to the avatar list")
            with open(f"{args.r}/myAvatars.json", 'r') as f:
                fo = json.loads(f.read())
            for fav in fo:
                if fav['releaseStatus'] == "public":
                    vrcfav.fav(fav['id'],'avatars1','avatar')
                else:
                    print(f"WARNING {fav['name']} was not set to public - {fav['id']}")
        print(f"INFO Your friend list can be found at {args.r}/friends_simple.txt.\nINFO It is also provided in a raw form via json files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup/Restore", epilog="example:\nbackup -b\nbackup -r <folder>\n", formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-b', action='store_true', help='backup your account')
    parser.add_argument('-r', action='store', help='restore account')
    parser.add_argument('-l', action='store_true', help='logout of account')
    args = parser.parse_args()
    if args.l:
        vutil.logout()
    elif args.b:
        backup()
    elif args.r:
        restore()
    else:
        parser.print_help()
