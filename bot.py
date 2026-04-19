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

# Logging setup
logging.basicConfig(level=logging.INFO)

# --- [ CONFIG ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8464390807:AAGVxObZ60Se34Kjo3nX34I0iDa8VBAcsRY"
OWNER_ID = 6632236983 

# MongoDB Connection
MONGO_URL = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["AhmedX_Storez"]
auth_col = db["authorized_users"] 

app = Client("AhmedX_Final", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ HELPERS ] ---
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    service = Service()
    return webdriver.Chrome(service=service, options=options)

async def is_authorized(user_id):
    if user_id == OWNER_ID:
        return True
    user = await auth_col.find_one({"user_id": user_id})
    return True if user else False

# --- [ SIDE MENU SETUP ] ---
async def setup_bot():
    async with app:
        await app.set_bot_commands([
            BotCommand("start", "🚀 Start Premium Bot"),
            BotCommand("indofix", "🛠 Run Indo Fix System"),
            BotCommand("add", "➕ User Add (Admin)"),
            BotCommand("remove", "➖ User Remove (Admin)"),
            BotCommand("users", "👥 Authorized List")
        ])

# --- [ ADMIN COMMANDS ] ---

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_user(client, message):
    if len(message.command) < 2:
        return await message.reply("📝 Usage: `/add 123456789`")
    target_id = int(message.command[1])
    await auth_col.update_one({"user_id": target_id}, {"$set": {"auth": True}}, upsert=True)
    await message.reply(f"✅ User `{target_id}` Authorized!")

@app.on_message(filters.command("remove") & filters.user(OWNER_ID))
async def remove_user(client, message):
    if len(message.command) < 2:
        return await message.reply("📝 Usage: `/remove 123456789`")
    target_id = int(message.command[1])
    await auth_col.delete_one({"user_id": target_id})
    await message.reply(f"➖ User `{target_id}` Removed!")

@app.on_message(filters.command("users") & filters.user(OWNER_ID))
async def list_users(client, message):
    users = await auth_col.find().to_list(length=100)
    reply = "👥 **Authorized Users:**\n" + "\n".join([f"• `{u['user_id']}`" for u in users])
    await message.reply(reply if users else "List khali hai.")

# --- [ BOT LOGIC ] ---

@app.on_message(filters.command("start"))
async def start(client, message):
    auth = await is_authorized(message.from_user.id)
    photo = "https://telegra.ph/file/2e8790380c5e732381284.jpg"
    text = f"🔥 **AHMED X STOREZ PREMIUM**\n\n👤: {message.from_user.first_name}\n🛡: {'✅ Authorized' if auth else '❌ No Access'}"
    await message.reply_photo(photo=photo, caption=text)

@app.on_message(filters.command("indofix"))
async def indofix(client, message):
    if not await is_authorized(message.from_user.id):
        return await message.reply("❌ Access Denied!")

    args = message.text.split()
    if len(args) < 3:
        return await message.reply("📝 Usage: `/indofix user pass`")
    
    status = await message.reply("⚙️ **Processing Account...**")
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
        await status.edit("✅ **Indo Fix Success!**")
    except Exception as e:
        await status.edit(f"❌ **Error:** {str(e)}")
    finally:
        if driver: driver.quit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_bot())
    app.run()
