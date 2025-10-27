# Program Kuis Sederhana dengan Batasan Soal
skor = 0

print("Maksimal soal yang dapat dimainkan adalah 3")

# Input jumlah soal yang ingin dimainkan
try:
    jumlah_soal_target_input = int(input("Masukkan jumlah soal yang ingin dimainkan: "))
    if jumlah_soal_target_input > 3:
        jumlah_soal_target = 3
        print(f"Jumlah soal dibatasi menjadi {jumlah_soal_target}.")
    elif jumlah_soal_target_input < 1:
        jumlah_soal_target = 1
        print("Minimal 1 soal. Jumlah soal diatur ke 1.")
    else:
        jumlah_soal_target = jumlah_soal_target_input
except ValueError:
    print("Input tidak valid. Menggunakan target default 3 soal.")
    jumlah_soal_target = 3

# Loop untuk setiap soal
for i in range(1, jumlah_soal_target + 1):
    print(f"--- Soal ke-{i} ---")
    jawaban_benar = ""
    
    # Definisi soal dan jawaban
    if i == 1:
        print("Ibu kota negara Indonesia adalah (A/B/C):")
        print("A. Bandung  B. Jakarta  C. Surabaya")
        jawaban_benar = "B"
    elif i == 2:
        print("Berapakah hasil dari 2 + 3 * 4?")
        print("A. 20  B. 14  C. 16")
        jawaban_benar = "B"
    elif i == 3:
        print("Planet terdekat dengan Matahari adalah (A/B/C):")
        print("A. Mars  B. Venus  C. Merkurius")
        jawaban_benar = "C"
    else:
        print("Anda telah melewati jumlah soal yang ditentukan.")
        continue # Melompati sisa kode dalam loop dan lanjut ke iterasi berikutnya (jika ada)

    jawaban_user = input("Jawaban Anda: ")

    # Cek jawaban dan update skor
    if jawaban_user.upper() == jawaban_benar:
        skor += 10
        print(f"✅ Benar! Skor Anda sekarang: {skor}")
    else:
        print(f"❌ Salah. Jawaban yang benar adalah: {jawaban_benar}")
    
    print("") 

print("===== Kuis Selesai! =====")
print(f"Total skor akhir Anda: {skor}")