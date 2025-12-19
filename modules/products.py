import database.db
import csv
from tabulate import tabulate

def list_products():
    with open("database/products.csv") as product:
        a = csv.DictReader(product)
        if not a:
            print("Mahsulotlar yo‘q")
            return
        print(tabulate(a, headers="keys", tablefmt="grid"))
