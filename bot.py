import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# --- [ LOGGING & CONFIG ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AHMED_X_PRO")

# CONFIGURATION
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "IDHAR_NAYA_TOKEN_DALO" # <--- APNA TOKEN DALO
OWNER_ID = 6632236983 

# DATABASE (In-Memory for Render Stability)
AUTH_USERS = {OWNER_ID}
DATABASE = {"users": set(), "banned": set()}

# --- [ RENDER ALIVE ENGINE ] ---
web = Flask('')
@web.route('/')
def home(): return "AHMED X PRO ENGINE IS RUNNING 🚀"

def run_web():
    web.run(host='0.0.0.0', port=8080)

# --- [ UI TEXTURE ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

app = Client("AhmedX_Full", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ DECORATORS / MIDDLEWARE ] ---
def is_owner(func):
    async def wrapper(client, message):
        if message.from_user.id != OWNER_ID:
            return await message.reply("⚠️ **ACCESS DENIED: OWNER ONLY COMMAND.**")
        return await func(client, message)
    return wrapper

# --- [ COMMANDS ] ---

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    uid = message.from_user.id
    DATABASE["users"].add(uid)
    
    if uid in DATABASE["banned"]:
        return await message.reply("🚫 **YOU ARE BANNED FROM THIS STORE.**")

    welcome_text = (
        f"{BR}\n"
        f"🔥 **WELCOME TO AHMED X STOREZ**\n"
        f"{BR}\n"
        f"👤 **USER:** {message.from_user.first_name.upper()}\n"
        f"🆔 **ID:** `{uid}`\n"
        f"🛡 **STATUS:** {'PREMIUM' if uid in AUTH_USERS else 'MEMBER'}\n"
        f"🌐 **VER:** 2026.X-PRO\n"
        f"{BR}\n"
        f"USE THE BUTTONS BELOW TO NAVIGATE:\n"
        f"{BR}"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 PRODUCTS", callback_data="prod"), 
         InlineKeyboardButton("🛡 SUPPORT", callback_data="supp")],
        [InlineKeyboardButton("📊 SYSTEM STATS", callback_data="stats")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=buttons)

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_handler(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 **REPLY TO A MESSAGE TO BROADCAST.**")
    
    sts = await message.reply("🚀 **BROADCASTING IN PROGRESS...**")
    done, fail = 0, 0
    
    for user in list(DATABASE["users"]):
        try:
            await message.reply_to_message.copy(user)
            done += 1
            await asyncio.sleep(0.1)
        except:
            fail += 1
            
    await sts.edit(f"✅ **BROADCAST COMPLETED**\n{BR}\n⚡ **SENT:** {done}\n❌ **FAILED:** {fail}")

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_user(client, message):
    try:
        target = int(message.command[1])
        AUTH_USERS.add(target)
        await message.reply(f"✅ **USER `{target}` HAS BEEN ADDED TO PREMIUM.**")
    except:
        await message.reply("❌ **ERROR: PROVIDE VALID USER ID.**")

@app.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_user(client, message):
    try:
        target = int(message.command[1])
        DATABASE["banned"].add(target)
        await message.reply(f"🚫 **USER `{target}` HAS BEEN BANNED.**")
    except:
        await message.reply("❌ **ERROR: PROVIDE VALID USER ID.**")

@app.on_message(filters.command("stats"))
async def stats_handler(client, message):
    text = (
        f"{BR}\n"
        f"📊 **AHMED X STOREZ STATS**\n"
        f"{BR}\n"
        f"👥 **TOTAL USERS:** {len(DATABASE['users'])}\n"
        f"🛡 **AUTH USERS:** {len(AUTH_USERS)}\n"
        f"🚫 **BANNED:** {len(DATABASE['banned'])}\n"
        f"🛰 **SERVER:** RENDER-ASIA-1\n"
        f"{BR}"
    )
    await message.reply_text(text)

# --- [ CALLBACK QUERY HANDLER ] ---
@app.on_callback_query()
async def cb_handler(client, query):
    if query.data == "prod":
        await query.message.edit(f"{BR}\n📦 **AVAILABLE PRODUCTS**\n{BR}\n1. FB ID CLONE - ₹499\n2. TELEGRAM BOT CLONE - ₹999\n3. PREMIUM SESSIONS - ₹299\n{BR}\n**CONTACT @OWNER TO BUY**")
    elif query.data == "supp":
        await query.message.edit(f"{BR}\n🛡 **SUPPORT CENTER**\n{BR}\nOWNER: @AHMED_X\nTIMING: 24/7\n{BR}")
    elif query.data == "stats":
        await query.answer("FETCHING LIVE DATA...", show_alert=True)

# --- [ BOOT ENGINE ] ---
async def main():
    Thread(target=run_web, daemon=True).start()
    await app.start()
    # Set Commands for Bot
    await app.set_bot_commands([
        BotCommand("start", "RESET THE ENGINE"),
        BotCommand("buy", "VIEW STORE"),
        BotCommand("stats", "CHECK LOAD"),
        BotCommand("broadcast", "OWNER ONLY")
    ])
    logger.info("🔥 AHMED X PRO IS LIVE!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
