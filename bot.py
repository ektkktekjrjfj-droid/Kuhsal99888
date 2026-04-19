import os
import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Logging taaki Render ke logs mein sab dikhe
logging.basicConfig(level=logging.INFO)

# --- [ CONFIG ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8464390807:AAGVxObZ60Se34Kjo3nX34I0iDa8VBAcsRY"

# ✅ UPDATED OWNER ID
OWNER_ID = 6632236983 

app = Client("AhmedX_Final_Fix", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Side Menu Setup (Automation)
async def setup_menu():
    async with app:
        await app.set_bot_commands([
            BotCommand("start", "🚀 Start Premium Bot"),
            BotCommand("indofix", "🛠 Indo Fix System (Owner Only)")
        ])
        print("✅ Side Menu Set Successfully!")

# Selenium Driver Setup for Render
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    service = Service()
    return webdriver.Chrome(service=service, options=options)

# --- [ WELCOME MESSAGE (OWNER ONLY) ] ---
@app.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start(client, message):
    # Aap kisi bhi photo ka direct link yahan daal sakte hain
    photo_url = "https://telegra.ph/file/2e8790380c5e732381284.jpg" 
    
    welcome_text = (
        "🔥 **WELCOME OWNER: AHMED X STOREZ**\n\n"
        "✨ **PREMIUM SETUP X** is active.\n"
        "☁️ Status: **Render Cloud (Online)**\n"
        "🛠 Menu: **Side Commands Activated**\n\n"
        "Aap niche Menu button se `/indofix` select kar sakte hain."
    )
    
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Developer", url="t.me/kushal_storez")]
    ])
    
    try:
        await message.reply_photo(photo=photo_url, caption=welcome_text, reply_markup=buttons)
    except:
        await message.reply_text(welcome_text, reply_markup=buttons)

# --- [ INDOFIX COMMAND (OWNER ONLY) ] ---
@app.on_message(filters.command("indofix"))
async def indofix(client, message):
    # Security Check
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ **Access Denied:** Ye bot sirf Owner ke liye hai.")

    args = message.text.split()
    if len(args) < 3:
        return await message.reply("📝 **Usage:** `/indofix username password`")
    
    msg = await message.reply("⚙️ **Ahmed X Auto-System Engine Starting...**")
    
    driver = None
    try:
        driver = get_driver()
        driver.get("https://business.facebook.com/business/loginpage/")
        await asyncio.sleep(5)
        
        driver.find_element(By.NAME, "email").send_keys(args[1])
        driver.find_element(By.NAME, "pass").send_keys(args[2])
        driver.find_element(By.NAME, "login").click()
        await asyncio.sleep(10)
        
        # Indo Fix Final Hit
        driver.get("https://business.facebook.com/?nav_ref=biz_unified_f3_login_page_to_mbs")
        await asyncio.sleep(5)
        
        await msg.edit("✅ **Ahmed X Fixer:** Account processed successfully!")
    except Exception as e:
        await msg.edit(f"❌ **Cloud Error:** {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # Commands set karke bot start karein
    loop = asyncio.get_event_loop()
    loop.run_until_complete(setup_menu())
    
    print("🚀 AHMED X PREMIUM BOT IS LIVE!")
    app.run()
