import time
from threading import Thread
from flask import Flask
import telebot
import requests

# 1. إعداد سيرفر وهمي لتنبيه منصة Render ومنع النوم
app = Flask('')

@app.route('/')
def home():
    return "TikTok Downloader Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. إعداد وتطوير البوت باستخدام التوكن الخاص بك
BOT_TOKEN = "8974963729:AAF1ji7SzMoL1wBM4aLHqZfYsbo2Dl0FrTg"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط فيديو تيك توك (TikTok)، وسأقوم بتحميله لك بأعلى دقة وبدون حقوق (كعلامة مائية) وإرساله لك كملف وفيديو. 🚀")

@bot.message_handler(func=lambda message: True)
def handle_tiktok_download(message):
    url = message.text.strip()
    
    # التحقق من أن الرابط يخص تيك توك
    if "tiktok.com" not in url:
        bot.reply_to(message, "الرجاء إرسال رابط فيديو تيك توك صحيح.")
        return
        
    msg = bot.reply_to(message, "⏳ جاري جلب الفيديو وبدء التحميل بأعلى دقة، يرجى الانتظار...")
    
    try:
        # استخدام واجهة برمجة تطبيقات مجانية ومستقرة لتحميل تيك توك بدون علامة مائية
        api_url = f"https://www.tikwm.com/api/?url={url}"
        response = requests.get(api_url).json()
        
        if response.get("code") == 0:
            video_data = response["data"]
            video_url = video_data.get("play")  # رابط الفيديو بدون علامة مائية وبأعلى دقة
            title = video_data.get("title", "tiktok_video")
            
            # تحميل ملف الفيديو في الذاكرة لإرساله كملف (Document)
            video_bytes = requests.get(video_url).content
            
            # تسمية الملف
            file_name = f"video_{message.message_id}.mp4"
            
            # إرسال الفيديو كملف للحفاظ على الدقة الكاملة وبدون أي ضغط
            bot.send_document(
                message.chat.id, 
                visible_file_name=file_name, 
                document=video_bytes, 
                caption="📥 تم تحميل الفيديو كملف بكامل الدقة الأصلية وبدون علامة مائية!"
            )
            
            # حذف رسالة الانتظار
            bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            
        else:
            bot.edit_message_text("❌ عذراً، تعذر تحميل هذا الفيديو. تأكد من أن الرابط صحيح والحساب ليس خاصاً.", chat_id=message.chat.id, message_id=msg.message_id)
            
    except Exception as e:
        print(f"Error: {e}")
        bot.edit_message_text("❌ حدث خطأ أثناء معالجة الرابط، يرجى المحاولة مرة أخرى لاحقاً.", chat_id=message.chat.id, message_id=msg.message_id)

# تشغيل السيرفر والبوت معاً
if __name__ == "__main__":
    keep_alive()
    print("Bot is starting...")
    bot.infinity_polling()
