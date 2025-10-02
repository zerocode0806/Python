import pyautogui
import pytesseract
import cv2
import time
import numpy as np
import re
from PIL import ImageGrab
import google.generativeai as genai

# === Konfigurasi Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# === Konfigurasi Gemini (stream)
API_KEY = "AIzaSyBLD3eDvxpMWlI0Rql4g5Ax-JV0U_HyMyM"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")  # gunakan model yang mendukung streaming

# === Fungsi bersihkan teks timestamp dan akhiran py
def clean_text(text):
    # Hapus timestamp
    text = re.sub(r'\b\d{1,2}[:.]\d{2}\s?(am|pm)?\b', '', text)
    text = re.sub(r'\b\d{3,4}\s?(am|pm)?\b', '', text)
    text = re.sub(r'\b\d{1,2}(am|pm)\b', '', text)
    text = re.sub(r'[—-]{1,2}\s?py$', '', text.strip())
    
    # Hapus karakter aneh
    text = re.sub(r'[^a-z0-9\s.,!?\'\"]+', '', text)  # hanya huruf, angka, spasi, tanda baca umum
    
    return text.strip()

# === Fungsi: hapus chat hijau (pesan kita sendiri)
def remove_green_text(img_bgr):
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    lower_green = np.array([40, 50, 50])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
    result = img_bgr.copy()
    result[mask != 0] = (0, 0, 0)
    return result

# === Area layar WhatsApp
chat_box_area = (664, 958, 1872, 1037)

print("🤖 Bot Streaming aktif. Tekan Ctrl+C untuk berhenti.")
last_text = ""

# === Loop utama
while True:
    screenshot = ImageGrab.grab(bbox=chat_box_area)
    img_rgb = np.array(screenshot)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    filtered_img = remove_green_text(img_bgr)

    extracted_text = pytesseract.image_to_string(filtered_img).lower().strip()
    cleaned_text = clean_text(extracted_text)

    if cleaned_text and cleaned_text != last_text:
        print("📩 Pertanyaan:", cleaned_text)
        last_text = cleaned_text

        try:
            print("🔮 Streaming jawaban dari Gemini...")

            response = model.generate_content(
                cleaned_text,
                stream=True  # Streaming token per token
            )

            for chunk in response:
                if chunk.text:
                    print(chunk.text, end="", flush=True)
                    pyautogui.write(chunk.text, interval=0.01)  # ketik real-time

            pyautogui.press("enter")
            print("\n✅ Pesan terkirim!\n")

        except Exception as e:
            print("❌ Error saat menjawab:", e)

    else:
        print("⏩ Tidak ada teks baru...")

    time.sleep(4)
