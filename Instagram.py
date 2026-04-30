import os
import telebot
import requests
import time
import threading
import random
import re
import gc
from flask import Flask, request
from pymongo import MongoClient
from telebot import types

# --- CONFIG & SECURE DATA ---
API_TOKEN = '8300468544:AAF9Q6eC3jBgMzCkJXPebKW-R6d-74BWZO0'
ADMIN_ID = 6932403164 
MONGO_URI = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Render Webhook URL (Apni Render URL yahan dalein)
WEBHOOK_URL = os.environ.get("RENDER_EXTERNAL_URL") 

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")
app = Flask(__name__)

# --- DATABASE CONNECTION ---
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client['KushalPremiumStore']
users_col = db['users']
history_col = db['history']

# --- RENDER WEBHOOK SETUP ---
@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook_setup():
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{API_TOKEN}")
    return "<h1>Kushal Premium Bot is Active!</h1>", 200

# --- OTP EXTRACTOR ---
def get_clean_otp(text):
    match = re.search(r'\b\d{4,8}\b', text)
    return match.group(0) if match else "---"

# --- FAST OTP ENGINE (STABLE) ---
def otp_checker():
    session = requests.Session()
    while True:
        try:
            active_users = list(users_col.find({"token": {"$exists": True}}))
            for user in active_users:
                headers = {"Authorization": f"Bearer {user['token']}"}
                r = session.get("https://api.mail.tm/messages", headers=headers, timeout=10).json()
                msgs = r.get('hydra:member', [])
                
                if msgs and str(msgs[0]['id']) != str(user.get('last_id', '0')):
                    m_id = msgs[0]['id']
                    detail = session.get(f"https://api.mail.tm/messages/{m_id}", headers=headers, timeout=10).json()
                    otp = get_clean_otp(detail.get('intro', '') + detail.get('subject', ''))
                    
                    # Exact Design
                    ui = (
                        f"📧 <b>Account:</b> <code>{user['email']}</code>\n"
                        f"📝 <b>Subject:</b> <i>{detail.get('subject')}</i>\n"
                        f"🔗 <b>Platform:</b> Instagram\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"⚡ <b>OTP CODE:</b> <code>{otp}</code>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"🔹 <i>Tap code to copy instantly</i>"
                    )
                    bot.send_message(user['uid'], ui, disable_web_page_preview=True)
                    users_col.update_one({"uid": user['uid']}, {"$set": {"last_id": m_id}})
            gc.collect()
            time.sleep(3) 
        except:
            time.sleep(10)

# --- START COMMAND (PHOTO + MENTION) ---
@bot.message_handler(commands=['start'])
def start(m):
    uid = m.chat.id
    name = m.from_user.first_name
    mention = f"<a href='tg://user?id={uid}'>{name}</a>"
    
    users_col.update_one({"uid": uid}, {"$set": {"name": name}}, upsert=True)
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📧 Get New Email", callback_data="gen"),
        types.InlineKeyboardButton("📊 My History", callback_data="his"),
        types.InlineKeyboardButton("🗑️ Clear Data", callback_data="clr")
    )
    
    welcome = f"🌟 <b>Welcome {mention}!</b>\n\n<b>KUSHAL PREMIUM STORE</b>\nStatus: <code>Online & Secure</code>\n\nBhai, niche diye buttons use karein!"
    
    try:
        photos = bot.get_user_profile_photos(uid)
        if photos.total_count > 0:
            bot.send_photo(uid, photos.photos[0][-1].file_id, caption=welcome, reply_markup=markup)
        else:
            bot.send_message(uid, welcome, reply_markup=markup)
    except:
        bot.send_message(uid, welcome, reply_markup=markup)

# --- CALLBACKS ---
@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    uid = call.message.chat.id
    if call.data == "gen":
        bot.answer_callback_query(call.id, "Generating...")
        try:
            dom = requests.get("https://api.mail.tm/domains").json()['hydra:member'][0]['domain']
            email = f"premium_{random.randint(100,999)}@{dom}"
            pwd = "password123"
            requests.post("https://api.mail.tm/accounts", json={"address": email, "password": pwd})
            token = requests.post("https://api.mail.tm/token", json={"address": email, "password": pwd}).json().get('token')
            if token:
                users_col.update_one({"uid": uid}, {"$set": {"email": email, "token": token, "last_id": "0"}}, upsert=True)
                history_col.insert_one({"uid": uid, "email": email, "id_code": str(random.randint(1000, 9999))})
                bot.send_message(uid, f"✅ <b>Generated:</b>\n<code>{email}</code>")
        except: bot.send_message(uid, "❌ Server Busy")
    
    elif call.data == "his":
        mails = list(history_col.find({"uid": uid}).limit(10))
        res = "📊 <b>Secure History:</b>\n\n"
        for d in mails: res += f"📧 <code>{d['email']}</code> | /del_{d.get('id_code', '0')}\n"
        bot.send_message(uid, res if mails else "No history found.")

# --- BROADCAST (PHOTO + TEXT) ---
@bot.message_handler(commands=['broadcast'])
def broadcast_command(m):
    if m.chat.id == ADMIN_ID:
        msg = bot.send_message(m.chat.id, "📢 Send me the message (Text or Photo with Caption)")
        bot.register_next_step_handler(msg, do_broadcast)

def do_broadcast(m):
    users = users_col.find({})
    for u in users:
        try:
            if m.content_type == 'photo': bot.send_photo(u['uid'], m.photo[-1].file_id, caption=m.caption)
            else: bot.send_message(u['uid'], m.text)
        except: pass
    bot.send_message(ADMIN_ID, "✅ Broadcast Completed!")

# --- DELETE SYSTEM ---
@bot.message_handler(regexp=r'/del_(\d+)')
def delete_item(m):
    code = m.text.split('_')[1]
    history_col.delete_one({"uid": m.chat.id, "id_code": code})
    bot.send_message(m.chat.id, "🗑️ Deleted from History.")

if __name__ == "__main__":
    threading.Thread(target=otp_checker, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
