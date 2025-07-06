import os
import psycopg2
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher.filters import Command
from dotenv import load_dotenv

load_dotenv(".env")

# === CONFIG ===
BOT_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))  # Optional, fallback 0
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_PORT = os.getenv("DB_PORT")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# === DB ULASH ===
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT,
    sslmode='require'
)
cursor = conn.cursor()

# Jadval yaratish
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY
    );
""")
conn.commit()

# Foydalanuvchini qo‘shish
def add_user(user_id):
    cursor.execute("INSERT INTO users (user_id) VALUES (%s) ON CONFLICT DO NOTHING;", (user_id,))
    conn.commit()

# Barcha foydalanuvchilarni olish
def get_all_users():
    cursor.execute("SELECT user_id FROM users;")
    return [row[0] for row in cursor.fetchall()]

# /start komandasi
@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    add_user(message.from_user.id)
    await message.answer("✅ Botga xush kelibsiz!")

# /sendall komandasi (faqat admin)
@dp.message_handler(commands=["sendall"])
async def send_all_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Siz admin emassiz.")
    
    await message.answer("✍️ Yubormoqchi bo‘lgan xabaringizni yozing:")

    @dp.message_handler()
    async def get_and_send(msg: types.Message):
        user_ids = get_all_users()
        sent = 0
        for uid in user_ids:
            try:
                await bot.send_message(uid, msg.text)
                sent += 1
            except:
                pass
        await msg.answer(f"✅ {sent} ta foydalanuvchiga yuborildi.")
        dp.message_handlers.unregister(get_and_send)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
