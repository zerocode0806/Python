# input angka 1 dan angka 2 (x dan y)
x = int(input("Masukkan angka pertama: "))
y = int(input("Masukkan angka kedua: "))

# input operasi yang diinginkan (+ , - , * , /)
operasi = input("Pilih operasi (+, -, *, /): ")

# fungsi untuk setiap operasi
def tambah(x, y):
    return x + y
def kurang(x, y):
    return x - y
def kali(x, y):
    return x * y    
def bagi(x, y):
    return x / y

# melakukan operasi sesuai input user
if operasi == '+':
    print(f"{x} + {y} = {tambah(x, y)}")  
elif operasi == '-':
    print(f"{x} - {y} = {kurang(x, y)}")
elif operasi == '*':
    print(f"{x} x {y} = {kali(x, y)}")
elif operasi == '/':
    print(f"{x} / {y} = {bagi(x, y)}")
else:
    print("Operasi tidak valid")