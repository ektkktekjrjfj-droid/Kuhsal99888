import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# --- [ LOGGING ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AHMED_X_ULTRA")

# --- [ CONFIGURATION ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
# Naya token yahan fix kar diya hai
BOT_TOKEN = "8410119226:AAEDaMjNEmPINLbJc26RsPVNKgGjVNH_fSk"
OWNER_ID = 6632236983

# --- [ RENDER WEB SERVER (KEEP-ALIVE) ] ---
web = Flask('')
@web.route('/')
def home(): return "<h1>AHMED X ENGINE IS ONLINE 🚀</h1>"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web.run(host='0.0.0.0', port=port)

# --- [ STORAGE & UI ] ---
USERS = set()
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

app = Client("AhmedX_PRO", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ MAIN COMMANDS ] ---

@app.on_message(filters.command("start"))
async def start(client, message):
    uid = message.from_user.id
    USERS.add(uid)
    
    text = (
        f"{BR}\n"
        f"🔥 **WELCOME TO AHMED X STOREZ**\n"
        f"{BR}\n"
        f"👤 **USER:** {message.from_user.first_name.upper()}\n"
        f"🆔 **ID:** `{uid}`\n"
        f"🛡 **RANK:** {'OWNER' if uid == OWNER_ID else 'VERIFIED MEMBER'}\n"
        f"🌐 **SYSTEM:** V10-HYBRID-ASYNC\n"
        f"{BR}\n"
        f"Niche diye gaye buttons se navigate karein:\n"
        f"{BR}"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 VIEW PRODUCTS", callback_data="prod")],
        [InlineKeyboardButton("📊 LIVE STATS", callback_data="stats"), InlineKeyboardButton("🛡 SUPPORT", url="t.me/Kushal_X")],
        [InlineKeyboardButton("👤 MY ACCOUNT", callback_data="acc")]
    ])
    
    await message.reply_text(text, reply_markup=buttons)

# --- [ BROADCAST SYSTEM (ADMIN ONLY) ] ---

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def bcast(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 **USAGE:** Reply to a message with `/broadcast` to send it to all users.")
    
    sts = await message.reply("🚀 **INITIATING BROADCAST...**")
    done = 0
    for user in list(USERS):
        try:
            await message.reply_to_message.copy(user)
            done += 1
            await asyncio.sleep(0.1)
        except: pass
    await sts.edit(f"✅ **BROADCAST DONE:** Sent to {done} users.")

# --- [ CALLBACK LOGIC ] ---

@app.on_callback_query()
async def cb_handler(client, query):
    if query.data == "prod":
        text = (
            f"{BR}\n"
            f"🛒 **AHMED X CURRENT STOCK**\n"
            f"{BR}\n"
            f"1️⃣ FB ID CLONE - ₹499\n"
            f"2️⃣ TELEGRAM BOT CLONE - ₹999\n"
            f"3️⃣ PREMIUM SESSIONS - ₹249\n"
            f"{BR}\n"
            f"💰 **PAYMENT:** DM @Kushal_X\n"
            f"{BR}"
        )
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="home")]]))

    elif query.data == "acc":
        text = (
            f"{BR}\n"
            f"👤 **ACCOUNT DETAILS**\n"
            f"{BR}\n"
            f"• NAME: {query.from_user.first_name}\n"
            f"• ID: `{query.from_user.id}`\n"
            f"• STATUS: {'PREMIUM' if query.from_user.id == OWNER_ID else 'MEMBER'}\n"
            f"{BR}"
        )
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="home")]]))

    elif query.data == "stats":
        await query.answer(f"System Load: 0.05% | Users: {len(USERS)}", show_alert=True)

    elif query.data == "home":
        await query.message.edit("🔄 Loading Dashboard...")
        await start(client, query.message)

# --- [ ENGINE STARTUP ] ---

async def start_services():
    # 1. Start Web Server in background thread
    Thread(target=run_web, daemon=True).start()
    
    try:
        logger.info("🚀 Booting Ahmed X Engine...")
        await app.start()
        
        # 2. Set Bot Commands Menu
        await app.set_bot_commands([
            BotCommand("start", "Open Main Menu"),
            BotCommand("broadcast", "Admin Only Broadcast")
        ])
        
        logger.info("✅ SUCCESS: Ahmed X is Live!")
        await idle()
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR: {e}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    # Render loop handler
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except (KeyboardInterrupt, SystemExit):
        pass
