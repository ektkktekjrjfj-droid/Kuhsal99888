import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from pyrogram import Client, filters

# --- [ CONFIG ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
# Aapka Naya Token
BOT_TOKEN = "8464390807:AAGVxObZ60Se34Kjo3nX34I0iDa8VBAcsRY"

app = Client("AhmedX_AutoFix", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_data = {}

async def automation_logic(client, message, user, pwd):
    options = Options()
    options.add_argument("--headless") # Screen nahi dikhegi
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"
    
    # 🚨 PATH FIX: Seedha system driver ko point kar raha hai
    service = Service("/usr/bin/chromedriver")
    
    try:
        driver = webdriver.Chrome(service=service, options=options)
        
        # Step 1: Login Page
        driver.get("https://business.facebook.com/business/loginpage/")
        await asyncio.sleep(5)
        
        driver.find_element(By.NAME, "email").send_keys(user)
        driver.find_element(By.NAME, "pass").send_keys(pwd)
        driver.find_element(By.NAME, "login").click()
        await asyncio.sleep(10)
        
        # Step 2: 2FA (Twist Verification) Check
        if "checkpoint" in driver.current_url:
            await message.reply("🔐 **Bhai Code (OTP) Maang Raha Hai!**\nJaldi se 6-digit code yahan likho:")
            user_data[message.from_user.id] = None
            
            for _ in range(60): # 1 minute wait
                if user_data[message.from_user.id]:
                    otp = user_data[message.from_user.id]
                    driver.find_element(By.ID, "approvals_code").send_keys(otp)
                    driver.find_element(By.ID, "checkpointSubmitButton").click()
                    await asyncio.sleep(5)
                    break
                await asyncio.sleep(1)
        
        # Step 3: Final Link Hit (Indo Fix)
        driver.get("https://business.facebook.com/?nav_ref=biz_unified_f3_login_page_to_mbs")
        await asyncio.sleep(5)
        
        driver.quit()
        return "✅ **Ahmed X Fixer:** Account successfully link ho gaya!"

    except Exception as e:
        return f"❌ **Error:** {str(e)}"

@app.on_message(filters.command("indofix"))
async def start_fix(client, message):
    args = message.text.split()
    if len(args) < 3:
        return await message.reply("📝 **Usage:** `/indofix username password`")
    
    status = await message.reply("⚙️ **Ahmed X Auto-System Started...**")
    res = await automation_logic(client, message, args[1], args[2])
    await status.edit(res)

@app.on_message(filters.text & ~filters.command("indofix"))
async def catch_otp(client, message):
    if message.from_user.id in user_data:
        user_data[message.from_user.id] = message.text
        await message.reply("📥 **OTP mil gaya!** Aage badh raha hoon...")

print("🔥 FULL AUTO-FIXER RUNNING...")
app.run()