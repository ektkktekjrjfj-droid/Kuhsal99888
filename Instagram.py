import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, idle
from pyrogram.handlers import MessageHandler

# --- [ LOGGING ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AHMED_X_ULTRA")

# --- [ CONFIG ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8464390807:AAGVxObZ60Se34Kjo3nX34I0iDa8VBAcsRY"
OWNER_ID = 6632236983

# --- [ WEB SERVER ] ---
web = Flask('')
@web.route('/')
def home(): return "<h1>AHMED X IS LIVE ✅</h1>"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web.run(host='0.0.0.0', port=port)

# --- [ BOT ENGINE ] ---
app = Client("AhmedX_NoSetting", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

# --- [ RAW MESSAGE HANDLER ] ---
# Ye function har message ko pakdega, chahe wo command ho ya simple text
async def handle_everything(client, message):
    if not message.text:
        return

    text = message.text.lower()
    uid = message.from_user.id
    logger.info(f"📩 Input Received: {text}")

    # Start Response
    if text.startswith("/start"):
        resp = (
            f"{BR}\n"
            f"🔥 **AHMED X STOREZ - LIVE**\n"
            f"{BR}\n"
            f"👤 USER: {message.from_user.first_name.upper()}\n"
            f"✅ STATUS: ONLINE\n"
            f"{BR}"
        )
        await message.reply_text(resp)

    # IndoFix Response
    elif text.startswith("/indofix"):
        data = text.replace("/indofix", "").strip()
        if not data:
            return await message.reply("❌ Usage: `/indofix DATA`")
        
        await message.reply(
            f"{BR}\n"
            f"🛠 **INDO-FIX DONE**\n"
            f"{BR}\n"
            f"📥 DATA: `{data}`\n"
            f"✅ SYSTEM: STABLE\n"
            f"{BR}"
        )

# --- [ BOOT SYSTEM ] ---

async def main():
    # Start Web Server
    Thread(target=run_web, daemon=True).start()
    
    # Register the handler manually (Sabse safe tarika)
    app.add_handler(MessageHandler(handle_everything))
    
    try:
        logger.info("🚀 Booting Ahmed X...")
        await app.start()
        logger.info("✅ SUCCESS: Ahmed X is Online!")
        await idle()
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        pass