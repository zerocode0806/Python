# Program Seleksi Pelamar Kerja
print("=== Seleksi Administrasi Pelamar Kerja ===")

ulang = 'y'
total_ditolak = 0
total_diterima = 0

'''
Syarat diterima adalah 
Usia antara 21 sampai 27
Pendidikan minimal S1
'''

while ulang.lower() == 'y':
    umur = int(input("Masukkan umur pelamar: "))
    pendidikan = str(input("Msukkan pendidikan terakhir anda (SMA/D3/S1/S2): "))

    if umur < 21 :
        print("Ditolak, masih terlalu muda") 
        total_ditolak += 1
    elif umur > 27 :
        print("Ditolak, terlalu tua ")
        total_ditolak += 1
    
    else :
        if pendidikan == "S1" or pendidikan == "S2" :
            print("Diterima, sudah memenuhi syarat")
            total_diterima += 1
        else :
            print("Ditolak, tidak memenuhi syarat")
            total_ditolak += 1
    
    ulang = input("Input data lagi? (y/t): ")
    
print("Program selesai. Terima kasih.")
print(f"Jumlah pelamar diterima {total_diterima} orang")
print(f"Jumlah pelamar ditolak {total_ditolak} orang")