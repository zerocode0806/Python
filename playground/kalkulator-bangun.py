# pilih opsi perhitungan
print("a. keliling lingkaran")
print("b. luas lingkaran")
print("c. luas segitiga")
print("d. keliling segitiga")
print(" ")

operasi = input("Masukkan opsi perhitungan a, b, c, d : ")

# lakukan perhitungan berdasarkan opsi yang dipilih
if operasi == "a" :
    r = float(input("Masukkan jari jari lingkaran (r) : "))
    print(f"Keliling dari lingkran dengan jari jari {r} adalah {2 * 3.14 * r}")
elif operasi == "b" :
    r = float(input("Masukkan jari jari lingkaran (r) : "))
    print(f"Keliling dari lingkran dengan jari jari {r} adalah {3.14 * r * r}")
elif operasi == "c" :
    a = float(input("Masukkan alas (a) : "))
    t = float(input("Masukkan tinggi (t) : "))
    print(f"Luas dari segitiga dengan alas {a} dan tinggi {t} adalah {0.2 * a * t}")
elif operasi == "d" :
    x = float(input("Masukkan panjang sisi 1 : "))
    y = float(input("Masukkan panjang sisi 2 : "))
    z = float(input("Masukkan panjang sisi 3 : "))
    print(f"Keliling dari segitiga dengan panjang sisi a {x}, sisi b {y}, dan sisi c {z} adalah {x + y + z}")
else : 
    print("pilihan tidak valid, pilih a, b, c, atau d")