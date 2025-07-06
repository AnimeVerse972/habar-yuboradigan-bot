import sqlite3

def get_conn():
    return sqlite3.connect("bot.db")

def add_user(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_user_count():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    conn.close()
    return count

def add_kino_code(code, channel, message_id, post_count):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS kino_codes (
        code TEXT PRIMARY KEY,
        channel TEXT,
        message_id INTEGER,
        post_count INTEGER
    )""")
    cur.execute("INSERT OR REPLACE INTO kino_codes (code, channel, message_id, post_count) VALUES (?, ?, ?, ?)",
                (code, channel, message_id, post_count))
    conn.commit()
    conn.close()

def get_kino_by_code(code):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT channel, message_id, post_count FROM kino_codes WHERE code = ?", (code,))
    data = cur.fetchone()
    conn.close()
    return data

def get_all_codes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM kino_codes")
    data = cur.fetchall()
    conn.close()
    return data

def send_message_to_all_users(message):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM users")
    users = cur.fetchall()
    
    for user in users:
        user_id = user[0]
        # Bu yerda xabar yuborish logikasini qo'shishingiz kerak
        print(f"Xabar yuborilmoqda: {message} foydalanuvchiga {user_id}")
        # Masalan, Telegram API orqali xabar yuborish
        # bot.send_message(chat_id=user_id, text=message)
    
    conn.close()

# Misol uchun, foydalanuvchilarni qo'shish va xabar yuborish
if __name__ == "__main__":
    # Foydalanuvchilarni qo'shish
    add_user(123456789)
    add_user(987654321)

    # Foydalanuvchilar sonini olish
    print(f"Jami foydalanuvchilar: {get_user_count()}")

    # Xabar yuborish
    send_message_to_all_users("Salom, bu xabar barcha foydalanuvchilarga yuborildi!")
