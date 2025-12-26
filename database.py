import csv
from config import *

def create_files():
    # Products
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nomi', 'brend', 'ram', 'ssd', 'narx', 'miqdor', 'aksiya'])
            writer.writerow(['1', 'Dell Inspiron 15', 'Dell', '8GB', '256GB', '5500000', '10', '10'])
            writer.writerow(['2', 'HP Pavilion 14', 'HP', '16GB', '512GB', '7200000', '5', '0'])
            writer.writerow(['3', 'Lenovo IdeaPad 3', 'Lenovo', '8GB', '256GB', '4800000', '15', '15'])
            writer.writerow(['4', 'Asus VivoBook 15', 'Asus', '12GB', '512GB', '6500000', '8', '5'])
            writer.writerow(['5', 'MacBook Air M2', 'Apple', '8GB', '256GB', '15000000', '3', '0'])
    
    # Users
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'username', 'parol', 'ism', 'telefon'])
            writer.writerow(['1', 'admin', 'admin123', 'Administrator', '998901234567'])
    
    # Cart
    if not os.path.exists(CART_FILE):
        with open(CART_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['user_id', 'product_id', 'nomi', 'narx', 'soni'])
    
    # Orders
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'user_id', 'username', 'mahsulot', 'soni', 'narx', 'jami', 'sana'])

def read_csv(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except:
        return []

def write_csv(filename, data, fieldnames):
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except:
        return False

def append_csv(filename, row):
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        return True
    except:
        return False

