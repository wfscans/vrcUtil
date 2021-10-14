# vrcUtil

Written for python3.6 will prob work with future versions. Won't work with past version due to f-strings if I recall.

I assume most sane Windows users who might want to use this might not have python installed. So builds are automaticly provided by github cli - https://github.com/wfscans/vrcutil/releases/

# [How to use console apps](https://github.com/wfscans/vrcUtil/wiki)

# VRCFAV
A simple CLI script/program that allows you to add/remove worlds from your favorite list from outside the game. If you need help with options try `vrcfav -h`. You do need to run this from a powershell/command prompt(or maybe from a shortcut? Though it wouldn't pause at the end)

# SHAREME
A script that will track your current world and post it to a rentry.co paste that updates as you go. I did it in a way where you could easily add in new ways(twitter is pretty easy). I had it working with 4chan but currently am not releasing that functional. Feel free to do so yourself.

# BACKUP
A simple CLI app to backup/restore parts of a VRChat account. Currently supports: Basic User Account Infomation, Friends list, World Favorites, Uploaded World infomation, Avatar Favorites, Uploaded Avatar infomation, Custom lists(Avatar/Friends/Worlds). **Due to the design of VRChat private uploaded avatars/worlds can't be added to your favorited by a different account. Same can be said to abouy your friends list. A text file will have to do.**

* `python3 backup.py -b` backups up the currently logged in account to a folder in the current directory
* `python3 backup.py -l` logout of the current logged in account
* `python3 backup.py -r <username_backup>` username_backup is the path to the folder from the first step.

```
$ python3 backup.py -b
Please login
Username: user
Password: 
INFO logged-in as user
INFO Creating user_backup in current directory
INFO Backed up group names
INFO Backed up user information
INFO Backed up friend list
INFO Backed up grouped friends
INFO Backed up world favorites
INFO Backed up user created world info
INFO night night zzz...(5)
INFO Backed up avatar favorites
INFO Backed up user created avatar info
$ python3 backup.py -l
INFO logged-in as user
INFO logged out
$ python3 backup.py -r user_backup
Please login
Username: user2
Password: 
INFO logged-in as user2
INFO setting group names
INFO avatars1 changed to name CustomName with visibility private
INFO worlds1 changed to name CustomName2 with visibility private
...
INFO setting up world favorites
INFO wrld_3 has been added to worlds1
INFO wrld_3 has been added to worlds2
...
INFO setting up avatar favorites
INFO avtr_ has been added to avatars1
INFO avtr_ has been added to avatars1
...
Would you like to your uploaded worlds that were marked as public to be added to your favorites?(y/n):y
INFO adding your uploaded public worlds to the first world list
WARNING WorldName was not set to public - wrld_
Would you like to your uploaded avatars that were marked as public to be added to your favorites?(y/n):y
INFO adding your uploaded public avatars to the avatar list
WARNING avatar was not set to public - avtr_
INFO avtr_ has been added to avatars1
...
INFO Your friend list can be found at user_backup/friends_simple.txt.
INFO It is also provided in a raw form via json files.
```
