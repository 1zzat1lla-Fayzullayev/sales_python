import csv
import os
from datetime import datetime

if not os.path.exists('database'):
    os.makedirs('database')

PRODUCTS_FILE = 'database/products.csv'
CUSTOMERS_FILE = 'database/customers.csv'
ORDERS_FILE = 'database/orders.csv'
CART_FILE = 'database/cart.csv'

CATEGORIES = {
    '1': 'Oshxona texnikasi',
    '2': 'Tozalash uskunalari',
    '3': 'Isitish va sovitish',
    '4': 'Shaxsiy parvarish',
    '5': 'Aqlli uy texnikasi'
}

MEMBERSHIPS = {
    'Bronze': {'chegirma': 5, 'ball': 1, 'yetkazish': 15000},
    'Silver': {'chegirma': 10, 'ball': 2, 'yetkazish': 10000},
    'Gold': {'chegirma': 15, 'ball': 3, 'yetkazish': 0},
    'Biznes': {'chegirma': 20, 'ball': 5, 'yetkazish': 0}
}

current_customer = None

def create_files():    
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nomi', 'kategoriya', 'narx', 'miqdor', 'aksiya'])
            writer.writerow(['1', 'Samsung Muzlatgich', 'Isitish va sovitish', '3500000', '10', '10'])
            writer.writerow(['2', 'LG Kir yuvish mashinasi', 'Tozalash uskunalari', '2800000', '5', '0'])
            writer.writerow(['3', 'Tefal Blender', 'Oshxona texnikasi', '450000', '15', '15'])
            writer.writerow(['4', 'Philips Soch quritgich', 'Shaxsiy parvarish', '280000', '20', '0'])
            writer.writerow(['5', 'Xiaomi Aqlli chiroq', 'Aqlli uy texnikasi', '120000', '30', '5'])
    
    if not os.path.exists(CUSTOMERS_FILE):
        with open(CUSTOMERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'ism', 'telefon', 'manzil', 'azolik', 'ballar'])
            writer.writerow(['1', 'Admin', '998901234567', 'Toshkent', 'Gold', '100'])
    
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'mijoz_id', 'mahsulot_nomi', 'soni', 'narx', 'jami', 'yetkazish', 'sana'])
    
    if not os.path.exists(CART_FILE):
        with open(CART_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['mijoz_id', 'mahsulot_id', 'mahsulot_nomi', 'narx', 'soni'])

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nDavom etish uchun Enter bosing...")

def format_price(price):
    return f"{int(price):,} so'm".replace(',', ' ')

def print_header(title):
    print("\n" + "="*60)
    print(title.center(60))
    print("="*60)

def print_table(headers, rows):
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(str(cell)))
    
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(border)
    print("|" + "|".join(f" {h:<{widths[i]}} " for i, h in enumerate(headers)) + "|")
    print(border)
    for row in rows:
        print("|" + "|".join(f" {str(cell):<{widths[i]}} " for i, cell in enumerate(row)) + "|")
    print(border)

def get_products():
    products = []
    with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append(row)
    return products

def show_categories():
    print_header("KATEGORIYALAR")
    for key, value in CATEGORIES.items():
        print(f"{key}. {value}")
    print("0. Ortga")

def show_products_by_category(category_id):
    if category_id not in CATEGORIES:
        print("Noto'g'ri kategoriya!")
        return
    
    category_name = CATEGORIES[category_id]
    products = get_products()
    
    filtered = [p for p in products if p['kategoriya'] == category_name]
    
    if not filtered:
        print(f"\n'{category_name}' kategoriyasida mahsulot yo'q!")
        return
    
    print_header(f"KATEGORIYA: {category_name}")
    
    headers = ['ID', 'Nomi', 'Narx', 'Miqdor', 'Aksiya']
    rows = []
    
    for p in filtered:
        aksiya = int(p['aksiya'])
        narx = int(p['narx'])
        
        if aksiya > 0:
            yangi_narx = narx * (100 - aksiya) / 100
            narx_text = f"{format_price(yangi_narx)} (-{aksiya}%)"
        else:
            narx_text = format_price(narx)
        
        rows.append([
            p['id'],
            p['nomi'],
            narx_text,
            p['miqdor'],
            f"{aksiya}%" if aksiya > 0 else "-"
        ])
    
    print_table(headers, rows)

def search_products():
    print_header("MAHSULOT QIDIRISH")
    query = input("Mahsulot nomini kiriting: ").lower()
    
    products = get_products()
    results = [p for p in products if query in p['nomi'].lower()]
    
    if not results:
        print("\nHech narsa topilmadi!")
        return
    
    print(f"\nTopildi: {len(results)} ta mahsulot\n")
    
    headers = ['ID', 'Nomi', 'Kategoriya', 'Narx', 'Miqdor']
    rows = []
    
    for p in results:
        aksiya = int(p['aksiya'])
        narx = int(p['narx'])
        
        if aksiya > 0:
            yangi_narx = narx * (100 - aksiya) / 100
            narx_text = f"{format_price(yangi_narx)} (-{aksiya}%)"
        else:
            narx_text = format_price(narx)
        
        rows.append([
            p['id'],
            p['nomi'],
            p['kategoriya'],
            narx_text,
            p['miqdor']
        ])
    
    print_table(headers, rows)

def show_product_details(product_id):
    products = get_products()
    product = None
    
    for p in products:
        if p['id'] == product_id:
            product = p
            break
    
    if not product:
        print("Mahsulot topilmadi!")
        return
    
    print_header("MAHSULOT TAFSILOTLARI")
    
    aksiya = int(product['aksiya'])
    narx = int(product['narx'])
    
    print(f"\nID: {product['id']}")
    print(f"Nomi: {product['nomi']}")
    print(f"Kategoriya: {product['kategoriya']}")
    print(f"Dastlabki narx: {format_price(narx)}")
    
    if aksiya > 0:
        yangi_narx = narx * (100 - aksiya) / 100
        print(f"Aksiya: -{aksiya}%")
        print(f"Aksiya narxi: {format_price(yangi_narx)}")
        print(f"Tejaysiz: {format_price(narx - yangi_narx)}")
    else:
        print("Aksiya: Yo'q")
    
    print(f"Mavjud: {product['miqdor']} dona")

def add_to_cart(product_id, quantity):
    if not current_customer:
        print("Iltimos, avval tizimga kiring!")
        return False
    
    products = get_products()
    product = None
    
    for p in products:
        if p['id'] == product_id:
            product = p
            break
    
    if not product:
        print("Mahsulot topilmadi!")
        return False
    
    if int(product['miqdor']) < quantity:
        print(f"Kechirasiz, omborda faqat {product['miqdor']} dona bor!")
        return False
    
    aksiya = int(product['aksiya'])
    narx = int(product['narx'])
    
    if aksiya > 0:
        narx = narx * (100 - aksiya) / 100
    
    with open(CART_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            current_customer['id'],
            product['id'],
            product['nomi'],
            int(narx),
            quantity
        ])
    
    print(f"\n✓ '{product['nomi']}' savatga qo'shildi!")
    return True

def show_cart():
    if not current_customer:
        print("Iltimos, avval tizimga kiring!")
        return
    
    cart_items = []
    with open(CART_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['mijoz_id'] == current_customer['id']:
                cart_items.append(row)
    
    if not cart_items:
        print("\nSavat bo'sh!")
        return
    
    print_header("MENING SAVATIM")
    
    headers = ['Mahsulot', 'Narx', 'Soni', 'Jami']
    rows = []
    total = 0
    
    for item in cart_items:
        narx = int(item['narx'])
        soni = int(item['soni'])
        jami = narx * soni
        total += jami
        
        rows.append([
            item['mahsulot_nomi'],
            format_price(narx),
            soni,
            format_price(jami)
        ])
    
    print_table(headers, rows)
    
    print(f"\n{'='*60}")
    print(f"JAMI: {format_price(total)}")
    
    if current_customer:
        membership = current_customer.get('azolik', 'Bronze')
        chegirma = MEMBERSHIPS[membership]['chegirma']
        
        if chegirma > 0:
            chegirma_summa = total * chegirma / 100
            final_price = total - chegirma_summa
            
            print(f"A'zolik chegirmasi ({membership}): -{chegirma}% = -{format_price(chegirma_summa)}")
            print(f"TO'LOV SUMMASI: {format_price(final_price)}")
        else:
            print(f"TO'LOV SUMMASI: {format_price(total)}")
    
    print(f"{'='*60}")

def clear_cart():
    if not current_customer:
        return
    
    other_items = []
    with open(CART_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['mijoz_id'] != current_customer['id']:
                other_items.append(row)
    
    with open(CART_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['mijoz_id', 'mahsulot_id', 'mahsulot_nomi', 'narx', 'soni'])
        writer.writeheader()
        writer.writerows(other_items)

def checkout():
    if not current_customer:
        print("Iltimos, avval tizimga kiring!")
        return
    
    cart_items = []
    with open(CART_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['mijoz_id'] == current_customer['id']:
                cart_items.append(row)
    
    if not cart_items:
        print("\nSavat bo'sh! Buyurtma berib bo'lmaydi.")
        return
    
    print_header("BUYURTMA BERISH")
    
    total = sum(int(item['narx']) * int(item['soni']) for item in cart_items)
    
    membership = current_customer.get('azolik', 'Bronze')
    chegirma_foiz = MEMBERSHIPS[membership]['chegirma']
    chegirma_summa = total * chegirma_foiz / 100
    final_price = total - chegirma_summa
    
    print(f"\nJami summa: {format_price(total)}")
    print(f"A'zolik ({membership}): -{chegirma_foiz}% = -{format_price(chegirma_summa)}")
    print(f"TO'LOV: {format_price(final_price)}")
    
    print("\nYETKAZISH USULI:")
    print("1. Yetkazib berish")
    print("2. Do'kondan olib ketish")
    print("0. Bekor qilish")
    
    delivery_choice = input("\nTanlang: ")
    
    if delivery_choice == '0':
        print("Buyurtma bekor qilindi.")
        return
    
    delivery_type = "Yetkazib berish" if delivery_choice == '1' else "Do'kondan olib ketish"
    delivery_cost = 0
    
    if delivery_choice == '1':
        delivery_cost = MEMBERSHIPS[membership]['yetkazish']
        if delivery_cost > 0:
            print(f"\nYetkazib berish: {format_price(delivery_cost)}")
            final_price += delivery_cost
    
    manzil = current_customer.get('manzil', '')
    if delivery_choice == '1':
        print(f"\nJoriy manzil: {manzil}")
        yangi_manzil = input("Yangi manzil (bo'sh qoldiring joriy manzil uchun): ")
        if yangi_manzil:
            manzil = yangi_manzil
    
    print("\n" + "="*60)
    print(f"TO'LOV SUMMASI: {format_price(final_price)}")
    print(f"Yetkazish: {delivery_type}")
    if delivery_choice == '1':
        print(f"Manzil: {manzil}")
    print("="*60)
    
    tasdiqlash = input("\nBuyurtmani tasdiqlaysizmi? (ha/yo'q): ")
    
    if tasdiqlash.lower() not in ['ha', 'yes', 'y']:
        print("Buyurtma bekor qilindi.")
        return
    
    orders = []
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            orders = list(csv.DictReader(f))
    
    new_id = max([int(o['id']) for o in orders], default=0) + 1
    
    with open(ORDERS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for item in cart_items:
            writer.writerow([
                new_id,
                current_customer['id'],
                item['mahsulot_nomi'],
                item['soni'],
                item['narx'],
                int(item['narx']) * int(item['soni']),
                delivery_type,
                datetime.now().strftime('%d.%m.%Y %H:%M')
            ])
            new_id += 1
    
    ballar = int(final_price / 10000) * MEMBERSHIPS[membership]['ball']
    update_customer_balls(ballar)
    
    clear_cart()
    
    print("\n✓ BUYURTMA MUVAFFAQIYATLI QABUL QILINDI!")
    print(f"✓ {ballar} ball qo'shildi!")
    print("\nTez orada siz bilan bog'lanamiz. Rahmat!")

def update_customer_balls(new_balls):
    if not current_customer:
        return
    
    customers = []
    with open(CUSTOMERS_FILE, 'r', encoding='utf-8') as f:
        customers = list(csv.DictReader(f))
    
    for customer in customers:
        if customer['id'] == current_customer['id']:
            customer['ballar'] = str(int(customer['ballar']) + new_balls)
            current_customer['ballar'] = customer['ballar']
            break
    
    with open(CUSTOMERS_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'ism', 'telefon', 'manzil', 'azolik', 'ballar'])
        writer.writeheader()
        writer.writerows(customers)

def login():
    global current_customer
    
    print_header("TIZIMGA KIRISH")
    
    telefon = input("Telefon raqam (+998): ").strip()
    
    try:
        with open(CUSTOMERS_FILE, 'r', encoding='utf-8') as f:
            customers = list(csv.DictReader(f))
        
        for customer in customers:
            if customer.get('telefon', '').strip() == telefon:
                current_customer = customer
                print(f"\n✓ Xush kelibsiz, {customer['ism']}!")
                print(f"A'zolik: {customer['azolik']}")
                print(f"Ballar: {customer['ballar']}")
                pause()
                return
        
        print("\n✗ Mijoz topilmadi!")
        print("Ro'yxatdan o'tishni xohlaysizmi? (ha/yo'q): ", end='')
        
        if input().lower() in ['ha', 'yes', 'y']:
            register()
    
    except FileNotFoundError:
        print("\n✗ Fayllar topilmadi! Iltimos dasturni qayta ishga tushiring.")
        pause()
    except Exception as e:
        print(f"\n✗ Xatolik: {e}")
        pause()

def register():
    """TO'G'IRLANGAN REGISTER FUNKSIYASI"""
    global current_customer
    
    print_header("RO'YXATDAN O'TISH")
    
    ism = input("Ism: ").strip()
    telefon = input("Telefon (+998): ").strip()
    manzil = input("Manzil: ").strip()
    
    if not ism or not telefon:
        print("\n✗ Ism va telefon bo'sh bo'lishi mumkin emas!")
        pause()
        return
    
    print("\nA'ZOLIK TURINI TANLANG:")
    for key, value in MEMBERSHIPS.items():
        print(f"  {key}: Chegirma {value['chegirma']}%, Ball {value['ball']}x")
    
    azolik = input("\nA'zolik (Bronze/Silver/Gold/Biznes): ").strip()
    if azolik not in MEMBERSHIPS:
        print("\n✗ Noto'g'ri a'zolik turi! Bronze tanlanadi.")
        azolik = 'Bronze'
    
    try:
        customers = []
        with open(CUSTOMERS_FILE, 'r', encoding='utf-8') as f:
            customers = list(csv.DictReader(f))
        
        for customer in customers:
            if customer.get('telefon', '').strip() == telefon:
                print(f"\n✗ Bu telefon raqam allaqachon ro'yxatdan o'tgan!")
                pause()
                return
        
        new_id = max([int(c['id']) for c in customers], default=0) + 1
        
        with open(CUSTOMERS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([new_id, ism, telefon, manzil, azolik, 0])
        
        current_customer = {
            'id': str(new_id),
            'ism': ism,
            'telefon': telefon,
            'manzil': manzil,
            'azolik': azolik,
            'ballar': '0'
        }
        
        print(f"\n✓ Ro'yxatdan o'tdingiz! Xush kelibsiz, {ism}!")
        pause()
    
    except Exception as e:
        print(f"\n✗ Xatolik: {e}")
        pause()

def logout():
    global current_customer
    if current_customer:
        print(f"\n✓ {current_customer['ism']}, ko'rishguncha!")
        current_customer = None
    pause()

def show_profile():
    if not current_customer:
        print("Iltimos, avval tizimga kiring!")
        return
    
    print_header("MENING PROFILIM")
    
    print(f"\nIsm: {current_customer['ism']}")
    print(f"Telefon: {current_customer['telefon']}")
    print(f"Manzil: {current_customer['manzil']}")
    print(f"A'zolik: {current_customer['azolik']}")
    print(f"Ballar: {current_customer['ballar']}")
    
    membership = current_customer['azolik']
    print(f"\nIMTIYOZLAR:")
    print(f"  Chegirma: {MEMBERSHIPS[membership]['chegirma']}%")
    print(f"  Ballar: {MEMBERSHIPS[membership]['ball']}x")
    yetkazish = MEMBERSHIPS[membership]['yetkazish']
    print(f"  Yetkazish: {'Bepul' if yetkazish == 0 else format_price(yetkazish)}")

def show_orders():
    if not current_customer:
        print("Iltimos, avval tizimga kiring!")
        return
    
    orders = []
    with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['mijoz_id'] == current_customer['id']:
                orders.append(row)
    
    if not orders:
        print("\nHali buyurtma yo'q!")
        return
    
    print_header("MENING BUYURTMALARIM")
    
    headers = ['ID', 'Mahsulot', 'Soni', 'Summa', 'Yetkazish', 'Sana']
    rows = []
    
    for order in orders:
        rows.append([
            order['id'],
            order['mahsulot_nomi'],
            order['soni'],
            format_price(int(order['jami'])),
            order['yetkazish'],
            order['sana']
        ])
    
    print_table(headers, rows)

def show_support():
    print_header("QO'LLAB-QUVVATLASH")
    
    print("\nALOQA:")
    print("  Telefon: +998 71 123-45-67")
    print("  Email: info@sales.uz")
    print("  Telegram: @sales_uz")
    
    print("\nISH VAQTI:")
    print("  Dushanba-Shanba: 9:00 - 20:00")
    print("  Yakshanba: 10:00 - 18:00")
    
    print("\nMANZIL:")
    print("  Toshkent sh., Chilonzor tumani")
    print("  Bunyodkor ko'chasi, 12-uy")
    
    print("\nSavol-javob:")
    print("  - Yetkazib berish: 24-48 soat ichida")
    print("  - Garovlik: 12 oy")
    print("  - Qaytarish: 14 kun ichida")

def main_menu():
    while True:
        clear_screen()
        print_header("Sales")
        
        if current_customer:
            print(f"\n👤 {current_customer['ism']} ({current_customer['azolik']}) | Ballar: {current_customer['ballar']}")
        else:
            print("\n👤 Mehmon")
        
        print("\nMAHSULOTLAR:")
        print("1. Kategoriyalar bo'yicha")
        print("2. Mahsulot qidirish")
        print("3. Savatga qo'shish")
        
        print("\nBUYURTMA:")
        print("4. Savatchani ko'rish")
        print("5. Buyurtma berish")
        
        print("\nPROFIL:")
        if current_customer:
            print("6. Mening profilim")
            print("7. Buyurtmalarim")
            print("8. Chiqish")
        else:
            print("6. Kirish / Ro'yxatdan o'tish")
        
        print("\nBOSHQA:")
        print("9. Qo'llab-quvvatlash")
        print("0. Dasturdan chiqish")
        
        tanlov = input("\nTanlang: ")
        
        if tanlov == '1':
            while True:
                clear_screen()
                show_categories()
                cat_choice = input("\nKategoriya raqami: ")
                
                if cat_choice == '0':
                    break
                elif cat_choice in CATEGORIES:
                    clear_screen()
                    show_products_by_category(cat_choice)
                    
                    product_id = input("\nMahsulot ID (0=ortga): ")
                    if product_id != '0':
                        clear_screen()
                        show_product_details(product_id)
                        pause()
                else:
                    print("Noto'g'ri tanlov!")
                    pause()
        
        elif tanlov == '2':
            clear_screen()
            search_products()
            
            product_id = input("\nMahsulot ID (0=ortga): ")
            if product_id != '0':
                clear_screen()
                show_product_details(product_id)
                pause()
        
        elif tanlov == '3':
            clear_screen()
            print_header("SAVATGA QO'SHISH")
            
            product_id = input("Mahsulot ID: ")
            quantity = input("Miqdor: ")
            
            try:
                add_to_cart(product_id, int(quantity))
            except ValueError:
                print("Noto'g'ri miqdor!")
            
            pause()
        
        elif tanlov == '4':
            clear_screen()
            show_cart()
            pause()
        
        elif tanlov == '5':
            clear_screen()
            checkout()
            pause()
        
        elif tanlov == '6':
            if current_customer:
                clear_screen()
                show_profile()
                pause()
            else:
                clear_screen()
                login()
        
        elif tanlov == '7' and current_customer:
            clear_screen()
            show_orders()
            pause()
        
        elif tanlov == '8' and current_customer:
            logout()
        
        elif tanlov == '9':
            clear_screen()
            show_support()
            pause()
        
        elif tanlov == '0':
            print("\nDasturdan chiqildi. Xayr!")
            break
        
        else:
            print("Noto'g'ri tanlov!")
            pause()

if __name__ == "__main__":
    create_files()
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nDastur to'xtatildi!")
    except Exception as e:
        print(f"\nXatolik: {e}")
        import traceback
        traceback.print_exc()