import csv
from datetime import datetime, timedelta
from tabulate import tabulate

def add(x,b,d,c):
    with open("../database/sales.csv", "a", newline="") as sotuvlar:
        a = csv.DictWriter(sotuvlar, fieldnames=['Nomi','Narxi','Soni','Sanasi'])
        a.writerow({'Nomi': x, 'Narxi': b, 'Soni': d, 'Sanasi': c})

def read():
    with open("../database/sales.csv") as sotuvlar:
        a = csv.DictReader(sotuvlar)
        print(tabulate(a, headers="keys", tablefmt="grid"))

def monthly_report(n):
    bir_oylik = datetime.now() - timedelta(days=30)

    products = {}

    with open("../database/sales.csv", encoding="utf-8") as sotuvlar:
        a = csv.DictReader(sotuvlar)

        for i in a:
            sanalar = datetime.strptime(i["Sanasi"], "%d.%m.%Y")
            if sanalar < bir_oylik:
                continue

            nomi = i["Nomi"]
            narxi = int(i["Narxi"])
            soni = int(i["Soni"])

            if nomi not in products:
                products[nomi] = {
                    "Nomi": nomi,
                    "Jami soni": 0,
                    "Jami summa": 0
                }

            products[nomi]["Jami soni"] += soni
            products[nomi]["Jami summa"] += narxi * soni

    hsobot = list(products.values())
    hsobot.sort(key=lambda x: x["Jami soni"], reverse=True)

    print(tabulate(hsobot[:n], headers="keys", tablefmt="grid"))

read()