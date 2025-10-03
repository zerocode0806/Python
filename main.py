# fungsi desimal ke biner
def decimal_to_binary(n):
    if n == 0:
        return "0"
    
    binary_digits = []
    
    while n > 0:
        remainder = n % 2       # ambil sisa bagi 2 menggunkan modulus
        binary_digits.append(str(remainder))
        n = n // 2              # lanjutkan bagi 2 menggunakan floor division
    
    # hasilnya terbalik, jadi kita balik list
    binary_digits.reverse()
    return "".join(binary_digits)

# fungsi desimal ke oktal
def decimal_to_octal(n):
    if n == 0:
        return "0"
    
    octal_digits = []
    
    while n > 0:
        remainder = n % 8        # ambil sisa bagi 8 menggunakan modulus
        octal_digits.append(str(remainder))
        n = n // 8               # lanjutkan bagi 8 menggunakan floor division
    
    # hasilnya terbalik, jadi kita balik list
    octal_digits.reverse()
    return "".join(octal_digits)

# fungsi desimal ke heksadesimal
def decimal_to_hex(n):
    if n == 0:
        return "0"
    
    hex_digits = "0123456789ABCDEF"
    result = []
    
    while n > 0:
        remainder = n % 16          # ambil sisa bagi 16 menggunakan modulus
        result.append(hex_digits[remainder])  # ambil dari string digit
        n = n // 16                 # lanjutkan bagi 16 menggunakan floor division
    
    result.reverse()
    return "".join(result)

# fungsi biner ke desimal
def binary_to_decimal(binary_str):
    decimal_value = 0           # penampung hasil akhir
    power = 0                   # posisi digit (mulai dari 0 untuk paling kanan)
    
    # baca digit biner dari kanan ke kiri
    for digit in binary_str[::-1]:
        if digit == "1":        # kalau digitnya 1
            decimal_value += 2 ** power   # tambahkan nilai 2^posisi
        power += 1              # geser ke posisi berikutnya
    
    return decimal_value

def to_decimal(number_str, base):
    """
    Mengubah bilangan dari basis tertentu ke desimal.
    
    number_str : str  -> bilangan dalam bentuk string
    base       : int  -> basis asal (2 untuk biner, 8 untuk oktal, 10 untuk desimal, 16 untuk hex)
    """
    return int(number_str, base)


# 🔹 Contoh penggunaan:
print(to_decimal("1010",16))  # biner -> 10
print(to_decimal("52", 8))     # oktal -> 42
print(to_decimal("2A", 16))    # hex   42
print(to_decimal("123", 10))   # desimal -> 123


# # biner ke desimal
# print(binary_to_decimal("1010"))  # 10
# # desimal ke heksadesimal
# print(decimal_to_hex(1945))
# # desimal ke oktal  
# print(decimal_to_octal(156))
# # desimal ke biner
# print(decimal_to_binary(7))