import io
import os
import threading
from flask import Flask
import requests
import telebot

# Tạo web server nhỏ để Render nhận diện được port và không tắt dịch vụ
app = Flask(__name__)


@app.route("/")
def home():
  return "Bot is running!"


def run_web():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# Khởi chạy web server ở một luồng riêng biệt
t = threading.Thread(target=run_web)
t.start()

TELEGRAM_TOKEN = '8512531507:AAGuwTWyxrbf5anIhwApLo_SGjFL2UkuI9k'
DISCORD_WEBHOOK_URL = (
    'https://discord.com/api/webhooks/1540999790043598910/LKFnqk7rKWQp-3b0t-cwpIKQexJ65jqVFlkJ_Th81EX7UNYGGNLiozY_XcmNwE_ungL'
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Nhận tin nhắn chữ từ Channel, Group lẫn Chat riêng
@bot.message_handler(content_types=['text'])
@bot.channel_post_handler(content_types=['text'])
def forward_text(message):
  payload = {'content': message.text}
  try:
    requests.post(DISCORD_WEBHOOK_URL, json=payload)
    print('Đã gửi tin nhắn Text sang Discord!')
  except Exception as e:
    print(f'Lỗi gửi Text: {e}')


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
    print('Đã gửi ảnh sang Discord!')
  except Exception as e:
    print(f'Lỗi gửi ảnh: {e}')


print('Bot đang chạy và lắng nghe tin nhắn...')
bot.infinity_polling()
