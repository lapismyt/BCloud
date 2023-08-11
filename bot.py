import telebot
import os

TOKEN = os.environ.get("BCLOUD_TG_TOKEN")
HOST = os.environ.get("BCLOUD_HOST")
PORT = int(os.environ.get("BCLOUD_PORT"))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=["document", "audio", "photo", "video"])
def file_handler(message):
    if message.document:
        file_info = bot.get_file(message.document.file_id)
    elif message.audio:
        file_info = bot.get_file(message.audio.file_id)
    elif message.photo:
        file_info = bot.get_file(message.photo[0].file_id)
    elif message.video:
        file_info = bot.get_file(message.video.file_id)
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
