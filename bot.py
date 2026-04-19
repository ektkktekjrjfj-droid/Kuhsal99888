import os
import asyncio
import logging
from flask import Flask
from threading import Thread
from pyrogram import Client, filters

# --- [ RENDER WEB-SURVIVAL ENGINE ] ---
# Ye part Render ko "Status 1" dene se rokega
web = Flask('')

@web.route('/')
def home():
    return "AHMED X STOREZ IS ONLINE 🚀"

def run():
    # Render default port 10000 use karta hai
    port = int(os.environ.get("PORT", 8080))
    web.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- [ BOT CONFIGURATION ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AhmedX")

API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "IDHAR_NAYA_TOKEN_DALO" # <--- APNA NAYA TOKEN YAHA PASTE KARO
OWNER_ID = 6632236983 

# IN-MEMORY DATABASE
AUTHORIZED_USERS = {OWNER_ID}
TOTAL_USERS = set()

app = Client("AhmedX_Boss", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ UI TEXTURE ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

# --- [ FUNCTIONS ] ---

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
        f"🌐 **ENGINE:** HYBRID WEB-BOT V5\n"
        f"{BR}\n"
        f"🛠 **PREMIUM FUNCTIONS:**\n"
        f"• `/buy` - STORE INVENTORY\n"
        f"• `/broadcast` - OWNER ONLY\n"
        f"• `/stats` - SYSTEM LOAD\n"
        f"{BR}"
    )
    try:
        await message.reply_photo("https://telegra.ph/file/2e8790380c5e732381284.jpg", caption=CAPTION)
    except:
        await message.reply_text(CAPTION)

@app.on_message(filters.command("buy"))
async def buy_menu(client, message):
    await message.reply(f"{BR}\n📦 **AHMED X STOREZ STOCK**\n{BR}\n1. **FB INDO FIX** - DM @OWNER\n2. **PREMIUM SESSION** - ₹499\n3. **CLONE BOT** - ₹999\n{BR}")

# --- [ OWNER TOOLS ] ---

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_tool(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 **REPLY TO A MESSAGE TO SEND BROADCAST.**")
    
    ex = await message.reply("🚀 **SENDING BROADCAST...**")
    done = 0
    for user in TOTAL_USERS:
        try:
            await message.reply_to_message.copy(user)
            done += 1
            await asyncio.sleep(0.1)
        except: pass
    await ex.edit(f"✅ **BROADCAST COMPLETED! SENT TO {done} USERS.**")

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_auth(client, message):
    try:
        uid = int(message.command[1])
        AUTHORIZED_USERS.add(uid)
        await message.reply(f"✅ **USER `{uid}` AUTHORIZED.**")
    except: await message.reply("❌ **USE: /add ID**")

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def show_stats(client, message):
    await message.reply(f"{BR}\n📊 **SYSTEM STATS**\n{BR}\n👥 **TOTAL USERS:** {len(TOTAL_USERS)}\n🛡 **AUTH USERS:** {len(AUTHORIZED_USERS)}\n{BR}")

# --- [ MAIN RUNNER ] ---
if __name__ == "__main__":
    logger.info("🚀 STARTING HYBRID ENGINE...")
    keep_alive() # Starts the Web Server
    app.run()    # Starts the Bot
