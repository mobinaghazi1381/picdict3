import telebot
from googletrans import Translator
from ddgs import DDGS
import requests
import io

bot = telebot.TeleBot("7900941995:AAGVoKeX2QMf1Qzg8e3cQ5mU_LrrZzYp4EE")
translator = Translator()

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    word = message.text.strip()

    # ترجمه
    try:
        translation = translator.translate(word, src='en', dest='fa').text
        bot.reply_to(message, f"ترجمه: {translation}")
    except Exception:
        bot.reply_to(message, "خطا در ترجمه")

    # جستجوی تصویر و ارسال
    try:
        with DDGS() as ddgs:
            results = ddgs.images(word, max_results=1)
            if results:
                img_url = results[0]['image']

                # دانلود تصویر
                response = requests.get(img_url)
                if response.status_code == 200:
                    photo = io.BytesIO(response.content)
                    photo.name = 'image.jpg'  # اسم فایل برای تلگرام لازم است
                    bot.send_photo(message.chat.id, photo)
                else:
                    bot.send_message(message.chat.id, "خطا در دانلود تصویر")
            else:
                bot.send_message(message.chat.id, "تصویری یافت نشد.")
    except Exception as e:
        bot.send_message(message.chat.id, f"خطا در دریافت تصویر: {e}")

bot.infinity_polling()
