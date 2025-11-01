# simulasi login sederhana dengaan gerbang logika sederhana
username = input("Masukkan username: ")
password = input("Masukkan password: ")

if username == "admin" and password == "password123":
    print("Login berhasil! Selamat datang.")
else:
    print("Login gagal! Username atau password salah.")