import io
import requests
import telebot

TELEGRAM_TOKEN = '8512531507:AAE-mpzcpKDKjxUI3NHj72QLbzgIExOY-Js'
DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1540999790043598910/LKFnqk7rKWQrP-3bOt-cwpiKQexj6SjqVfIKj_Th8lEX7UNYGGNLiozY_XcmNwE_ungL'

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Nhận tin nhắn chữ từ Channel, Group lẫn Chat riêng
@bot.message_handler(content_types=['text'])
@bot.channel_post_handler(content_types=['text'])
def forward_text(message):
    payload = {"content": message.text}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("Đã gửi tin nhắn Text sang Discord!")
    except Exception as e:
        print(f"Lỗi gửi Text: {e}")

# Nhận hình ảnh từ Channel, Group lẫn Chat riêng
@bot.message_handler(content_types=['photo'])
@bot.channel_post_handler(content_types=['photo'])
def forward_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    files = {'file': ('image.jpg', io.BytesIO(downloaded_file), 'image/jpeg')}
    payload = {}
    if message.caption:
        payload['content'] = message.caption

    try:
        requests.post(DISCORD_WEBHOOK_URL, data=payload, files=files)
        print("Đã gửi ảnh sang Discord!")
    except Exception as e:
        print(f"Lỗi gửi ảnh: {e}")

print("Bot đang chạy và lắng nghe tin nhắn...")
bot.infinity_polling()