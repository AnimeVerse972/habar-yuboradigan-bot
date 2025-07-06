import sqlite3
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# ADMINLAR RO'YXATI - BU YERGA O'Z ID'LARINGIZNI QO'YING
ADMIN_IDS = [6486825926]  # Misol: [123456789, 987654321]

def get_conn():
    return sqlite3.connect("bot.db")

async def send_message_to_all_users(context: CallbackContext, message: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    users = cur.fetchall()
    
    success = 0
    failed = 0
    
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user[0],
                text=message
            )
            success += 1
        except Exception as e:
            print(f"Xatolik (ID: {user[0]}): {e}")
            failed += 1
    
    conn.close()
    return success, failed

def add_user_to_db(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    add_user_to_db(user_id)
    await update.message.reply_text(
        "👋 Assalomu alaykum! Men sizga muhim xabarlarni yuborish uchun botman.\n\n"
        "Agar admin bo'lsangiz, /send buyrug'i orqali xabar yuborishingiz mumkin."
    )

async def send_to_all(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Sizda bunday buyruqni bajarish huquqi yo'q!")
        return
    
    if not context.args:
        await update.message.reply_text("📝 Xabar matnini kiriting:\n/send <xabar matni>")
        return
    
    message_text = " ".join(context.args)
    success, failed = await send_message_to_all_users(context, message_text)
    
    await update.message.reply_text(
        f"📊 Xabar yuborish natijasi:\n\n"
        f"✅ Muvaffaqiyatli: {success} ta\n"
        f"❌ Muvaffaqiyatsiz: {failed} ta\n\n"
        f"Jami foydalanuvchilar: {success + failed} ta"
    )

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("send", send_to_all))

    updater.start_polling()
    print("🤖 Bot ishga tushdi...")
    updater.idle()

if __name__ == '__main__':
    main()
