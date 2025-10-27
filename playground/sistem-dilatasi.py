# Input pilihan titik pusat
pilihan = input("Gunakan titik pusat default (0,0)? (y/n): ")

if pilihan == 'y' or pilihan == 'Y':
    a = 0
    b = 0
else:
    a, b = map(float, input("Masukkan titik pusat dilatasi (a b): ").split())

# Input jumlah titik dan faktor skala
total_titik = int(input("Masukkan jumlah titik: "))
k = float(input("Masukkan faktor skala (k): "))

# Proses perulangan untuk setiap titik
for i in range(1, total_titik + 1):
    print(f"\nMasukkan koordinat titik ke-{i} (x y): ", end="")
    x, y = map(float, input().split())

    # Rumus dilatasi
    x_aksen = a + k * (x - a)
    y_aksen = b + k * (y - b)

    # Output hasil
    print(f"Hasil dilatasi titik ke-{i} dengan skala {k}:")
    print(f"Dari ({x}, {y}) menjadi ({x_aksen}, {y_aksen})")

print("\nProgram selesai. Semua titik telah dihitung.")
