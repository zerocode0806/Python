print("Pilih unit konversi")
print("C -> Celcius")
print("K -> Kelvin")
print("F -> Fahrenheit")

unit = str(input("Masukkan unit konversi C, K, F: "))

if unit == "C" or unit == "c" :
    temperatur = float(input("Msukkan suhu dalam Celcius(C): "))
    print(f"{temperatur} derajat celcius dalam kelvin adalah {temperatur + 273.15}K")
    print(f"{temperatur} derajat celcius dalam fahrenheit adalah {(temperatur * 1.8) + 32}F")
elif unit == "K" or unit == "k" :
    temperatur = float(input("Msukkan suhu dalam Kelvin(K): "))
    print(f"{temperatur} derajat kelvin dalam Celcius adalah {temperatur - 273.15}C")
    print(f"{temperatur} derajat kelvin dalam fahrenheit adalah {((temperatur - 273.15) * 1.8) + 32}F")
elif unit == "F" or unit == "f" :
    temperatur = float(input("Msukkan suhu dalam Fahrenheit(F): "))
    print(f"{temperatur} derajat fahrenheit dalam kelvin adalah {((temperatur - 32) / 1.8) + 273.15}K")
    print(f"{temperatur} derajat fahrenheit dalam celcius adalah {(temperatur - 32) / 1.8}C")
else : 
    print("Pilihan tidak valid")