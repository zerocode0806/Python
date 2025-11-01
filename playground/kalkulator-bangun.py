# pilih opsi perhitungan
print("1. keliling lingkaran")
print("2. luas lingkaran")
print("3. luas segitiga")
print("4. keliling segitiga")
print(" ")

operasi = input("Pilih opsi perhitungan 1, 2, 3, 4 : ")

# lakukan perhitungan berdasarkan opsi yang dipilih
if operasi == "1" :
    r = float(input("Masukkan jari jari lingkaran (r) : "))
    print(f"Keliling dari lingkran dengan jari jari {r} adalah {2 * 3.14 * r}")
elif operasi == "2" :
    r = float(input("Masukkan jari jari lingkaran (r) : "))
    print(f"Keliling dari lingkran dengan jari jari {r} adalah {3.14 * r * r}")
elif operasi == "3" :
    a = float(input("Masukkan alas (a) : "))
    t = float(input("Masukkan tinggi (t) : "))
    print(f"Luas dari segitiga dengan alas {a} dan tinggi {t} adalah {0.2 * a * t}")
elif operasi == "4" :
    x = float(input("Masukkan panjang sisi a : "))
    y = float(input("Masukkan panjang sisi b : "))
    z = float(input("Masukkan panjang sisi c : "))
    print(f"Keliling dari segitiga dengan panjang sisi a {x}, sisi b {y}, dan sisi c {z} adalah {x + y + z}")
else : 
    print("pilihan tidak valid, pilih antara 1, 2, 3, atau 4")