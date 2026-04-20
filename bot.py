import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# --- [ PRO LOGGING ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AHMED_X_ULTRA")

# --- [ CONFIGURATION ] ---
API_ID = int(os.environ.get("API_ID", "21552435"))
API_HASH = os.environ.get("API_HASH", "5b108bd2fdd31c0c34bc65f24a5216a0")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8635335052:AAHNPs7bSlwc3a_dGkPGuMhneWj40rD3gmw")
OWNER_ID = int(os.environ.get("OWNER_ID", "6632236983"))

# --- [ RENDER WEB SERVER (BYPASS STATUS 1) ] ---
web = Flask('')

@web.route('/')
def home():
    return "Ahmed X Engine: Running ✅"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    web.run(host='0.0.0.0', port=port)

# --- [ STORAGE ] ---
TOTAL_USERS = set()
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

app = Client("AhmedX_PRO", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ COMMANDS ] ---

@app.on_message(filters.command("start"))
async def start(client, message):
    uid = message.from_user.id
    TOTAL_USERS.add(uid)
    
    welcome_text = (
        f"{BR}\n"
        f"🔥 **WELCOME TO AHMED X STOREZ**\n"
        f"{BR}\n"
        f"👤 **USER:** {message.from_user.first_name.upper()}\n"
        f"🛡 **STATUS:** {'OWNER' if uid == OWNER_ID else 'MEMBER'}\n"
        f"{BR}\n"
        f"SELECT AN OPTION:\n"
        f"{BR}"
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📦 PRODUCTS", callback_data="prod"), 
         InlineKeyboardButton("📊 STATS", callback_data="stats")]
    ])
    
    await message.reply_text(welcome_text, reply_markup=buttons)

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 Reply to a message.")
    
    sts = await message.reply("🚀 Sending...")
    done = 0
    for user in list(TOTAL_USERS):
        try:
            await message.reply_to_message.copy(user)
            done += 1
            await asyncio.sleep(0.1)
        except: pass
    await sts.edit(f"✅ Sent to {done} users.")

# --- [ CALLBACKS ] ---
@app.on_callback_query()
async def cb(client, query):
    if query.data == "prod":
        await query.message.edit(f"{BR}\n📦 **STOCK**\n{BR}\n1. FB ID FIX\n2. BOT CLONE\n{BR}\n**DM @OWNER**")
    elif query.data == "stats":
        await query.answer(f"Users: {len(TOTAL_USERS)}", show_alert=True)

# --- [ THE ULTIMATE RUNNER ] ---

async def start_services():
    # 1. Start Web Server
    Thread(target=run_web, daemon=True).start()
    
    # 2. Start Bot
    logger.info("🚀 Starting Ahmed X...")
    await app.start()
    
    # 3. Set Menu
    await app.set_bot_commands([
        BotCommand("start", "Restart Bot"),
        BotCommand("broadcast", "Send Broadcast")
    ])
    
    logger.info("✅ Bot is Live!")
    await idle()
    await app.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(start_services())
    except (KeyboardInterrupt, SystemExit):
        pass
    except Exception as e:
        logger.error(f"❌ CRITICAL ERROR: {e}")
