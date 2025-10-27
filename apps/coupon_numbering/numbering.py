from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
import os
import math
import sys

# === Konfigurasi ===
template_path = "numbering/kupon_template.png"
output_pdf_path = "kupon_fix_posisi.pdf"
font_path = "C:/Windows/Fonts/arialbd.ttf"
font_size = 30
digit_length = 4  # Jumlah digit, contoh: 3 untuk 001, 002, ..., 999
start_number = 1
total_kupons = 80
text_fill_color = "#C48A37"

# Validasi batas maksimum
max_number = int("9" * digit_length)
end_number = start_number + total_kupons - 1

if start_number < 0 or end_number > max_number:
    print(f"❌ Error: Rentang nomor ({start_number} s.d. {end_number}) melebihi batas untuk {digit_length} digit (maks {max_number}).")
    sys.exit(1)

# === Koordinat nomor kupon ===
number_pairs = [
    ((198, 300),   (664, 295)),    # 1 (disesuaikan dari pola kolom kiri)
    ((1202, 300),  (1667, 295)),   # 2 (disesuaikan dari pola kolom kanan)
    ((198, 654),   (664, 649)),    # 3 (sudah sesuai dengan baris berikut)
    ((1202, 654),  (1667, 649)),   # 4
    ((198, 1008),  (664, 1003)),   # 5 
    ((1202, 1008), (1667, 1003)),  # 6
    ((198, 1362),  (664, 1357)),   # 7
    ((1202, 1362), (1667, 1357)),  # 8
]

kupons_per_page = len(number_pairs)
total_pages = math.ceil(total_kupons / kupons_per_page)
font = ImageFont.truetype(font_path, font_size)

with Image.open(template_path) as img:
    template_width, template_height = img.size

c = canvas.Canvas(output_pdf_path, pagesize=(template_width, template_height))
current_number = start_number

for page in range(total_pages):
    template_img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(template_img)

    for i in range(kupons_per_page):
        if current_number > end_number:
            break

        number_text = f"{current_number:0{digit_length}d}"
        panitia_pos, peserta_pos = number_pairs[i]

        for pos in [panitia_pos, peserta_pos]:
            bbox = font.getbbox(number_text)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            centered = (pos[0] - text_width // 2, pos[1] - text_height // 2)
            draw.text(centered, number_text, font=font, fill=text_fill_color)

        current_number += 1

    temp_img_path = f"temp_page_{page + 1}.png"
    template_img.save(temp_img_path)

    c.drawImage(temp_img_path, 0, 0, width=template_width, height=template_height)
    c.showPage()
    os.remove(temp_img_path)

c.save()
print(f"✅ Kupon PDF berhasil dibuat: {output_pdf_path}")
