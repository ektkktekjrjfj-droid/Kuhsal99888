import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# --- [ PRO LOGGING ] ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AHMED_X_ULTRA")

# --- [ CONFIGURATION ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "IDHAR_NAYA_TOKEN_DALO" # <--- APNA TOKEN DALO
OWNER_ID = 6632236983 

# INTERNAL DATABASE
AUTH_USERS = {OWNER_ID}
TOTAL_USERS = set()
BANNED_USERS = set()

# --- [ RENDER WEB SERVER ] ---
web = Flask('')
@web.route('/')
def home(): return "AHMED X PRO ENGINE IS LIVE 🚀"

def run_web():
    web.run(host='0.0.0.0', port=8080)

# --- [ UI DESIGN ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

app = Client("AhmedX_Ultra", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ COMMAND HANDLERS ] ---

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    uid = message.from_user.id
    TOTAL_USERS.add(uid)
    
    if uid in BANNED_USERS:
        return await message.reply("🚫 **ACCESS DENIED: YOU ARE BANNED.**")

    welcome_text = (
        f"{BR}\n"
        f"🔥 **WELCOME TO AHMED X STOREZ**\n"
        f"{BR}\n"
        f"👤 **USER:** {message.from_user.first_name.upper()}\n"
        f"🆔 **ID:** `{uid}`\n"
        f"🛡 **STATUS:** {'PREMIUM OWNER' if uid == OWNER_ID else 'VERIFIED MEMBER'}\n"
        f"🛰 **SERVER:** ASIA-RENDER-V10\n"
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
        except: fail += 1
    await sts.edit(f"✅ **BROADCAST COMPLETED**\n{BR}\n⚡ **SUCCESS:** {done}\n❌ **FAILED:** {fail}")

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_user(client, message):
    try:
        target = int(message.command[1])
        AUTH_USERS.add(target)
        await message.reply(f"✅ **USER `{target}` ADDED TO AUTH LIST.**")
    except: await message.reply("❌ **USE: /add USER_ID**")

@app.on_message(filters.command("stats"))
async def stats_handler(client, message):
    text = (
        f"{BR}\n"
        f"📊 **LIVE SYSTEM STATISTICS**\n"
        f"{BR}\n"
        f"👥 **TOTAL USERS:** {len(TOTAL_USERS)}\n"
        f"🛡 **AUTH USERS:** {len(AUTH_USERS)}\n"
        f"🚫 **BANNED:** {len(BANNED_USERS)}\n"
        f"⏳ **UPTIME:** STABLE\n"
        f"{BR}"
    )
    await message.reply_text(text)

# --- [ BUTTON LOGIC ] ---
@app.on_callback_query()
async def cb_handler(client, query):
    if query.data == "prod":
        await query.message.edit(f"{BR}\n📦 **CURRENT STOCK LIST**\n{BR}\n1. FB ID FIX - ₹499\n2. BOT CLONE - ₹999\n3. PREMIUM SESSIONS - ₹299\n{BR}\n**CONTACT @OWNER TO ORDER**")
    elif query.data == "supp":
        await query.message.edit(f"{BR}\n🛡 **SUPPORT & HELP**\n{BR}\nOWNER: @AHMED_X\nSTATUS: ONLINE\n{BR}")
    elif query.data == "stats":
        await query.answer(f"System Load: 0.05% | Users: {len(TOTAL_USERS)}", show_alert=True)

# --- [ BOOT ENGINE ] ---
async def main():
    Thread(target=run_web, daemon=True).start()
    await app.start()
    await app.set_bot_commands([
        BotCommand("start", "Restart Bot"),
        BotCommand("stats", "Check Status"),
        BotCommand("broadcast", "Send News")
    ])
    logger.info("🔥 AHMED X ULTRA ENGINE IS LIVE!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
