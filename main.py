# xabarnoma_boti.py
import sqlite3
import time

def dasturni_boshlash():
    print("""
    ******************************
    * XABARNOMA YUBORUVCHI BOT   *
    ******************************
    """)

def maqolni_korsat():
    print("\nBot vazifasi:")
    print("""
    Ushbu bot orqali siz ro'yxatdan o'tgan barcha foydalanuvchilarga  
    bir vaqtning o'zida xabarnoma yuborishingiz mumkin. Xabarlar  
    SMS yoki elektron pochta orqali yuborilishi mumkin.
    """)

def menyuni_korsat():
    print("\nMenyu:")
    print("1. Foydalanuvchilar ro'yxati")
    print("2. Xabar yuborish")
    print("3. Hisobot")
    print("4. Chiqish")
    return input("Tanlang (1-4): ")

def foydalanuvchilarni_korsat():
    boglanma = sqlite3.connect('foydalanuvchilar.db')
    kurs = boglanma.cursor()
    
    print("\nFoydalanuvchilar ro'yxati:")
    print("{:<5} {:<15} {:<15} {:<20}".format("ID", "Ism", "Telefon", "Ro'yxatdan o'tgan sana"))
    print("-" * 60)
    
    for row in kurs.execute("SELECT * FROM foydalanuvchilar"):
        print("{:<5} {:<15} {:<15} {:<20}".format(row[0], row[1], row[2], row[3]))
    
    boglanma.close()
    input("\nDavom etish uchun Enter tugmasini bosing...")

def xabar_yubor():
    print("\nXabar yuborish:")
    mavzu = input("Xabar mavzusi: ")
    matn = input("Xabar matni: ")
    
    qabul_qiluvchilar = foydalanuvchilarni_olish()
    if not qabul_qiluvchilar:
        print("Hech qanday foydalanuvchi topilmadi!")
        return
    
    print(f"\nXabar {len(qabul_qiluvchilar)} ta foydalanuvchiga yuborilmoqda...")
    for foydalanuvchi in qabul_qiluvchilar:
        print(f"{foydalanuvchi[1]} ({foydalanuvchi[2]}) ga xabar yuborilmoqda...")
        # SMS yoki e-mail yuborish logikasi shu joyga qo'shiladi
        time.sleep(0.5)  # Demo uchun kutish
    
    print("\nXabarlar muvaffaqiyatli yuborildi!")
    input("Davom etish uchun Enter tugmasini bosing...")

def foydalanuvchilarni_olish():
    boglanma = sqlite3.connect('foydalanuvchilar.db')
    kurs = boglanma.cursor()
    kurs.execute("SELECT * FROM foydalanuvchilar")
    natijalar = kurs.fetchall()
    boglanma.close()
    return natijalar

def hisobot():
    boglanma = sqlite3.connect('foydalanuvchilar.db')
    kurs = boglanma.cursor()
    
    # Foydalanuvchilar soni
    kurs.execute("SELECT COUNT(*) FROM foydalanuvchilar")
    foydalanuvchilar_soni = kurs.fetchone()[0]
    
    print(f"\nJami foydalanuvchilar: {foydalanuvchilar_soni}")
    
    # Oxirgi 5 ta xabar
    print("\nOxirgi 5 ta yuborilgan xabar:")
    for row in kurs.execute("SELECT * FROM xabarlar ORDER BY yuborilgan_sana DESC LIMIT 5"):
        print(f"{row[2]} | {row[3]} | {row[5]} ta foydalanuvchiga yuborilgan")
    
    boglanma.close()
    input("\nDavom etish uchun Enter tugmasini bosing...")

def asosiy():
    dbni_boshlash()
    dasturni_boshlash()
    maqolni_korsat()
    
    while True:
        tanlov = menyuni_korsat()
        
        if tanlov == "1":
            foydalanuvchilarni_korsat()
        elif tanlov == "2":
            xabar_yubor()
        elif tanlov == "3":
            hisobot()
        elif tanlov == "4":
            print("Dastur tugatildi. Xayr!")
            break
        else:
            print("Noto'g'ri tanlov! Qaytadan urinib ko'ring.")

if __name__ == "__main__":
    asosiy()
