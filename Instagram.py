import asyncio
import yt_dlp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import datetime
import config # Saari details config.py se uthayega

# --- CLIENTS SETUP ---
app = Client(
    "KushalMusicBot", 
    api_id=config.API_ID, 
    api_hash=config.API_HASH, 
    bot_token=config.BOT_TOKEN
)

user_app = Client(
    "KushalUserBot", 
    api_id=config.API_ID, 
    api_hash=config.API_HASH, 
    session_string=config.STRING_SESSION
)

call_py = PyTgCalls(user_app)

# --- UTILS (Exact Real-Time Design) ---
def get_seekbar(current, total):
    percentage = (current / (total if total > 0 else 1)) * 100
    completed = int(percentage / 10)
    remaining = 10 - completed
    return f"{format_time(current)} {'━' * completed}🔘{'━' * remaining} {format_time(total)}"

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))[2:].split('.')[0]

# --- PLAY HANDLER (GROUP ONLY) ---
@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        return await message.reply_text("🔎 **Gᴀᴀɴᴇ ᴋᴀ ɴᴀᴀᴍ ʟɪᴋʜᴏ!**")

    query = " ".join(message.command[1:])
    m = await message.reply_text("🔎 **Sᴇᴀʀᴄʜɪɴɢ...**")
    chat_id = message.chat.id

    # ANTI-OVERLAP: Naya chalne se pehle purana band
    try:
        await call_py.leave_group_call(chat_id)
    except:
        pass

    ydl_opts = {'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            url = info['url']
            title = info.get('title', 'Music')
            duration_sec = info.get('duration', 0)
            thumb = info.get('thumbnail')
            dur_min = format_time(duration_sec)

        # Assistant VC join karega
        await call_py.join_group_call(chat_id, AudioPiped(url))

        # UI Text (Branding Removed)
        caption = (
            f"➻ **Sᴛᴀʀᴛᴇᴅ Sᴛʀᴇᴀᴍɪɴɢ |** ❞\n\n"
            f"✨ **Tɪᴛʟᴇ :** #{title[:35]}...\n"
            f"⏱ **Dᴜʀᴀᴛɪᴏɴ :** {dur_min} **ᴍɪɴᴜᴛᴇs**\n"
            f"🥀 **Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** 🦋💸 ⃪♔‌⃟𝐊𝐔𝐒𝐇𝐀𝐋"
        )

        def player_buttons(curr):
            return InlineKeyboardMarkup([
                [InlineKeyboardButton(get_seekbar(curr, duration_sec), callback_data="none")],
                [
                    InlineKeyboardButton("▷", "resume_cb"), 
                    InlineKeyboardButton("II", "pause_cb"), 
                    InlineKeyboardButton("↻", "replay_cb"), 
                    InlineKeyboardButton("‣‣", "skip_cb"), 
                    InlineKeyboardButton("▢", "stop_cb")
                ],
                [InlineKeyboardButton("➕ Aᴅᴅ Mᴇ", url=f"https://t.me/{client.me.username}?startgroup=true")]
            ])

        post = await message.reply_photo(
            photo=thumb if thumb else "https://telegra.ph/file/bc3343358055a40b85354.jpg",
            caption=caption,
            reply_markup=player_buttons(0)
        )
        await m.delete()

        # Real-time update loop
        curr_time = 0
        while curr_time < duration_sec:
            await asyncio.sleep(10)
            curr_time += 10
            try:
                await post.edit_reply_markup(reply_markup=player_buttons(curr_time))
            except: break

    except Exception as e:
        await m.edit(f"❌ Error: {e}")

# --- CALLBACK HANDLERS ---
@app.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    chat_id = query.message.chat.id
    if query.data == "pause_cb":
        await call_py.pause_stream(chat_id)
        await query.answer("Stream Paused ⏸")
    elif query.data == "resume_cb":
        await call_py.resume_stream(chat_id)
        await query.answer("Stream Resumed ▶️")
    elif query.data == "stop_cb":
        await call_py.leave_group_call(chat_id)
        await query.message.delete()
        await query.answer("Stream Stopped 🛑")

# --- START ---
async def start_bot():
    await app.start()
    await user_app.start()
    await call_py.start()
    print("✅ Music Bot Ready to Blast!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bot())