from config import *
from database import *

def get_all_products():
    return read_csv(PRODUCTS_FILE)

def show_all_products():
    products = get_all_products()
    
    if not products:
        print("\nMahsulotlar yo'q!")
        return
    
    print_header("BARCHA NOUTBUKLAR")
    
    headers = ['ID', 'Nomi', 'Brend', 'RAM', 'SSD', 'Narx', 'Miqdor', 'Aksiya']
    rows = []
    
    for p in products:
        aksiya = int(p['aksiya'])
        narx = int(p['narx'])
        
        if aksiya > 0:
            yangi_narx = narx * (100 - aksiya) / 100
            narx_str = f"{format_price(yangi_narx)} (-{aksiya}%)"
        else:
            narx_str = format_price(narx)
        
        rows.append([
            p['id'],
            p['nomi'],
            p['brend'],
            p['ram'],
            p['ssd'],
            narx_str,
            p['miqdor'],
            f"{aksiya}%" if aksiya > 0 else "-"
        ])
    
    print_table(headers, rows)

def show_by_brand(brend):
    products = get_all_products()
    filtered = [p for p in products if p['brend'] == brend]
    
    if not filtered:
        print(f"\n{brend} noutbuklari yo'q!")
        return
    
    print_header(f"{brend} NOUTBUKLARI")
    
    headers = ['ID', 'Nomi', 'RAM', 'SSD', 'Narx', 'Miqdor']
    rows = []
    
    for p in filtered:
        aksiya = int(p['aksiya'])
        narx = int(p['narx'])
        
        if aksiya > 0:
            yangi_narx = narx * (100 - aksiya) / 100
            narx_str = f"{format_price(yangi_narx)} (-{aksiya}%)"
        else:
            narx_str = format_price(narx)
        
        rows.append([
            p['id'],
            p['nomi'],
            p['ram'],
            p['ssd'],
            narx_str,
            p['miqdor']
        ])
    
    print_table(headers, rows)

def search_product(query):
    products = get_all_products()
    query = query.lower()
    
    results = [p for p in products if 
               query in p['nomi'].lower() or 
               query in p['brend'].lower()]
    
    if not results:
        print("\nHech narsa topilmadi!")
        return
    
    print_header(f"QIDIRUV: '{query}'")
    
    headers = ['ID', 'Nomi', 'Brend', 'RAM', 'Narx']
    rows = []
    
    for p in results:
        aksiya = int(p['aksiya'])
        narx = int(p['narx'])
        
        if aksiya > 0:
            yangi_narx = narx * (100 - aksiya) / 100
            narx_str = f"{format_price(yangi_narx)}"
        else:
            narx_str = format_price(narx)
        
        rows.append([p['id'], p['nomi'], p['brend'], p['ram'], narx_str])
    
    print_table(headers, rows)

def get_product_by_id(product_id):
    products = get_all_products()
    
    for p in products:
        if p['id'] == product_id:
            return p
    return None
