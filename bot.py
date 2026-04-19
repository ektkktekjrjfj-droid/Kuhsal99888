import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import BotCommand

# --- [ LOGGING SETUP ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- [ CONFIGURATION ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "NAYA_TOKEN_YAHA_DALO" # <--- Apna Naya Token Paste Karo
OWNER_ID = 6632236983 

# In-Memory Database (Bot restart hone par reset hoga, MongoDB ke bina yahi option hai)
AUTH_USERS = [OWNER_ID]
BANNED_USERS = []
TOTAL_USERS = set()

app = Client("AHMEDX_PRO", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ UI TEXTURE ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

# --- [ HELPER FUNCTIONS ] ---
async def is_auth(uid):
    return uid in AUTH_USERS

# --- [ COMMANDS & FUNCTIONS ] ---

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    uid = message.from_user.id
    TOTAL_USERS.add(uid)
    
    if uid in BANNED_USERS:
        return await message.reply("❌ **YOUR ACCESS IS RESTRICTED BY OWNER.**")
    
    status = "✅ ⚡ AUTHORIZED ⚡" if await is_auth(uid) else "❌ ⚡ ACCESS DENIED ⚡"
    
    CAPTION = (
        f"{BR}\n"
        f"🔥 **WELCOME TO AHMED X STOREZ**\n"
        f"{BR}\n"
        f"👤 **USER:** {message.from_user.first_name.upper()}\n"
        f"🆔 **ID:** `{uid}`\n"
        f"🛡 **STATUS:** {status}\n"
        f"🌐 **SERVER:** RENDER CLOUD 2026\n"
        f"{BR}\n"
        f"🛠 **COMMANDS:**\n"
        f"• `/buy` - VIEW PRODUCTS\n"
        f"• `/help` - SUPPORT\n"
        f"• `/stats` - SYSTEM LOAD\n"
        f"{BR}"
    )
    await message.reply_photo("https://telegra.ph/file/2e8790380c5e732381284.jpg", caption=CAPTION)

@app.on_message(filters.command("buy"))
async def buy_cmd(client, message):
    await message.reply(f"{BR}\n📦 **AHMED X STOREZ - STOCK LIST**\n{BR}\n1️⃣ **FB INDO FIX** - CONTACT OWNER\n2️⃣ **PREMIUM SESSIONS** - RS. 499\n3️⃣ **STORE BOT CLONE** - RS. 999\n{BR}")

# --- [ OWNER ONLY FUNCTIONS ] ---

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 **REPLY TO A MESSAGE TO BROADCAST.**")
    
    msg = await message.reply("🚀 **BROADCASTING TO ALL USERS...**")
    count = 0
    for user in TOTAL_USERS:
        try:
            await message.reply_to_message.copy(user)
            count += 1
        except: pass
    await msg.edit(f"✅ **BROADCAST COMPLETED! SENT TO {count} USERS.**")

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_auth(client, message):
    try:
        uid = int(message.command[1])
        if uid not in AUTH_USERS: AUTH_USERS.append(uid)
        await message.reply(f"✅ **USER {uid} HAS BEEN AUTHORIZED.**")
    except: await message.reply("❌ **USE: /add 12345678**")

@app.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_user(client, message):
    try:
        uid = int(message.command[1])
        if uid not in BANNED_USERS: BANNED_USERS.append(uid)
        await message.reply(f"🚫 **USER {uid} BANNED FROM STORE.**")
    except: await message.reply("❌ **USE: /ban 12345678**")

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    await message.reply(f"{BR}\n📊 **SYSTEM STATISTICS**\n{BR}\n👥 **TOTAL USERS:** {len(TOTAL_USERS)}\n🛡 **AUTH USERS:** {len(AUTH_USERS)}\n🚫 **BANNED:** {len(BANNED_USERS)}\n{BR}")

# --- [ AUTO-RESPONSE SYSTEM ] ---
@app.on_message(filters.text & ~filters.command(["start", "help", "buy", "add", "ban", "stats"]))
async def echo(client, message):
    if "admin" in message.text.lower():
        await message.reply("👤 **OWNER IS BUSY. USE /help TO VIEW SUPPORT LINKS.**")

if __name__ == "__main__":
    print("🚀 AHMED X PRO ENGINE IS LIVE!")
    app.run()
