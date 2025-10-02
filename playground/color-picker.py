import pyautogui
from pynput import mouse

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def on_click(x, y, button, pressed):
    if pressed:
        screenshot = pyautogui.screenshot()
        color = screenshot.getpixel((x, y))
        print(f"\n🖱️ Klik di ({x}, {y})")
        print(f"🎨 RGB: {color}")
        print(f"🔷 HEX: {rgb_to_hex(color)}")
        return False  # Hentikan listener setelah satu klik

print("🖱️ Klik di mana saja untuk ambil warna...")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
