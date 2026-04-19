import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# --- [ ADVANCED LOGGING ] ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AHMED_X_ULTRA")

# --- [ ENVIRONMENT DATA FETCH ] ---
# Ye values Render Dashboard ke 'Environment' tab se aayengi
API_ID = int(os.environ.get("API_ID", "21552435"))
API_HASH = os.environ.get("API_HASH", "5b108bd2fdd31c0c34bc65f24a5216a0")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8635335052:AAHNPs7bSlwc3a_dGkPGuMhneWj40rD3gmw")
OWNER_ID = int(os.environ.get("OWNER_ID", "6632236983"))

# --- [ RENDER WEB SERVER (STATUS 1 BYPASS) ] ---
web = Flask('')

@web.route('/')
def home():
    return "<h1>AHMED X STOREZ ENGINE IS ONLINE 🚀</h1>"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web.run(host='0.0.0.0', port=port)

# --- [ INTERNAL DATA STORAGE ] ---
TOTAL_USERS = set()
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

app = Client(
    "AhmedX_Final",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- [ BOT COMMAND HANDLERS ] ---

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    uid = message.from_user.id
    TOTAL_USERS.add(uid)
    
    welcome_text = (
        f"{BR}\n"
        f"🔥 **WELCOME TO AHMED X STOREZ**\n"
        f"{BR}\n"
        f"👤 **USER:** {message.from_user.first_name.upper()}\n"
        f"🆔 **ID:** `{uid}`\n"
        f"🛡 **STATUS:** {'PREMIUM OWNER' if uid == OWNER_ID else 'VERIFIED MEMBER'}\n"
        f"🌐 **ENGINE:** STABLE V10 [NO-CHROME]\n"
        f"{BR}\n"
        f"SELECT AN OPTION BELOW:\n"
        f"{BR}"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 PRODUCTS", callback_data="prod"), 
         InlineKeyboardButton("🛡 SUPPORT", callback_data="supp")],
        [InlineKeyboardButton("📊 LIVE STATS", callback_data="stats")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=buttons)

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 **REPLY TO A MESSAGE TO BROADCAST.**")
    
    sts = await message.reply("🚀 **INITIATING BROADCAST...**")
    done, fail = 0, 0
    for user in list(TOTAL_USERS):
        try:
            await message.reply_to_message.copy(user)
            done += 1
            await asyncio.sleep(0.1)
        except: 
            fail += 1
            
    await sts.edit(f"✅ **BROADCAST COMPLETED**\n{BR}\n⚡ **SUCCESS:** {done}\n❌ **FAILED:** {fail}")

@app.on_message(filters.command("stats"))
async def show_stats(client, message):
    await message.reply_text(f"{BR}\n📊 **LIVE STATS**\n{BR}\n👥 **TOTAL USERS:** {len(TOTAL_USERS)}\n🛡 **AUTH USERS:** 1\n{BR}")

# --- [ BUTTON LOGIC ] ---
@app.on_callback_query()
async def cb_handler(client, query):
    if query.data == "prod":
        await query.message.edit(f"{BR}\n📦 **CURRENT STOCK LIST**\n{BR}\n1. FB ID CLONE - ₹499\n2. BOT CLONING - ₹999\n3. PREMIUM SESSIONS - ₹299\n{BR}\n**CONTACT @OWNER TO ORDER**")
    elif query.data == "supp":
        await query.message.edit(f"{BR}\n🛡 **SUPPORT & HELP**\n{BR}\nOWNER: @AHMED_X\nSTATUS: ONLINE\n{BR}")
    elif query.data == "stats":
        await query.answer(f"System Load: 0.05% | Users: {len(TOTAL_USERS)}", show_alert=True)

# --- [ MAIN ENGINE RUNNER ] ---

async def main():
    # 1. Start Web Server in Background
    Thread(target=run_web, daemon=True).start()
    
    # 2. Start Bot
    logger.info("🚀 STARTING AHMED X ENGINE...")
    await app.start()
    
    # 3. Set Bot Menu Commands
    await app.set_bot_commands([
        BotCommand("start", "Restart the bot"),
        BotCommand("stats", "Check user count"),
        BotCommand("broadcast", "Send message to all")
    ])
    
    logger.info("✅ BOT IS LIVE ON RENDER!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
