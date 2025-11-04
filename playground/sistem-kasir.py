# Inisialisasi total
total = 0

# Input jumlah barang
jumlah_barang = int(input("Masukkan jumlah barang: "))

# Loop untuk input data barang
for i in range(1, jumlah_barang + 1):
    nama_barang = input(f"Masukkan nama barang ke-{i}: ")
    harga_barang = float(input(f"Masukkan harga barang {nama_barang}: "))
    total += harga_barang

# Hitung diskon berdasarkan jumlah barang
if total > 1000000:
    diskon = 0.20
elif total > 500000:
    diskon = 0.10
elif total > 100000:
    diskon = 0.05
else:
    diskon = 0

# Hitung total bayar
bayar = total - (total * diskon)

# Tampilkan hasil
print("\n===== HASIL PERHITUNGAN KASIR =====")
print(f"Total harga semua barang : Rp{total:,.2f}")
print(f"Diskon : {diskon * 100}%")
print(f"Total yang harus dibayar : Rp{bayar:,.2f}")
