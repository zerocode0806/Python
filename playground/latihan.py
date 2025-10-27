# 1. Penjumlahan dua bilangan
bilangan_pertama = 3
bilangan_kedua = 4
hasil_jumlah = bilangan_pertama + bilangan_kedua
print("Hasil penjumlahan:", hasil_jumlah)

# 2. Cek bilangan ganjil atau genap
a = 5
if a % 2 == 0:
    print(a, "adalah bilangan genap")
else:
    print(a, "adalah bilangan ganjil")

# 3. Menampilkan angka 1 sampai 10 secara berurutan
print("Angka 1 sampai 10:")
for i in range(1, 11):
    print(i, end=" ")
print()  # newline

# 4. Menghitung total belanja dengan diskon
belanja = 120000
if belanja > 100000:
    diskon = belanja * 0.10 # 10% diskon
else:
    diskon = 0

total_bayar = belanja - diskon
print("Total belanja:", belanja)
print("Diskon:", diskon)
print("Total yang harus dibayar:", total_bayar)
