def convert(number_str, from_base, to_base):
    """
    Mengubah bilangan dari suatu basis ke basis lain (2, 8, 10, 16).
    """
    decimal_value = int(number_str, from_base)  # ubah dulu ke desimal
    
    if to_base == 10:
        return str(decimal_value)
    if to_base == 2:
        return format(decimal_value, "b")
    if to_base == 8:
        return format(decimal_value, "o")
    if to_base == 16:
        return format(decimal_value, "X")
    raise ValueError("Basis hanya mendukung 2, 8, 10, atau 16.")


def show_all_bases(number_str, from_base):
    """
    Menampilkan bilangan dalam semua basis (2, 8, 10, 16)
    """
    # ubah ke desimal dulu
    decimal_value = int(number_str, from_base)

    print(f"Input ({from_base}) : {number_str}")
    print("Desimal      :", decimal_value)
    print("Biner        :", format(decimal_value, "b"))
    print("Oktal        :", format(decimal_value, "o"))
    print("Hex          :", format(decimal_value, "X"))
    print("-" * 30)


# 🔹 Contoh penggunaan:
show_all_bases("200", 10)    # input desimal 10
# show_all_bases("0011", 2)   # input biner 1010
# show_all_bases("12", 8)     # input oktal 12
# show_all_bases("A", 16)     # input hex A
