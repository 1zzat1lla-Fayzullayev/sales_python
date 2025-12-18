# ------------------adminla bilimi-------------

#  ||  Adminlar   ||    || Aloqalar ||    ||    Faollar    ||
#  | Izzatilla     |    | 255        |    | Izzatilla       |    
#  | Samandar      |    | 123        |    | Samandar        |    
#  | Doston        |    | 365        |    | Doston          |    
#  | Feruzbek      |    | 166        |    | Feruzbek        |    
#  | Shuxratjon    |    | 65         |    | Shuxratjon      |    
#  | Diyorbek      |    | 163        |    | Diyorbek        |    

import pandas as malumot
kirim = []
adminlar = ["Izzatilla", "Samandar", "Dostonbek", "Feruzbek", "Shuxratjon", "Diyorbek"]
aloqalar = [315, 64, 985, 54, 894, 516]

kiritish = float(input("kiriting: "))
kiritish = kirim

data = {
    "Adminlar": adminlar,
    "Aloqalar": aloqalar
}
jami_kirim = sum(kirim)
jamoa = malumot.DataFrame(data, index=range(1, len(adminlar) + 1))
print(jamoa)