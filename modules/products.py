import database.db
from database.db import read_data

def list_products():
    products = read_data("database/products.csv")
    if not products:
        print("Mahsulotlar yo‘q")
        return

    for p in products:
        print(f"{p['id']} | {p['name']} | {p['price']} | {p['quantity']}")
