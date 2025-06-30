import asyncio
import os
import sys
from telethon import TelegramClient

API_ID = 611335
API_HASH = "d524b414d21f4d37f08684c1df41ac9c"


BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHATID")
MESSAGE_THREAD_ID = os.environ.get("MESSAGE_THREAD_ID")
DEVICE = os.environ.get("DEVICE")
kernelversion = os.environ.get("KernelVer")
KPM= os.environ.get("KPM")
lz4kd= os.environ.get("LZ4KD")
ksuver= os.environ.get("KSUVERSIONS")
MSG_TEMPLATE = """
**New Build Published!**
#{device}
```Kernel Info
kernelver: {kernelversion}
KsuVersion: {Ksuver}
KPM: {kpm}
Lz4kd: {Lz4kd}
```
testing for auto push...
""".strip()


def get_caption():
    msg = MSG_TEMPLATE.format(
        device=DEVICE,
        kernelversion=kernelversion,
        kpm=KPM,
        Lz4kd=lz4kd,
        Ksuver=ksuver,
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
    async with await TelegramClient(session=session_dir, api_id=API_ID, api_hash=API_HASH).start(bot_token=BOT_TOKEN) as bot:
        caption = [""] * len(files)
        caption[-1] = get_caption()
        print("[+] Caption: ")
        print("---")
        print(caption)
        print("---")
        print("[+] Sending")
        await bot.send_file(entity=CHAT_ID, file=files, caption=caption, reply_to=MESSAGE_THREAD_ID, parse_mode="markdown")
        print("[+] Done!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[-] An error occurred: {e}")
