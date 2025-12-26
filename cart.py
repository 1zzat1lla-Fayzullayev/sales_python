from config import *
from database import *
from products import get_product_by_id

current_user = None

def add_to_cart(product_id, quantity):
    if not current_user:
        print("\nIltimos, avval tizimga kiring!")   
        return False
    
    product = get_product_by_id(product_id)
    
    if not product:
        print("\nMahsulot topilmadi!")
        return False
    
    if int(product['miqdor']) < quantity:
        print(f"\nOmborda faqat {product['miqdor']} dona bor!")
        return False
    
    aksiya = int(product['aksiya'])
    narx = int(product['narx'])
    
    if aksiya > 0:
        narx = narx * (100 - aksiya) / 100
    
    append_csv(CART_FILE, [
        current_user['id'],
        product['id'],
        product['nomi'],
        int(narx),
        quantity
    ])
    
    print(f"\n✓ '{product['nomi']}' savatga qo'shildi!")
    return True

def show_cart():
    if not current_user:
        print("\nIltimos, avval tizimga kiring!")
        return
    
    cart_items = read_csv(CART_FILE)
    my_items = [item for item in cart_items if item['user_id'] == current_user['id']]
    
    if not my_items:
        print("\nSavat bo'sh!")
        return
    
    print_header("MENING SAVATIM")
    
    headers = ['Mahsulot', 'Narx', 'Soni', 'Jami']
    rows = []
    total = 0
    
    for item in my_items:
        narx = int(item['narx'])
        soni = int(item['soni'])
        jami = narx * soni
        total += jami
        
        rows.append([
            item['nomi'],
            format_price(narx),
            soni,
            format_price(jami)
        ])
    
    print_table(headers, rows)
    
    print(f"\n{'='*60}")
    print(f"JAMI: {format_price(total)}")
    print(f"{'='*60}")

def clear_cart():
    if not current_user:
        return
    
    cart_items = read_csv(CART_FILE)
    other_items = [item for item in cart_items if item['user_id'] != current_user['id']]
    
    write_csv(CART_FILE, other_items, ['user_id', 'product_id', 'nomi', 'narx', 'soni'])

def checkout():
    if not current_user:
        print("\nIltimos, avval tizimga kiring!")
        return
    
    cart_items = read_csv(CART_FILE)
    my_items = [item for item in cart_items if item['user_id'] == current_user['id']]
    
    if not my_items:
        print("\nSavat bo'sh!")
        return
    
    print_header("BUYURTMA BERISH")
    
    total = sum(int(item['narx']) * int(item['soni']) for item in my_items)
    
    print(f"\nJami summa: {format_price(total)}")
    print(f"\nTasdiqlaysizmi? (ha/yo'q): ", end='')
    
    if input().lower() not in ['ha', 'yes', 'y']:
        print("Buyurtma bekor qilindi.")
        return
    
    orders = read_csv(ORDERS_FILE)
    new_id = max([int(o['id']) for o in orders], default=0) + 1
    
    for item in my_items:
        append_csv(ORDERS_FILE, [
            new_id,
            current_user['id'],
            current_user['username'],
            item['nomi'],
            item['soni'],
            item['narx'],
            int(item['narx']) * int(item['soni']),
            get_datetime()
        ])
        order_id = max([int(o['id']) for o in orders], default=0) + 1

    
    clear_cart()
    
    print("\n✓ BUYURTMA MUVAFFAQIYATLI!")
    print("Tez orada siz bilan bog'lanamiz.")

def show_my_orders():
    if not current_user:
        print("\nIltimos, avval tizimga kiring!")
        return
    
    orders = read_csv(ORDERS_FILE)
    my_orders = [o for o in orders if o['user_id'] == current_user['id']]
    
    if not my_orders:
        print("\nHali buyurtma yo'q!")
        return
    
    print_header("MENING BUYURTMALARIM")
    
    headers = ['ID', 'Mahsulot', 'Soni', 'Summa', 'Sana']
    rows = []
    
    for order in my_orders:
        rows.append([
            order['id'],
            order['mahsulot'],
            order['soni'],
            format_price(int(order['jami'])),
            order['sana']
        ])
    
    print_table(headers, rows)
