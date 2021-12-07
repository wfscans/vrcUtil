import sys
if len(sys.argv) != 2:
    print("usage: skim rentry.co/sample or skim https://rentry.co/sample")
    exit()

def getId(s):
     a = s.find("wrld_")
     b = s.find("&", a)
     if (b==-1):
         return s[a:]
     else:
         return s[a:b]

print("Output will be printed to screen. If you are unable to highlight or would like it in a file. Please rerun the command with ' > file.txt' on the end. Example: skim rentry.co/sample > file.txt")
import vutil
r = vutil.s.get(f"{sys.argv[1]}/raw")
if r.status_code == 200:
    for line in r.content.decode().split("\n"):
        if line.startswith("http"):
            print(f"https://vrchat.com/home/world/{getId(vutil.s.get(line.split(' ')[0]).url)}")
else:
    print(f"Error! The url returned and error code! ({r.status_code})")
