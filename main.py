from config import *
from database import *
from products import *
from cart import *
from auth import *
from admin import *
import cart


def main():
    create_files()

    while True:
        clear_screen()
        print_header("NOTEBOOK SHOP - NOUTBUK DO'KONI")

        if cart.current_user:
            print(f"\n👤 {cart.current_user['ism']} ({cart.current_user['username']})")
            if is_admin():
                print("🔑 Admin")
        else:
            print("\n👤 Mehmon")

        print("\n📦 MAHSULOTLAR:")
        print("1. Barcha noutbuklar")
        print("2. Brendlar bo'yicha")
        print("3. Qidirish")

        print("\n🛒 SAVAT:")
        print("4. Savatga qo'shish")
        print("5. Savatni ko'rish")
        print("6. Buyurtma berish")

        print("\n👤 PROFIL:")
        if cart.current_user:
            print("7. Buyurtmalarim")
            if is_admin():
                print("8. Admin panel")
            print("9. Chiqish")
        else:
            print("7. Kirish")
            print("8. Ro'yxatdan o'tish")

        print("\n0. Dasturdan chiqish")

        choice = input("\nTanlang: ")

        if choice == '1':
            clear_screen()
            show_all_products()
            pause()

        elif choice == '2':
            clear_screen()
            print_header("BRENDLAR")
            for i, brand in enumerate(BRANDS, 1):
                print(f"{i}. {brand}")

            try:
                brand = BRANDS[int(input("\nBrend raqami: ")) - 1]
                clear_screen()
                show_by_brand(brand)
            except:
                print("Noto'g'ri tanlov!")
            pause()

        elif choice == '3':
            clear_screen()
            search_product(input("Qidiruv: "))
            pause()

        elif choice == '4':
            clear_screen()
            add_to_cart(input("Mahsulot ID: "), int(input("Miqdor: ")))
            pause()

        elif choice == '5':
            clear_screen()
            show_cart()
            pause()

        elif choice == '6':
            clear_screen()
            checkout()
            pause()

        elif choice == '7':
            clear_screen()
            show_my_orders() if cart.current_user else login()
            pause()

        elif choice == '8':
            if cart.current_user and is_admin():
                admin_menu()
            elif not cart.current_user:
                clear_screen()
                register()
                pause()
            else:
                print("Faqat adminlar uchun!")
                pause()

        elif choice == '9' and cart.current_user:
            logout()
            pause()

        elif choice == '0':
            print("\nDasturdan chiqildi. Xayr!")
            break

        else:
            print("Noto'g'ri tanlov!")
            pause()


if __name__ == "__main__":
    print("CSV fayllar tekshirilmoqda...")
    fix_all_csv_files()
    main()
    