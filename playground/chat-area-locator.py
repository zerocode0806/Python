import cv2
import numpy as np
from PIL import ImageGrab
from pynput import mouse
import time

coords = []
click_count = 0

def on_click(x, y, button, pressed):
    global click_count
    if pressed:
        click_count += 1
        if click_count == 1:
            print("🕒 Klik pertama diabaikan (biasanya untuk fokus)...")
            return  # Do nothing
        coords.append((x, y))
        print(f"🖱️ Klik ke-{click_count - 1}: {x}, {y}")
        if len(coords) == 2:
            return False  # Stop listener

def capture_and_draw_area():
    print("⏳ Kamu punya 3 detik untuk fokus ke jendela yang ingin di-screenshot...")
    time.sleep(3)

    print("📸 Mengambil screenshot...")
    img = ImageGrab.grab()  # Screenshot layar aktif saat ini
    img_np = np.array(img)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    print("👆 Klik 2 titik: sudut kiri-atas dan kanan-bawah area target")
    print("💡 Klik pertama akan diabaikan (biasanya untuk fokus jendela)...")

    cv2.imshow("Tentukan Area - klik 2 kali", img_bgr)
    cv2.waitKey(1)  # Tampilkan gambar

    # Dengarkan klik
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    cv2.destroyAllWindows()

    if len(coords) == 2:
        (x1, y1), (x2, y2) = coords
        left = min(x1, x2)
        top = min(y1, y2)
        right = max(x1, x2)
        bottom = max(y1, y2)
        print(f"\n✅ Area berhasil ditentukan:")
        print(f"chat_box_area = ({left}, {top}, {right}, {bottom})")

capture_and_draw_area()
