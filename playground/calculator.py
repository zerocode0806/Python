x = float(input("Masukkan angka pertama : "))
y = float(input("Masukkan angka kedua : "))

operasi = input("Pilih operasi +, -, *, / : ")

if operasi == "+" :
    print(f"Hasil dari {x} + {y} = {x + y}")
elif operasi == "-" :
    print(f"Hasil dari {x} - {y} = {x - y}")
elif operasi == "*" :
    print(f"Hasil dari {x} x {y} = {x * y}")
elif operasi == "/" :
    print(f"Hasil dari {x} / {y} = {x / y}")
else : 
    print("Invalid input")