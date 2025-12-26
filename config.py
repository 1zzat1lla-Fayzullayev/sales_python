import os
from datetime import datetime

# Papkalarni yaratish
if not os.path.exists('database'):
    os.makedirs('database')

# Fayllar
PRODUCTS_FILE = 'database/products.csv'
USERS_FILE = 'database/users.csv'
CART_FILE = 'database/cart.csv'
ORDERS_FILE = 'database/orders.csv'

# Adminlar
ADMIN_USERS = ['admin', 'boss', 'manager']

# Brendlar
BRANDS = ['Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Apple']

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nDavom etish uchun Enter bosing...")

def format_price(price):
    return f"{int(price):,} so'm".replace(',', ' ')

def get_date():
    return datetime.now().strftime('%d.%m.%Y')

def get_datetime():
    return datetime.now().strftime('%d.%m.%Y %H:%M')

def print_header(title):
    print("\n" + "="*60)
    print(title.center(60))
    print("="*60)

def print_table(headers, rows):
    if not rows:
        print("Ma'lumot yo'q")
        return
    
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))
    
    border = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(border)
    print("|" + "|".join(f" {h:<{widths[i]}} " for i, h in enumerate(headers)) + "|")
    print(border)
    
    for row in rows:
        print("|" + "|".join(f" {str(cell):<{widths[i]}} " for i, cell in enumerate(row)) + "|")
    print(border)