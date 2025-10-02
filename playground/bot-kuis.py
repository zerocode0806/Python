import pytesseract
import pyautogui
import openai
import time
import cv2
import numpy as np
from PIL import ImageGrab
import pytesseract
from openai import OpenAI

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# 1. Konfigurasi OpenAI


# 2. Screenshot area soal + opsi
question_area = (100, 300, 800, 600)  # ← Ubah sesuai layar

def read_screen_text():
    img = ImageGrab.grab(bbox=question_area)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    raw_text = pytesseract.image_to_string(img_cv)
    return raw_text

# 3. Kirim ke ChatGPT untuk menjawab


client = OpenAI(api_key="")  # ← Ganti dengan API key kamu

def ask_ai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're an expert quiz solver."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


# 4. Klik jawaban berdasarkan hasil AI
def click_answer(matching_text):
    for i in range(4):  # asumsi 4 opsi
        pyautogui.moveTo(300, 400 + i*60)  # ubah sesuai posisi
        screenshot = ImageGrab.grab(bbox=(250, 380 + i*60, 900, 420 + i*60))
        img_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        text = pytesseract.image_to_string(img_cv).lower()

        if matching_text.lower().strip() in text:
            pyautogui.click()
            print(f"✅ Clicked answer: {text.strip()}")
            return
    print("❌ Could not find matching answer.")

# 5. Main loop
print("Bot running in 5 seconds...")
time.sleep(5)

question_text = read_screen_text()
print("📋 OCR Result:\n", question_text)

ai_answer = ask_ai(question_text)
print("🧠 AI Answer:\n", ai_answer)

click_answer(ai_answer)
