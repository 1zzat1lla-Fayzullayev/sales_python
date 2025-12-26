from config import *
from database import *
from auth import is_admin

def admin_menu():
    if not is_admin():
        print("\n✗ Bu bo'lim faqat adminlar uchun!")
        return
    
    while True:
        clear_screen()
        print_header("ADMIN PANEL")
        
        print("\n1. Mahsulot qo'shish")
        print("2. Mahsulot o'chirish")
        print("3. Barcha buyurtmalar")
        print("4. Statistika")
        print("0. Ortga")
        
        choice = input("\nTanlang: ")
        
        if choice == '1':
            add_product()
        elif choice == '2':
            delete_product()
        elif choice == '3':
            all_orders()
        elif choice == '4':
            statistics()
        elif choice == '0':
            break
        else:
            print("Noto'g'ri tanlov!")
            pause()

def add_product():
    clear_screen()
    print_header("YANGI MAHSULOT")
    
    nomi = input("Nomi: ")
    brend = input("Brend: ")
    ram = input("RAM (8GB): ")
    ssd = input("SSD (256GB): ")
    narx = input("Narx: ")
    miqdor = input("Miqdor: ")
    aksiya = input("Aksiya (%): ")
    
    products = read_csv(PRODUCTS_FILE)
    new_id = max([int(p['id']) for p in products], default=0) + 1
    
    append_csv(PRODUCTS_FILE, [new_id, nomi, brend, ram, ssd, narx, miqdor, aksiya])
    
    print(f"\n✓ '{nomi}' qo'shildi!")
    pause()

def delete_product():
    from products import show_all_products
    
    clear_screen()
    show_all_products()
    
    product_id = input("\nO'chirish uchun ID: ")
    
    products = read_csv(PRODUCTS_FILE)
    products = [p for p in products if p['id'] != product_id]
    
    write_csv(PRODUCTS_FILE, products, ['id', 'nomi', 'brend', 'ram', 'ssd', 'narx', 'miqdor', 'aksiya'])
    
    print("\n✓ O'chirildi!")
    pause()

def all_orders():
    clear_screen()
    print_header("BARCHA BUYURTMALAR")
    
    orders = read_csv(ORDERS_FILE)
    
    if not orders:
        print("\nHali buyurtma yo'q!")
        pause()
        return
    
    headers = ['ID', 'User', 'Mahsulot', 'Soni', 'Summa', 'Sana']
    rows = []
    
    for order in orders:
        rows.append([
            order['id'],
            order['username'],
            order['mahsulot'],
            order['soni'],
            format_price(int(order['jami'])),
            order['sana']
        ])
    
    print_table(headers, rows)
    pause()

def statistics():
    clear_screen()
    print_header("STATISTIKA")
    
    products = read_csv(PRODUCTS_FILE)
    users = read_csv(USERS_FILE)
    orders = read_csv(ORDERS_FILE)
    
    total_products = len(products)
    total_users = len(users)
    total_orders = len(orders)
    
    total_revenue = sum(int(o['jami']) for o in orders)
    
    print(f"\nJami mahsulotlar: {total_products} ta")
    print(f"Jami foydalanuvchilar: {total_users} ta")
    print(f"Jami buyurtmalar: {total_orders} ta")
    print(f"Jami daromad: {format_price(total_revenue)}")
    
    pause()
