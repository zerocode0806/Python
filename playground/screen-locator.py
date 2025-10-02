from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, Key

running = True

def on_click(x, y, button, pressed):
    if pressed and running:
        print(f"Mouse clicked at ({x}, {y})")

def on_press(key):
    global running
    if key == Key.esc:
        print("Escape key pressed. Exiting...")
        running = False
        return False  # Stop keyboard listener

# Start mouse listener in a separate thread
mouse_listener = MouseListener(on_click=on_click)
mouse_listener.start()

# Start keyboard listener (main thread)
with KeyboardListener(on_press=on_press) as keyboard_listener:
    keyboard_listener.join()

mouse_listener.stop()
tes spamtes s