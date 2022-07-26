from database import add_data, update_data, select_data, load_db
from client import uploader, colors
from os import system, name
from tinytag import TinyTag
from pathlib import Path
from confing import info

up = uploader(info.auth)
load_db()

def main(urlfile):
    up.downloader(urlfile)
    filename = urlfile.split("/")[-1]
    return filename

if not info.file:
    file = input(f"{colors.YELLOW}Enter your path file / url: {colors.RESET}")
else:
    file = info.file

if not info.file:
    path = file if not "http" in file else main(file)
else:
    path = info.file if not "http" in info.file else main(info.file)

Size = Path(path).stat().st_size

if select_data() == None:
    add_data(Size)
else:
	size_new = int(select_data()[0] + Size)
	update_data(size_new)

if name == "nt":
    system("cls")
else:
    system("clear")

if not info.guid:
    while True:
        try:
            chats = up.getChats()["data"]["chats"]
            break
        except:continue

    target, n = {}, 0
    for chat in chats:
        n += 1
        if chat["abs_object"]["type"] == "User":
            title = chat["abs_object"].get("first_name")
            target[n] = chat["abs_object"]["object_guid"]
            print(f"{colors.YELLOW}[{n}]{colors.RESET}-{colors.GREEN}({title}){colors.RESET}")
        else:
            title = chat["abs_object"].get("title")
            target[n] = chat["abs_object"]["object_guid"]
            print(f"{colors.YELLOW}[{n}]{colors.RESET}-{colors.GREEN}({title}){colors.RESET}")
    num = int(input(f"\n{colors.YELLOW}Enter your target number => {colors.RESET}"))
    
    if name == "nt":
        system("cls")
    else:
        system("clear")
        
    target = target[num]
else:
    target = info.guid

print(f"""{colors.CYAN}[1]-[Gif]
{colors.CYAN}[2]-[Image]
{colors.CYAN}[3]-[movie]
{colors.CYAN}[4]-[music]
{colors.CYAN}[5]-[voice]
{colors.CYAN}[6]-[File]
{colors.CYAN}[7]-[Exit]
{colors.CYAN}[8]-[Get the volume uploaded by the user]{colors.RESET}""")

Type = int(input(f"{colors.YELLOW}File sending type: {colors.RESET}"))

if name == "nt":
    system("cls")
else:
    system("clear")

if Type == 1:
    #send gif
    while True:
        try:
            up.sendgif(target, path, height=720, width=720, caption=info.cap)
            break
        except:continue

elif Type == 2:
    #send image
    while True:
        try:
            up.sendimage(target, path, caption=info.cap)
            break
        except:continue

elif Type == 3:
    #send movie
    while True:
        try:
            dur = TinyTag.get(path).duration * 1000
            up.sendmovie(target, path, height=720, width=720, duration=dur,caption=info.cap)
            break
        except:continue

elif Type == 4:
    #send music
    while True:
        try:
            dur = TinyTag.get(path).duration
            arti = dur = TinyTag.get(path).artist
            up.sendmusic(target, path, artist=arti, duration=dur, caption=info.cap)
            break
        except:continue

elif Type == 5:
    #send voice
    while True:
        try:
            dur = TinyTag.get(path).duration * 1000
            up.sendvoice(target, path, duration=dur, caption=info.cap)
            break
        except:continue

elif Type == 6:
    #send file
    while True:
        try:
            up.sendfile(target, path, caption=info.cap)
            break
        except:continue

elif Type == 7:
    exit()

elif Type == 8:
    print(f"{colors.GREEN} {round((select_data()[0] / 1024) / 1024)} {colors.RESET} Mb")