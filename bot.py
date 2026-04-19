import os
import asyncio
import logging
from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient

# LOGGING
logging.basicConfig(level=logging.INFO)

# --- [ CONFIGURATION ] ---
API_ID = 21552435
API_HASH = "5b108bd2fdd31c0c34bc65f24a5216a0"
BOT_TOKEN = "8464390807:AAGVxObZ60Se34Kjo3nX34I0iDa8VBAcsRY"
OWNER_ID = 6632236983 

# MONGODB CONNECTION
MONGO_URL = "mongodb+srv://Elevenyts:Elevenyts@cluster0.vuyc1u2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
db_client = AsyncIOMotorClient(MONGO_URL)
db = db_client["AHMEDX_DB"]
auth_col = db["AUTH_USERS"] 

app = Client("AHMEDX_FINAL_FIX", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# --- [ UI DESIGN ] ---
BR = "━━━━━━━━━━━━━━━━━━━━━━━━"

async def is_authorized(user_id):
    if user_id == OWNER_ID: return True
    user = await auth_col.find_one({"user_id": user_id})
    return True if user else False

# --- [ COMMANDS ] ---

@app.on_message(filters.command("start"))
async def start(client, message):
    auth = await is_authorized(message.from_user.id)
    STATUS = "✅ ⚡ AUTHORIZED ⚡" if auth else "❌ ⚡ ACCESS DENIED ⚡"
    
    CAPTION = (
        f"{BR}\n"
        f"🔥 **WELCOME TO AHMED X STOREZ**\n"
        f"{BR}\n"
        f"👤 **USER:** {message.from_user.first_name.upper()}\n"
        f"🆔 **ID:** `{message.from_user.id}`\n"
        f"🛡 **STATUS:** {STATUS}\n"
        f"🌐 **SERVER:** RENDER CLOUD [LIVE]\n"
        f"{BR}\n"
        f"✨ **PREMIUM SETUP X ACTIVE**\n"
        f"{BR}"
    )
    await message.reply_photo("https://telegra.ph/file/2e8790380c5e732381284.jpg", caption=CAPTION)

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
    await message.reply(f"{BR}\n➖ **USER {target_id} ACCESS TERMINATED**\n{BR}")

@app.on_message(filters.command("users") & filters.user(OWNER_ID))
async def list_users(client, message):
    cursor = auth_col.find({})
    users = await cursor.to_list(length=100)
    REPLY = f"{BR}\n👥 **AUTHORIZED LIST**\n{BR}\n"
    if users:
        REPLY += "\n".join([f"• `{u['user_id']}`" for u in users])
    else:
        REPLY += "EMPTY DATABASE"
    await message.reply(f"{REPLY}\n{BR}")

if __name__ == "__main__":
    app.run()
