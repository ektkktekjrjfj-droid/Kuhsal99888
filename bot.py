import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- [ CONFIG ] ---
API_ID = 6632236983
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8464390807:AAGVxObZ60Se34Kjo3nX34I0iDa8VBAcsRY"

# 👑 OWNER ID (Yahan apni Telegram ID dalo)
OWNER_ID = 123456789 

app = Client("AhmedX_Final", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Selenium Setup for Cloud
def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"
    service = Service()
    return webdriver.Chrome(service=service, options=options)

# --- [ SIDE MENU COMMANDS SETUP ] ---
async def set_commands():
    async with app:
        await app.set_bot_commands([
            BotCommand("start", "🚀 Bot ko start karein"),
            BotCommand("indofix", "🛠 Indo Fix System (Owner Only)"),
            BotCommand("help", "❓ Help aur Jankari")
        ])
        print("✅ Side Menu Commands Updated!")

# --- [ START COMMAND WITH PHOTO ] ---
@app.on_message(filters.command("start") & filters.user(OWNER_ID))
async def start(client, message):
    # Aap is link ko apni kisi bhi image link se badal sakte hain
    photo_url = "https://telegra.ph/file/your_image_link.jpg" 
    welcome_text = (
        "🔥 **WELCOME OWNER: AHMED X STOREZ**\n\n"
        "✨ **PREMIUM SETUP X** is active.\n"
        "☁️ Server: **Render Cloud (Online)**\n\n"
        "Aapki commands niche menu mein set kar di gayi hain."
    )
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛠 Use Indo Fix", callback_data="run_fix")],
        [InlineKeyboardButton("👤 Support", url="t.me/your_username")]
    ])
    
    try:
        await message.reply_photo(photo=photo_url, caption=welcome_text, reply_markup=buttons)
    except:
        await message.reply_text(welcome_text, reply_markup=buttons)

# --- [ INDOFIX COMMAND ] ---
@app.on_message(filters.command("indofix"))
async def indofix(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("❌ **Access Denied:** Ye bot sirf Owner ke liye hai.")

    args = message.text.split()
    if len(args) < 3:
        return await message.reply("📝 **Usage:** `/indofix user pass` (Ya menu se select karein)")
    
    msg = await message.reply("⚙️ **Ahmed X Auto-System Starting...**")
    
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
        
        driver.quit()
        await msg.edit("✅ **Ahmed X Fixer:** Success! Account processed.")
    except Exception as e:
        if 'driver' in locals(): driver.quit()
        await msg.edit(f"❌ **Cloud Error:** {str(e)}")

if __name__ == "__main__":
    # Bot start hote hi menu commands set karega
    loop = asyncio.get_event_loop()
    loop.run_until_complete(set_commands())
    
    print("🚀 AHMED X PREMIUM BOT IS LIVE...")
    app.run()
