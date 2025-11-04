x = float(input("Masukkan angka pertama : "))
y = float(input("Masukkan angka kedua : "))

operasi = input("Pilih operasi +, -, *, / : ")

match operasi :
    case "+":
        print(f"Hasil dari {x} + {y} = {x + y}")
    case "-" :
        print(f"Hasil dari {x} - {y} = {x - y}")
    case "*" :
        print(f"Hasil dari {x} x {y} = {x * y}")
    case "/" :
        print(f"Hasil dari {x} / {y} = {x / y}")
    case _ :
        print("Invalid input")