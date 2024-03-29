import telebot
import os
import json
import random

TOKEN = os.environ.get("BCLOUD_TG_TOKEN")
HOST = os.environ.get("BCLOUD_HOST")
PORT = int(os.environ.get("BCLOUD_PORT"))
ADMIN = int(os.environ.get("BCLOUD_TG_ADMIN"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["shorturl"])
def text_handler(message):
    if "http" in message.text:
        urls_db = json.load(open("data/urls.json"))
        url_id = str(random.randint(10000, 100000))
        url_obj = {"id": url_id, "usages": 0, "link": message.text.split()[1]}
        urls_db[url_id] = url_obj
        json.dump(urls_db, open("data/urls.json", "w"))
        if PORT in [80, 443]:
            bot.reply_to(message, f"http://{HOST}/u/{url_id}")
        else:
            bot.reply_to(message, f"http://{HOST}:{PORT}/u/{url_id}")

@bot.message_handler(commands=["banip"])
def banip_cmd(message):
    if (message.from_user.id != ADMIN):
        return None
    blacklist = json.load(open("data/blacklist.json"))
    args = message.text.split()
    if (len(args) == 2):
        blacklist["ip"].append(args[1])
        json.dump(blacklist, open("data/blacklist.json", "w"))
        bot.reply_to(message, f"IP {args[1]} забанен!")

@bot.message_handler(commands=["blacklist"])
def blacklist_cmd(message):
    if (message.from_user.id != ADMIN):
        return None
    blacklist = json.load(open("data/blacklist.json"))
    bot.reply_to(message, "\n".join(blacklist["ip"]))

@bot.message_handler(commands=["urls"])
def urls_cmd(message):
    if (message.from_user.id != ADMIN):
        return None
    urls_db = json.load(open("data/urls.json"))
    reply = "Статистика переходов по URL за всё время:\n\n"
    if PORT in [80, 443]:
        index = f"http://{HOST}/u/"
    else:
        index = f"http://{HOST}:{PORT}/u/"
    for url in urls_db.keys():
        reply += f"`{index + urls_db[url]['id']}` - `{urls_db[url]['link']}`:\n{str(urls_db[url]['usages'])} переходов\n\n"
    bot.reply_to(message, reply, parse_mode="markdown")

@bot.message_handler(content_types=["document", "audio", "photo", "video", "gif"])
def file_handler(message):
    if (message.from_user.id != ADMIN):
        return None
    if message.document:
        file_info = bot.get_file(message.document.file_id)
    elif message.audio:
        file_info = bot.get_file(message.audio.file_id)
    elif message.photo:
        file_info = bot.get_file(message.photo[-1].file_id)
    elif message.video:
        file_info = bot.get_file(message.video.file_id)
    elif medsage.gif:
        file_info = bot.get_file(message.gif.file_id)
    print(file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    if hasattr(file_info, "file_name"):
        file_name = file_info.file_name
    else:
        file_name = str(random.randint(10000, 99999999)) + "." + file_info.file_path.split(".")[-1]
    src = "uploads/" + file_name
    with open(src, "wb") as f:
        f.write(downloaded_file)
    if PORT in [80, 443]:
        index = f"http://HOST"
    else:
        index = f"http://{HOST}:{str(PORT)}"
    bot.reply_to(message, f"{index}/uploads/{file_name}")

if __name__ == "__main__":
    bot.infinity_polling()
