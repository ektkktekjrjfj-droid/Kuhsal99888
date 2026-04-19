import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from motor.motor_asyncio import AsyncIOMotorClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# LOGGING SETUP
logging.basicConfig(level=logging.INFO)

# --- [ CONFIGURATION ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8464390807:AAGVxObZ60Se34Kjo3nX34I0iDa8VBAcsRY"
OWNER_ID = 6632236983 

# MONGODB CONNECTION
MONGO_URL = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["AhmedX_Storez"]
auth_col = db["authorized_users"] 

app = Client("AhmedX_Ultra_Bold", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ SELENIUM ENGINE ] ---
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    return webdriver.Chrome(options=options)

async def is_authorized(user_id):
    if user_id == OWNER_ID: return True
    user = await auth_col.find_one({"user_id": user_id})
    return True if user else False

# --- [ SIDE MENU CONFIG ] ---
async def setup_bot():
    async with app:
        await app.set_bot_commands([
            BotCommand("start", "🚀 START PREMIUM SYSTEM"),
            BotCommand("indofix", "🛠 RUN INDO FIX ENGINE"),
            BotCommand("add", "➕ AUTHORIZE NEW USER"),
            BotCommand("remove", "➖ TERMINATE USER ACCESS"),
            BotCommand("users", "👥 VIEW ALL AUTHORIZED USERS")
        ])

# --- [ UI TEXTURE DESIGN ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

@app.on_message(filters.command("start"))
async def start(client, message):
    auth = await is_authorized(message.from_user.id)
    photo = "https://telegra.ph/file/2e8790380c5e732381284.jpg"
    
    STATUS = "✅ ⚡ AUTHORIZED ⚡" if auth else "❌ ⚡ ACCESS DENIED ⚡"
    
    CAPTION = (
        f"{BR}\n"
        f"🔥 **WELCOME TO AHMED X STOREZ**\n"
        f"{BR}\n"
        f"👤 **USER:** {message.from_user.first_name.upper()}\n"
        f"🆔 **ID:** `{message.from_user.id}`\n"
        f"🛡 **STATUS:** {STATUS}\n"
        f"🌐 **SERVER:** RENDER CLOUD [NODE-01]\n"
        f"{BR}\n"
        f"✨ **PREMIUM SETUP X IS ACTIVE**\n"
        f"{BR}"
    )
    await message.reply_photo(photo=photo, caption=CAPTION)

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_user(client, message):
    if len(message.command) < 2:
        return await message.reply(f"{BR}\n📝 **ERROR: PROVIDE USER ID**\n{BR}")
    target_id = int(message.command[1])
    await auth_col.update_one({"user_id": target_id}, {"$set": {"auth": True}}, upsert=True)
    await message.reply(f"{BR}\n✅ **USER {target_id} AUTHORIZED**\n{BR}")

@app.on_message(filters.command("remove") & filters.user(OWNER_ID))
async def remove_user(client, message):
    if len(message.command) < 2:
        return await message.reply(f"{BR}\n📝 **ERROR: PROVIDE USER ID**\n{BR}")
    target_id = int(message.command[1])
    await auth_col.delete_one({"user_id": target_id})
    await message.reply(f"{BR}\n➖ **USER {target_id} REMOVED**\n{BR}")

@app.on_message(filters.command("users") & filters.user(OWNER_ID))
async def list_users(client, message):
    cursor = auth_col.find({})
    users = await cursor.to_list(length=100)
    REPLY = f"{BR}\n👥 **AUTHORIZED USER LIST**\n{BR}\n"
    if not users:
        REPLY += "EMPTY LIST"
    else:
        for idx, u in enumerate(users, 1):
            REPLY += f"{idx}. `{u['user_id']}`\n"
    REPLY += f"{BR}"
    await message.reply(REPLY)

@app.on_message(filters.command("indofix"))
async def indofix(client, message):
    if not await is_authorized(message.from_user.id):
        return await message.reply(f"{BR}\n❌ **ACCESS DENIED: CONTACT OWNER**\n{BR}")

    args = message.text.split()
    if len(args) < 3:
        return await message.reply(f"{BR}\n📝 **USAGE: /INDOFIX [USER] [PASS]**\n{BR}")
    
    MSG = await message.reply(f"{BR}\n⚙️ **AHMED X ENGINE: PROCESSING...**\n{BR}")
    driver = None
    try:
        driver = get_driver()
        driver.get("https://business.facebook.com/business/loginpage/")
        await asyncio.sleep(5)
        driver.find_element(By.NAME, "email").send_keys(args[1])
        driver.find_element(By.NAME, "pass").send_keys(args[2])
        driver.find_element(By.NAME, "login").click()
        await asyncio.sleep(10)
        driver.get("https://business.facebook.com/?nav_ref=biz_unified_f3_login_page_to_mbs")
        await asyncio.sleep(5)
        await MSG.edit(f"{BR}\n✅ **INDO FIX COMPLETED BY AHMED X**\n{BR}")
    except Exception as e:
        await MSG.edit(f"{BR}\n❌ **ERROR:** {str(e).upper()}\n{BR}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_bot())
    app.run()
