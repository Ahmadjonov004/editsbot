from pyrogram import Client, filters
from pyrogram.types import Message
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1

# Bot sozlamalari
API_ID = 123456  # my.telegram.org saytida API_ID oling
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

# Botni ishga tushirish
app = Client("music_editor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Foydalanuvchi usernameini saqlash uchun o'zgaruvchi
allowed_channel = None

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "Assalomu alaykum! Bu bot kanalingizga yuklangan qo'shiqlarni avtomatik tahrirlaydi. "
        "Kanal usernameini kiritish uchun /setchannel buyrug'idan foydalaning."
    )

@app.on_message(filters.command("setchannel"))
async def set_channel(client, message):
    global allowed_channel
    if len(message.command) < 2:
        await message.reply("Iltimos, kanal usernameini yuboring. Masalan: `/setchannel @kanal_username`")
        return
    
    allowed_channel = message.command[1]
    await message.reply(f"Kanal sozlandi: {allowed_channel}")

@app.on_message(filters.chat(allowed_channel) & filters.audio)
async def edit_audio(client, message: Message):
    # Audio faylni yuklab olish
    file_path = await message.download()
    
    # MP3 faylini o'qish va tahrirlash
    audio = MP3(file_path, ID3=ID3)
    if not audio.tags:
        audio.add_tags()
    audio.tags.add(TIT2(encoding=3, text="Yangi Qo'shiq Nomi"))
    audio.tags.add(TPE1(encoding=3, text="Ijrochining Ismi"))
    audio.save()
    
    # Tahrirlangan faylni qayta yuklash
    await message.reply_audio(audio=open(file_path, "rb"), caption="Tahrirlangan qo'shiq")

# Botni ishga tushirish
app.run()
