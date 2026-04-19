import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# --- [ LOGGING ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AhmedX-AutoFix")

# --- [ INTERNAL PORT CONFIGURATION ] ---
# Yahan humne PORT ko direct 8080 par lock kar diya hai
PORT = 8080

web = Flask('')

@web.route('/')
def home():
    return "AHMED X STOREZ: SELF-HEALING SYSTEM ACTIVE 🚀"

def run():
    # Render ya local host, dono ke liye port fixed hai
    try:
        logger.info(f"📡 STARTING INTERNAL WEB SERVER ON PORT: {PORT}")
        web.run(host='0.0.0.0', port=PORT)
    except Exception as e:
        logger.error(f"❌ WEB SERVER ERROR: {e}")

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- [ BOT CONFIGURATION ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "IDHAR_NAYA_TOKEN_DALO" # <--- APNA NAYA TOKEN YAHA PASTE KARO
OWNER_ID = 6632236983 

# IN-MEMORY DATABASE
AUTHORIZED_USERS = {OWNER_ID}
TOTAL_USERS = set()

app = Client("AhmedX_SelfFix", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ UI TEXTURE ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

# --- [ COMMANDS ] ---

@app.on_message(filters.command("start"))
async def start(client, message):
    try:
        uid = message.from_user.id
        TOTAL_USERS.add(uid)
        is_auth = uid in AUTHORIZED_USERS
        STATUS = "✅ ⚡ AUTHORIZED ⚡" if is_auth else "❌ ⚡ ACCESS DENIED ⚡"
        
        CAPTION = (
            f"{BR}\n"
            f"🔥 **WELCOME TO AHMED X STOREZ**\n"
            f"{BR}\n"
            f"👤 **USER:** {message.from_user.first_name.upper()}\n"
            f"🆔 **ID:** `{uid}`\n"
            f"🛡 **STATUS:** {STATUS}\n"
            f"🌐 **ENGINE:** INTERNAL PORT FIX V8\n"
            f"{BR}\n"
            f"🛠 **COMMANDS:** /buy, /stats, /help\n"
            f"✨ **AUTO-RESTART: ACTIVE**\n"
            f"{BR}"
        )
        await message.reply_text(CAPTION)
    except Exception as e:
        logger.error(f"Error in start: {e}")

@app.on_message(filters.command("buy"))
async def buy(client, message):
    await message.reply(f"{BR}\n📦 **STORE STOCK**\n{BR}\n1. **FB INDO FIX**\n2. **PREMIUM SESSION**\n3. **CLONE BOT**\n{BR}")

# --- [ ADMIN TOOLS ] ---

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 **REPLY TO A MESSAGE.**")
    for user in TOTAL_USERS:
        try:
            await message.reply_to_message.copy(user)
            await asyncio.sleep(0.1)
        except: pass
    await message.reply("✅ **BROADCAST DONE.**")

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    await message.reply(f"{BR}\n📊 **STATS**\n{BR}\n👥 **USERS:** {len(TOTAL_USERS)}\n🛡 **AUTH:** {len(AUTHORIZED_USERS)}\n{BR}")

# --- [ THE UNSTOPPABLE RUNNER ] ---
async def start_bot():
    while True:
        try:
            logger.info("🚀 STARTING AHMED X ENGINE...")
            await app.start()
            logger.info("✅ BOT IS LIVE!")
            while True:
                await asyncio.sleep(1000)
        except Exception as e:
            logger.error(f"⚠️ CRASH DETECTED: {e}. AUTO-RESTARTING...")
            try: await app.stop()
            except: pass
            await asyncio.sleep(5)
            continue

if __name__ == "__main__":
    keep_alive() # Internal Port 8080 Fix
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())
