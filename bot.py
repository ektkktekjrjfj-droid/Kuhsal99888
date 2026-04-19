import os
import asyncio
import logging
from pyrogram import Client, filters

# --- [ LOGGING ] ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AhmedX")

# --- [ CONFIGURATION ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "IDHAR_NAYA_TOKEN_DALO" # <--- APNA NAYA TOKEN PASTE KARO
OWNER_ID = 6632236983 

# IN-MEMORY STORAGE (NO MONGODB NEEDED)
AUTHORIZED_USERS = {OWNER_ID}
TOTAL_USERS = set()

app = Client("AhmedX_Survivor", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ UI DESIGN ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

# --- [ COMMANDS ] ---

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
        f"🌐 **SERVER:** RENDER CLOUD 2026\n"
        f"{BR}\n"
        f"🛠 **AVAILABLE FUNCTIONS:**\n"
        f"• `/buy` - VIEW STORE ITEMS\n"
        f"• `/help` - SUPPORT CENTER\n"
        f"• `/stats` - USER STATISTICS\n"
        f"{BR}"
    )
    await message.reply_photo("https://telegra.ph/file/2e8790380c5e732381284.jpg", caption=CAPTION)

@app.on_message(filters.command("buy"))
async def buy(client, message):
    await message.reply(f"{BR}\n📦 **AHMED X STORE STOCK**\n{BR}\n1. **FB INDO FIX** - DM OWNER\n2. **PREMIUM SESSION** - ₹499\n3. **BOT CLONING** - ₹999\n{BR}")

# --- [ OWNER ONLY: BROADCAST & ADMIN ] ---

@app.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if not message.reply_to_message:
        return await message.reply("📝 **REPLY TO A MESSAGE TO BROADCAST.**")
    
    msg = await message.reply("🚀 **AHMED X ENGINE: SENDING...**")
    done = 0
    for user in TOTAL_USERS:
        try:
            await message.reply_to_message.copy(user)
            done += 1
            await asyncio.sleep(0.1)
        except: pass
    await msg.edit(f"✅ **BROADCAST DONE: {done} USERS.**")

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_auth(client, message):
    try:
        uid = int(message.command[1])
        AUTHORIZED_USERS.add(uid)
        await message.reply(f"✅ **USER `{uid}` AUTHORIZED SUCCESSFULLY.**")
    except: await message.reply("❌ **FORMAT: /add 12345678**")

@app.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(client, message):
    await message.reply(f"{BR}\n📊 **STORE STATISTICS**\n{BR}\n👥 **TOTAL USERS:** {len(TOTAL_USERS)}\n🛡 **AUTHORIZED:** {len(AUTHORIZED_USERS)}\n{BR}")

# --- [ STARTUP ENGINE ] ---
if __name__ == "__main__":
    logger.info("🚀 AHMED X PRO IS STARTING...")
    app.run()
