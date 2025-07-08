import asyncio
import os
import sys
import requests


BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHATID")
MESSAGE_THREAD_ID = os.environ.get("MESSAGE_THREAD_ID")
DEVICE = os.environ.get("DEVICE")
KPM= os.environ.get("KPM")
lz4kd= os.environ.get("LZ4KD")
MSG_TEMPLATE = """
**New Build Published!**
#{device}
```Kernel Info
kernelver: {kernelversion}
KsuVersion: {Ksuver}
KPM: {kpm}
lz4kd: {Lz4kd} lz4&zstd: {lz4_zstd}
```
十分感谢yc佬对本自动推送bot做出的贡献❤️
""".strip()


def get_caption():
    msg = MSG_TEMPLATE.format(
        device=DEVICE,
        kernelversion=kernelversion,
        kpm=KPM,
        Lz4kd=lz4kd,
        Ksuver=ksuver,
        lz4_zstd=check_lz4_zstd(),
    )
    if len(msg) > 1024:
        return f"{DEVICE}{kernelversion}"
    return msg


def check_environ():
    global CHAT_ID, MESSAGE_THREAD_ID
    if BOT_TOKEN is None:
        print("[-] Invalid BOT_TOKEN")
        exit(1)
    if CHAT_ID is None:
        print("[-] Invalid CHAT_ID")
        exit(1)
    else:
        try:
            CHAT_ID = int(CHAT_ID)
        except:
            pass
    if MESSAGE_THREAD_ID is not None and MESSAGE_THREAD_ID != "":
        try:
            MESSAGE_THREAD_ID = int(MESSAGE_THREAD_ID)
        except:
            print("[-] Invaild MESSAGE_THREAD_ID")
            exit(1)
    else:
        MESSAGE_THREAD_ID = None
    get_versions()

def send_file(entity:int,file:str,caption:str,reply_to:int,parse_mode:str):
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    data = {
        "chat_id": entity,
        "parse_mode": parse_mode,
        "caption": caption,
        }
    if reply_to:
        data["message_thread_id"] = reply_to
    with open(file,"rb") as file_data:
        files = {"document": file_data}
        response = requests.post(api_url,data=data,files=files)
    if response.status_code != 200:
        raise Excpetion(f"Request failed:{response.status_code}.{response.text}")
    return response.json()

def get_kernel_versions():
    version=""
    patchlevel=""
    sublevel=""

    try:
        with open("Makefile",'r') as file:
            for line in file:
                if line.startswith("VERSION"):
                    version = line.split('=')[1].strip()
                elif line.startswith("PATCHLEVEL"):
                    patchlevel = line.split('=')[1].strip()
                elif line.startswith("SUBLEVEL"):
                    sublevel = line.split('=')[1].strip()
                elif line.startswith("#"): # skip comments
                    continue
                else:
                    break
    except FileNotFoundError:
        raise
    return f"{version}.{patchlevel}.{sublevel}"

def get_versions():
    global kernelversion,ksuver
    current_work=os.getcwd()
    os.chdir(current_work+"/kernel_workspace/kernel_platform/common") #除非next
    kernelversion=get_kernel_versions()
    os.chdir(os.getcwd()+"/../KernelSU")
    ksuver=os.popen("echo $(git describe --tags $(git rev-list --tags --max-count=1))-$(git rev-parse --short HEAD)@$(git branch --show-current)").read().strip()
    os.chdir(current_work)

def check_lz4_zstd():
    global lz4kd
    if lz4kd == "Off":
        return "On"
    else:
        return "Off"
    return "Off"

async def main():
    print("[+] Uploading to telegram")
    check_environ()
    files = sys.argv[1:]
    print("[+] Files:", files)
    if len(files) <= 0:
        print("[-] No files to upload")
        exit(1)
    print("[+] Logging in Telegram with bot")
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    session_dir = os.path.join(script_dir, "ksubot")
    caption = [""] * len(files)
    caption[-1] = get_caption()
    print("[+] Caption: ")
    print("---")
    print(caption)
    print("---")
    print("[+] Sending")
    send_file(entity=CHAT_ID, file=files[0], caption=caption, reply_to=MESSAGE_THREAD_ID, parse_mode="markdown")
    print("[+] Done!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[-] An error occurred: {e}")
