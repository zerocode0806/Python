import pyautogui
import pytesseract
import numpy as np
from PIL import ImageGrab
import time

# Path ke Tesseract (ubah jika perlu)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Atur area teks yang ingin dibaca (x1, y1, x2, y2)
text_area = (927, 817, 1624, 1154)  # Ubah sesuai kotak teks di layar

# Waktu jeda antar baca (dalam detik)
interval = 0.5  # Baca layar setiap 0.5 detik

# Untuk menghindari mengetik ulang teks yang sama
last_text = ""

print("🚀 Bot berjalan... Fokus ke area typing game dalam 3 detik...")
time.sleep(3)

try:
    while True:
        # Ambil screenshot dari area
        screenshot = ImageGrab.grab(bbox=text_area)
        img_np = np.array(screenshot)

        # OCR: Ekstrak teks
        extracted_text = pytesseract.image_to_string(img_np).strip()

        # Jika teks baru terdeteksi, ketikkan
        if extracted_text and extracted_text != last_text:
            print(f"📋 Detected: {extracted_text}")
            pyautogui.write(extracted_text + " ", interval=0.01)
            last_text = extracted_text
        else:
            print("⏳ Tidak ada teks baru...")

        time.sleep(interval)

except KeyboardInterrupt:
    print("\n❌ Bot dihentikan.")
