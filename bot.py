import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle

# --- [ LOGGING ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AhmedX-Final")

# --- [ WEB SERVER FOR RENDER ] ---
# Ye Render ko Status 1 dene se rokta hai
web = Flask('')

@web.route('/')
def home():
    return "AHMED X STOREZ: SYSTEM ONLINE 🚀"

def run_web():
    # Port 8080 internal fix
    try:
        web.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error(f"Web Server Error: {e}")

# --- [ CONFIGURATION ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "IDHAR_NAYA_TOKEN_DALO" # <--- APNA NAYA TOKEN PASTE KARO
OWNER_ID = 6632236983 

# In-Memory DB
AUTHORIZED_USERS = {OWNER_ID}
TOTAL_USERS = set()

app = Client("AhmedX_Final", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ UI TEXTURE ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

# --- [ COMMANDS ] ---

@app.on_message(filters.command("start"))
async def start(client, message):
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
        f"🌐 **ENGINE:** STABLE IDLE V9\n"
        f"{BR}\n"
        f"🛠 **COMMANDS:** /buy, /stats, /help\n"
        f"{BR}"
    )
    await message.reply_text(CAPTION)

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    await message.reply(f"👥 TOTAL USERS: {len(TOTAL_USERS)}")

# --- [ MAIN RUNNER ] ---

async def main():
    # 1. Start Web Server in background
    Thread(target=run_web, daemon=True).start()
    
    # 2. Start Bot
    logger.info("🚀 STARTING AHMED X ENGINE...")
    await app.start()
    logger.info("✅ BOT IS LIVE ON RENDER!")
    
    # 3. Keep bot running (IDLE)
    await idle()
    
    # 4. Stop if idle breaks
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
