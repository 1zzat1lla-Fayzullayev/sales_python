from config import *
from database import *
import cart

def login():
    """Tizimga kirish - YAKUNIY VERSIYA"""
    print_header("TIZIMGA KIRISH")
    
    username = input("Username: ").strip()
    parol = input("Parol: ").strip()
    
    if not username or not parol:
        print("\n✗ Username va parol bo'sh bo'lmasligi kerak!")
        return False
    
    # Faylni tekshirish va tuzatish
    import os
    if not os.path.exists(USERS_FILE):
        print(f"\n✗ {USERS_FILE} fayl topilmadi!")
        print("Fayl yaratilmoqda...")
        from database import create_files
        create_files()
        return False
    
    # CSV faylni tekshirish va header qo'shish (agar yo'q bo'lsa)
    ensure_csv_header(USERS_FILE, ['id', 'username', 'parol', 'ism', 'telefon'])
    
    # Foydalanuvchilarni o'qish
    users = read_csv(USERS_FILE)
    
    print(f"\n[DEBUG] Tizimda {len(users)} ta foydalanuvchi bor.")
    
    if not users:
        print("✗ Hech kim ro'yxatdan o'tmagan!")
        print("Avval ro'yxatdan o'ting.")
        return False
    
    # Login tekshiruvi
    for user in users:
        db_username = str(user.get('username', '')).strip()
        db_parol = str(user.get('parol', '')).strip()
        
        if db_username == username and db_parol == parol:
            cart.current_user = user
            print(f"\n✓ Xush kelibsiz, {user.get('ism', 'Foydalanuvchi')}!")
            
            if username in ADMIN_USERS:
                print("🔑 Admin huquqi bor")
            
            return True
    
    print("\n✗ Username yoki parol noto'g'ri!")
    return False

def register():
    """Ro'yxatdan o'tish - YAKUNIY VERSIYA"""
    print_header("RO'YXATDAN O'TISH")
    
    username = input("Username: ").strip()
    parol = input("Parol: ").strip()
    ism = input("Ism: ").strip()
    telefon = input("Telefon: ").strip()
    
    if not username or not parol or not ism:
        print("\n✗ Barcha maydonlarni to'ldiring!")
        return False
    
    # CSV header tekshiruvi
    ensure_csv_header(USERS_FILE, ['id', 'username', 'parol', 'ism', 'telefon'])
    
    # Mavjud userlarni o'qish
    users = read_csv(USERS_FILE)
    
    # Username tekshiruvi
    for user in users:
        if str(user.get('username', '')).strip() == username:
            print("\n✗ Bu username band!")
            return False
    
    # Yangi ID
    if users:
        new_id = max([int(u.get('id', 0)) for u in users]) + 1
    else:
        new_id = 1
    
    # Saqlash
    success = append_csv(USERS_FILE, [new_id, username, parol, ism, telefon])
    
    if success:
        print(f"\n✓ Ro'yxatdan o'tdingiz, {ism}!")
        print(f"Username: {username}")
        print(f"Parol: {parol}")
        print("\nEndi tizimga kiring (tanlov 7).")
        return True
    else:
        print("\n✗ Xatolik yuz berdi!")
        return False

def logout():
    """Chiqish"""
    if cart.current_user:
        print(f"\n✓ {cart.current_user.get('ism', 'Foydalanuvchi')}, ko'rishguncha!")
        cart.current_user = None

def is_admin():
    """Admin tekshiruvi"""
    if not cart.current_user:
        return False
    return cart.current_user.get('username', '') in ADMIN_USERS

def ensure_csv_header(filename, headers):
    """CSV faylda header borligini tekshirish va qo'shish"""
    import os
    import csv
    
    if not os.path.exists(filename):
        # Fayl yo'q bo'lsa, header bilan yaratish
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
        print(f"[INFO] {filename} yaratildi")
        return
    
    # Faylni o'qish
    with open(filename, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
    
    # Header borligini tekshirish
    if not first_line or first_line.split(',')[0].isdigit():
        # Header yo'q! Qo'shish kerak
        print(f"[WARNING] {filename} da header yo'q! Tuzatilmoqda...")
        
        # Eski ma'lumotlarni o'qish
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Header bilan qayta yozish
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            # Eski ma'lumotlarni yozish
            for line in lines:
                if line.strip():
                    f.write(line)
        
        print(f"[INFO] Header qo'shildi: {','.join(headers)}")

def fix_all_csv_files():
    """Barcha CSV fayllarni tuzatish"""
    print_header("CSV FAYLLARNI TUZATISH")
    
    # Users
    ensure_csv_header(USERS_FILE, ['id', 'username', 'parol', 'ism', 'telefon'])
    
    # Products
    ensure_csv_header(PRODUCTS_FILE, ['id', 'nomi', 'brend', 'ram', 'ssd', 'narx', 'miqdor', 'aksiya'])
    
    # Cart
    ensure_csv_header(CART_FILE, ['user_id', 'product_id', 'nomi', 'narx', 'soni'])
    
    # Orders
    ensure_csv_header(ORDERS_FILE, ['id', 'user_id', 'username', 'mahsulot', 'soni', 'narx', 'jami', 'sana'])
    
    print("\n✓ Barcha CSV fayllar tuzatildi!")
    print("Endi dasturni qayta ishga tushiring.")
