import hashlib

users = {}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_input(prompt):
    while True:
        value = input(prompt)
        if not value:
            print("Bo'sh qoldirmang!")
        elif " " in value:
            print("Bo'sh joy ishlatish mumkin emas! \n")
        else:
            return value

while True:
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    tanlash = input("Tanlang : ")


    if tanlash == "1":
        username = get_input("Usernameni kiriting : ")

        if username in users:
            print("Bu username mavjud!")
            continue

        password = get_input("Parolni kiriting : ")
        hashed_password = hash_password(password)

        users[username] = hashed_password
        print("Ro'yxatdan muvaffaqiyatli o'tdingiz \n")


    elif tanlash == "2":
        username = get_input("Usernameni kiriting : ")
        password = get_input("Parolni kiriting : ")

        hashed_password = hash_password(password)

        if username in users and users[username] == hashed_password:
            print("Login muvaffaqiyatli \n")
        else:
            print("Username yoki parol xato")


    elif tanlash == "3":
        print("Dasturdan chiqildi")
        break

    else:
        print("Xato \n")