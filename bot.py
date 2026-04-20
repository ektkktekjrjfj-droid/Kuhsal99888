import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- [ LOGGING ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AHMED_X")

# --- [ DATA ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8410119226:AAEDaMjNEmPINLbJc26RsPVNKgGjVNH_fSk"
OWNER_ID = 6632236983

# --- [ WEB SERVER FOR RENDER ] ---
web = Flask('')
@web.route('/')
def home(): return "<h1>AHMED X ENGINE LIVE ✅</h1>"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web.run(host='0.0.0.0', port=port)

# --- [ BOT ENGINE ] ---
app = Client("AhmedX", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "━━━━━━━━━━━━━━━━━━━━\n🔥 **AHMED X STOREZ IS LIVE**\n━━━━━━━━━━━━━━━━━━━━",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📦 STOCK", callback_data="p")
        ]])
    )

@app.on_callback_query()
async def cb(client, query):
    if query.data == "p":
        await query.message.edit("🛒 **STOCK LIST:**\n1. FB ID - ₹499\n2. BOT CLONE - ₹999")

# --- [ THE FINAL FIX RUNNER ] ---
def main():
    # Keep-Alive thread start
    Thread(target=run_web, daemon=True).start()
    
    # Start the event loop
    loop = asyncio.get_event_loop()
    
    try:
        logger.info("🚀 Starting Bot...")
        loop.run_until_complete(app.start())
        logger.info("✅ Bot is Online!")
        idle()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        loop.run_until_complete(app.stop())

if __name__ == "__main__":
    main()
