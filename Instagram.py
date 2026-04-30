import telebot
import requests
import time
import threading
import random
import re
import dns.resolver
from pymongo import MongoClient
from telebot import types
from concurrent.futures import ThreadPoolExecutor

# --- DNS BYPASS ---
try:
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8', '1.1.1.1']
except: pass

# --- CONFIG ---
API_TOKEN = '8300468544:AAF9Q6eC3jBgMzCkJXPebKW-R6d-74BWZO0'
MONGO_URI = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

# --- MONGODB ---
users_col = None
history_col = None
try:
    client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True, serverSelectionTimeoutMS=5000)
    db = client['KushalPremiumStore']
    users_col = db['users']
    history_col = db['history']
    client.admin.command('ping')
except: pass

# --- SPEED HELPERS ---
def get_clean_otp(text):
    matches = re.findall(r'\b\d{4,8}\b', text)
    return matches[0] if matches else "NOT FOUND"

def detect_platform(text):
    text = text.lower()
    if "instagram" in text: return "Instagram", "https://instagram.com"
    if "facebook" in text: return "Facebook", "https://facebook.com"
    return "Web Service", "https://google.com"

# --- ⚡ SUPER FAST ENGINE (0.5s Check) ---
def check_inbox(uid, email, token, last_id):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        # Timeout kam kiya taaki jaldi check ho
        r = requests.get("https://api.mail.tm/messages", headers=headers, timeout=3).json()
        msgs = r.get('hydra:member', [])
        
        if msgs:
            m = msgs[0]
            m_id = str(m['id'])
            if m_id != str(last_id):
                detail = requests.get(f"https://api.mail.tm/messages/{m_id}", headers=headers).json()
                body = detail.get('intro', '')
                subj = detail.get('subject', '')
                otp = get_clean_otp(body + subj)
                plat_name, plat_url = detect_platform(body + subj)

                # --- EXACT SCREENSHOT DESIGN (NO PHOTO PREVIEW) ---
                ui = (
                    f"📧 <b>Account:</b> <code>{email}</code>\n"
                    f"📝 <b>Subject:</b> <i>{subj}</i>\n"
                    f"🔗 <b>Platform:</b> <a href='{plat_url}'>{plat_name}</a>\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"📩 <b>Message Body:</b>\n"
                    f"<i>{body[:120]}...</i>\n\n"
                    f"⚡ <b>OTP CODE:</b> <code>{otp}</code>\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"🔹 <i>Tap code to copy instantly</i>"
                )
                
                # disable_web_page_preview=True se Instagram photo nahi aayegi
                bot.send_message(uid, ui, disable_web_page_preview=True)
                if users_col is not None:
                    users_col.update_one({"uid": uid}, {"$set": {"last_id": m_id}})
    except: pass

def background_loop():
    while True:
        try:
            if users_col is not None:
                all_users = list(users_col.find({"token": {"$exists": True}}))
                # Threading workers badha diye taaki delay na ho
                with ThreadPoolExecutor(max_workers=50) as exe:
                    for user in all_users:
                        exe.submit(check_inbox, user['uid'], user['email'], user['token'], user.get('last_id', '0'))
        except: pass
        time.sleep(1) # Speed fast kar di

# --- SIDE MENU CONFIG ---
def set_menu():
    bot.delete_my_commands(scope=None, language_code=None)
    bot.set_my_commands([
        types.BotCommand("start", "🏠 Home / Refresh"),
        types.BotCommand("generate", "📧 Generate New Mail"),
        types.BotCommand("id", "📊 My History / Delete"),
        types.BotCommand("reset", "🗑️ Clear All Data")
    ])

# --- COMMANDS ---

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.chat.id
    name = m.from_user.first_name
    set_menu()

    photo_id = ""
    try:
        p = bot.get_user_profile_photos(uid)
        if p.total_count > 0: photo_id = p.photos[0][-1].file_id
    except: pass

    mention = f'<b><a href="tg://user?id={uid}">{name}</a></b>'
    welcome_ui = (
        f"👋 <b>Welcome, {mention}!</b>\n\n"
        f"🚀 <b>KUSHAL PREMIUM STORE</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🆔 <b>User ID:</b> <code>{uid}</code>\n"
        f"📊 <b>Status:</b> <code>Cloud Active</code>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📩 <i>Click /generate for instant mail.</i>"
    )
    if photo_id: bot.send_photo(uid, photo_id, caption=welcome_ui)
    else: bot.send_message(uid, welcome_ui)

@bot.message_handler(commands=['generate'])
def generate(m):
    uid = m.chat.id
    # Fast animation
    status = bot.send_message(uid, "⚡ <b>Generating Instant Mail...</b>")
    
    try:
        # Optimized Domain Fetch
        doms = requests.get("https://api.mail.tm/domains").json()['hydra:member']
        target = doms[0]['domain'] # Pehla domain uthaya speed ke liye
        
        email = f"pro{random.randint(10,99)}x{random.randint(100,999)}@{target}"
        pwd = f"kushal{random.randint(10,99)}"
        
        # Async-like requests
        requests.post("https://api.mail.tm/accounts", json={"address": email, "password": pwd}, timeout=5)
        tk = requests.post("https://api.mail.tm/token", json={"address": email, "password": pwd}, timeout=5).json()
        token = tk.get('token')

        if token:
            if users_col is not None:
                users_col.update_one({"uid": uid}, {"$set": {"email": email, "token": token, "last_id": "0"}}, upsert=True)
                history_col.insert_one({"uid": uid, "email": email, "id_code": str(random.randint(100000, 999999))})
            
            bot.edit_message_text(f"✅ <b>Generated Successfully!</b>\n\n📧 <code>{email}</code>", uid, status.message_id)
        else: bot.edit_message_text("❌ Error. Try again.", uid, status.message_id)
    except: bot.edit_message_text("❌ Server Busy.", uid, status.message_id)

@bot.message_handler(commands=['id'])
def show_id(m):
    uid = m.chat.id
    if history_col is None: return
    mails = list(history_col.find({"uid": uid}).limit(20))
    
    if not mails:
        bot.send_message(uid, "📊 <b>History Khali Hai!</b>")
        return

    res = "📊 <b>Your History:</b>\n━━━━━━━━━━━━━━━━━━\n"
    for i, d in enumerate(mails, 1):
        code = d.get('id_code', '000')
        res += f"{i}. <code>{d['email']}</code> | /delete_{code}\n"
    
    res += "━━━━━━━━━━━━━━━━━━"
    bot.send_message(uid, res)

@bot.message_handler(regexp=r'/delete_(\d+)')
def delete_mail(m):
    code = m.text.split('_')[1]
    if history_col is not None:
        history_col.delete_one({"uid": m.chat.id, "id_code": code})
        bot.send_message(m.chat.id, "🗑️ <b>Deleted.</b>")

if __name__ == "__main__":
    set_menu()
    threading.Thread(target=background_loop, daemon=True).start()
    print(">>> Fast System Online")
    bot.polling(none_stop=True)