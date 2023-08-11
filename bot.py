import telebot
import os
import json
import random

TOKEN = os.environ.get("BCLOUD_TG_TOKEN")
HOST = os.environ.get("BCLOUD_HOST")
PORT = int(os.environ.get("BCLOUD_PORT"))

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
            bot.reply_to(message, f"{HOST}/u/{url_id}")
        else:
            bot.reply_to(message, f"{HOST}:{PORT}/u/{url_id}")

@bot.message_handler(content_types=["document", "audio", "photo", "video", "gif"])
def file_handler(message):
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
        file_name = str(file_info.file_id)[-5:] + "." + file_info.file_path.split(".")[-1]
    src = "uploads/" + file_name
    with open(src, "wb") as f:
        f.write(downloaded_file)
    if PORT in [80, 443]:
        index = HOST
    else:
        index = f"{HOST}:{str(PORT)}"
    bot.reply_to(message, f"{index}/uploads/{file_name}")

if __name__ == "__main__":
    bot.infinity_polling()
