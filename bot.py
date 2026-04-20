import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# --- [ ADVANCED LOGGING ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AHMED_X_ULTRA")

# --- [ CONFIGURATION & TAGS ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8635335052:AAHNPs7bSlwc3a_dGkPGuMhneWj40rD3gmw")
OWNER_ID = 6632236983

# --- [ INTERNAL DATABASE ] ---
USERS = set()
PREMIUM_USERS = {OWNER_ID}
BANNED_USERS = set()

# --- [ RENDER KEEP-ALIVE SYSTEM ] ---
web = Flask('')
@web.route('/')
def home(): return "<h1>AHMED X STOREZ: ENGINE STABLE 🚀</h1>"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web.run(host='0.0.0.0', port=port)

# --- [ UI DESIGN ELEMENTS ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"
LOGO = "🔥 **AHMED X STOREZ V10** 🔥"

app = Client("AhmedX_PRO", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ MIDDLEWARE / FILTERS ] ---
def is_admin(_, __, message):
    return message.from_user.id == OWNER_ID

# --- [ MAIN COMMANDS ] ---

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    uid = message.from_user.id
    USERS.add(uid)
    
    if uid in BANNED_USERS:
        return await message.reply("🚫 **BANNED:** Aapko is store se block kiya gaya hai.")

    status = "👑 OWNER" if uid == OWNER_ID else ("⚡ PREMIUM" if uid in PREMIUM_USERS else "👤 MEMBER")
    
    CAPTION = (
        f"{BR}\n"
        f"{LOGO}\n"
        f"{BR}\n"
        f"👋 **WELCOME:** {message.from_user.first_name.upper()}\n"
        f"🆔 **YOUR ID:** `{uid}`\n"
        f"🛡 **RANK:** {status}\n"
        f"🛰 **SERVER:** RENDER-ASIA-1\n"
        f"{BR}\n"
        f"Niche diye gaye buttons se navigate karein:\n"
        f"{BR}"
    )
    
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 VIEW PRODUCTS", callback_data="products")],
        [InlineKeyboardButton("👤 MY ACCOUNT", callback_data="acc"), InlineKeyboardButton("📊 LIVE STATS", callback_data="stats")],
        [InlineKeyboardButton("🛡 CONTACT OWNER", url="t.me/Kushal_X")]
    ])
    
    await message.reply_text(CAPTION, reply_markup=kb)

# --- [ STORE LOGIC ] ---

@app.on_callback_query()
async def cb_handler(client, query):
    uid = query.from_user.id
    
    if query.data == "products":
        text = (
            f"{BR}\n"
            f"🛒 **AHMED X AVAILABLE STOCK**\n"
            f"{BR}\n"
            f"1️⃣ **FB INDO CLONE** - ₹499\n"
            f"2️⃣ **TELEGRAM BOT SETUP** - ₹999\n"
            f"3️⃣ **PREMIUM SESSIONS** - ₹249\n"
            f"4️⃣ **AUTO-REACTION BOT** - ₹599\n"
            f"{BR}\n"
            f"💰 **PAYMENT:** DM @Kushal_X\n"
            f"{BR}"
        )
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="home")]]))

    elif query.data == "acc":
        text = (
            f"{BR}\n"
            f"👤 **USER ACCOUNT DETAILS**\n"
            f"{BR}\n"
            f"• **NAME:** {query.from_user.first_name}\n"
            f"• **ID:** `{uid}`\n"
            f"• **PLAN:** {'LIFETIME' if uid in PREMIUM_USERS else 'FREE'}\n"
            f"• **JOINED:** APRIL 2026\n"
            f"{BR}"
        )
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 BACK", callback_data="home")]]))

    elif query.data == "stats":
        await query.answer(f"System Load: 0.1% | Live Users: {len(USERS)}", show_alert=True)
        
    elif query.data == "home":
        # Restart logic to main menu
        await query.message.edit("🔄 Loading Menu...", reply_markup=None)
        await start_handler(client, query.message)

# --- [ ADMIN PANEL COMMANDS ] ---

@app.on_message(filters.command("broadcast") & filters.create(is_admin))
async def bcast(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 **USAGE:** Reply to a message with `/broadcast`")
    
    msg = await message.reply("🚀 **SENDING BROADCAST...**")
    done = 0
    for user in list(USERS):
        try:
            await message.reply_to_message.copy(user)
            done += 1
            await asyncio.sleep(0.1)
        except: pass
    await msg.edit(f"✅ **BROADCAST DONE:** Sent to {done} users.")

@app.on_message(filters.command("add") & filters.create(is_admin))
async def add_prem(client, message):
    try:
        target = int(message.command[1])
        PREMIUM_USERS.add(target)
        await message.reply(f"⚡ **USER `{target}` ADDED TO PREMIUM!**")
    except:
        await message.reply("❌ **ERROR:** Use `/add USER_ID`")

@app.on_message(filters.command("ban") & filters.create(is_admin))
async def ban_user(client, message):
    try:
        target = int(message.command[1])
        BANNED_USERS.add(target)
        await message.reply(f"🚫 **USER `{target}` BANNED SUCCESSFULLY.**")
    except:
        await message.reply("❌ **ERROR:** Use `/ban USER_ID`")

# --- [ BOOT SYSTEM ] ---

async def main_engine():
    # 1. Start Keep-Alive Web Server
    Thread(target=run_web, daemon=True).start()
    
    try:
        logger.info("🚀 AHMED X ENGINE STARTING...")
        await app.start()
        
        # Set Bot Commands for Telegram Menu
        await app.set_bot_commands([
            BotCommand("start", "Open Main Menu"),
            BotCommand("broadcast", "Admin Only: Send News"),
            BotCommand("stats", "Check System Status"),
            BotCommand("add", "Admin Only: Add Premium")
        ])
        
        logger.info("✅ AHMED X IS LIVE ON RENDER!")
        await idle()
    except Exception as e:
        logger.error(f"❌ ENGINE CRASH: {e}")
    finally:
        if app.is_connected:
            await app.stop()

if __name__ == "__main__":
    asyncio.run(main_engine())
