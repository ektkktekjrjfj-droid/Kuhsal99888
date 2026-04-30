import telebot
import requests
import time
import threading
import os
import random
import re
import gc
from pymongo import MongoClient
from flask import Flask
from telebot import types

# --- RENDER WEB FIX (Ye Render ko crash hone se rokta hai) ---
app = Flask(__name__)
@app.route('/health')
def health_check():
    return "Bot is Running", 200

def run_flask():
    # Render automatically sets PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- CONFIG ---
API_TOKEN = '8300468544:AAF9Q6eC3jBgMzCkJXPebKW-R6d-74BWZO0'
ADMIN_ID = 6932403164
MONGO_URI = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")
session = requests.Session() # Memory bachaane ke liye session use kiya

# --- DATABASE ---
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client['KushalPremiumStore']
users_col = db['users']
history_col = db['history']

# --- OTP EXTRACTOR ---
def get_clean_otp(text):
    match = re.search(r'\b\d{4,8}\b', text)
    return match.group(0) if match else "NOT FOUND"

# --- STABLE BACKGROUND ENGINE ---
def background_otp_checker():
    while True:
        try:
            # Sirf un users ko check karo jin ke paas active token hai
            active_users = list(users_col.find({"token": {"$exists": True}}))
            
            for user in active_users:
                uid = user['uid']
                email = user['email']
                token = user['token']
                last_id = user.get('last_id', '0')

                headers = {"Authorization": f"Bearer {token}"}
                try:
                    resp = session.get("https://api.mail.tm/messages", headers=headers, timeout=5).json()
                    msgs = resp.get('hydra:member', [])
                    
                    if msgs:
                        m_id = msgs[0]['id']
                        if str(m_id) != str(last_id):
                            # Naya message aaya hai
                            detail = session.get(f"https://api.mail.tm/messages/{m_id}", headers=headers, timeout=5).json()
                            full_text = f"{detail.get('intro', '')} {detail.get('subject', '')}"
                            otp = get_clean_otp(full_text)
                            
                            design = (
                                f"📩 <b>New Mail Received!</b>\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"📧 <b>To:</b> <code>{email}</code>\n"
                                f"📝 <b>Sub:</b> {detail.get('subject')}\n"
                                f"━━━━━━━━━━━━━━━━━━\n"
                                f"⚡ <b>OTP:</b> <code>{otp}</code>\n"
                                f"━━━━━━━━━━━━━━━━━━"
                            )
                            bot.send_message(uid, design)
                            users_col.update_one({"uid": uid}, {"$set": {"last_id": m_id}})
                except:
                    continue
            
            gc.collect() # Har loop ke baad memory saaf karo
            time.sleep(4) # CPU usage kam rakhne ke liye 4 sec sleep
            
        except Exception as e:
            print(f"Loop Error: {e}")
            time.sleep(10)

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def welcome(m):
    uid = m.chat.id
    name = m.from_user.first_name
    mention = f"<a href='tg://user?id={uid}'>{name}</a>"
    
    # User Photo fetch logic
    welcome_msg = f"👋 <b>Oye {mention}!</b>\n\nWelcome to <b>Kushal Premium Store</b>.\nID: <code>{uid}</code>\n\nBhai, niche wala button dabao naya email lene ke liye."
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📧 Generate Email", callback_data="gen"))
    
    try:
        photos = bot.get_user_profile_photos(uid)
        if photos.total_count > 0:
            bot.send_photo(uid, photos.photos[0][-1].file_id, caption=welcome_msg, reply_markup=markup)
        else:
            bot.send_message(uid, welcome_msg, reply_markup=markup)
    except:
        bot.send_message(uid, welcome_msg, reply_markup=markup)

# --- GENERATE EMAIL ---
@bot.callback_query_handler(func=lambda call: call.data == "gen")
def gen_email(call):
    uid = call.message.chat.id
    bot.answer_callback_query(call.id, "♻️ Generating...")
    
    try:
        dom = session.get("https://api.mail.tm/domains").json()['hydra:member'][0]['domain']
        email = f"kushal{random.randint(100,999)}@{dom}"
        pwd = "password123"
        
        session.post("https://api.mail.tm/accounts", json={"address": email, "password": pwd})
        token_data = session.post("https://api.mail.tm/token", json={"address": email, "password": pwd}).json()
        token = token_data.get('token')
        
        if token:
            users_col.update_one({"uid": uid}, {"$set": {"email": email, "token": token, "last_id": "0"}}, upsert=True)
            history_col.insert_one({"uid": uid, "email": email, "date": time.strftime("%Y-%m-%d")})
            bot.send_message(uid, f"✅ <b>Email Taiyar Hai:</b>\n<code>{email}</code>\n\n<i>Waiting for OTP... (Keep this chat open)</i>")
    except:
        bot.send_message(uid, "❌ Server Down. Try again later.")

# --- BROADCAST SYSTEM ---
@bot.message_handler(commands=['broadcast'])
def bc_handler(m):
    if m.chat.id == ADMIN_ID:
        msg = bot.reply_to(m, "📢 Send me the message (Text or Photo with Caption)")
        bot.register_next_step_handler(msg, perform_bc)

def perform_bc(m):
    users = list(users_col.find({}, {"uid": 1}))
    success = 0
    for u in users:
        try:
            if m.content_type == 'photo':
                bot.send_photo(u['uid'], m.photo[-1].file_id, caption=m.caption)
            else:
                bot.send_message(u['uid'], m.text)
            success += 1
            time.sleep(0.1) # Flood wait se bachne ke liye
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ Broadcast sent to {success} users.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # 1. Flask for Health Check (Render mandatory)
    threading.Thread(target=run_flask, daemon=True).start()
    
    # 2. OTP Checker Loop
    threading.Thread(target=background_otp_checker, daemon=True).start()
    
    # 3. Start Bot Polling
    print(">>> Bot is starting...")
    bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
