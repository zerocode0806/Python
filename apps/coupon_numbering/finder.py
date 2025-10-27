import cv2

# Inisialisasi variabel global
zoom_scale = 1.0
offset_x = 0
offset_y = 0

img_original = cv2.imread("kupon_template.png")
height, width = img_original.shape[:2]

def show_image():
    global zoom_scale, offset_x, offset_y
    resized = cv2.resize(img_original, None, fx=zoom_scale, fy=zoom_scale, interpolation=cv2.INTER_LINEAR)

    # Ukuran area tampilan
    view_h, view_w = 600, 800
    start_x = min(max(offset_x, 0), max(resized.shape[1] - view_w, 0))
    start_y = min(max(offset_y, 0), max(resized.shape[0] - view_h, 0))
    end_x = start_x + view_w
    end_y = start_y + view_h

    cropped = resized[start_y:end_y, start_x:end_x].copy()
    cv2.imshow("Gambar", cropped)

def mouse_callback(event, x, y, flags, param):
    global offset_x, offset_y, zoom_scale
    if event == cv2.EVENT_LBUTTONDOWN:
        # Hitung posisi asli pada gambar
        real_x = int((x + offset_x) / zoom_scale)
        real_y = int((y + offset_y) / zoom_scale)

        if 0 <= real_x < img_original.shape[1] and 0 <= real_y < img_original.shape[0]:
            b, g, r = img_original[real_y, real_x]
            hex_color = '#{:02X}{:02X}{:02X}'.format(r, g, b)
            print(f"Posisi: X = {real_x}, Y = {real_y}")
            print(f"RGB: ({r}, {g}, {b})")
            print(f"HEX: {hex_color}")
        else:
            print("Klik di luar area gambar")

cv2.namedWindow("Gambar")
cv2.setMouseCallback("Gambar", mouse_callback)

while True:
    show_image()
    key = cv2.waitKey(50)

    if key == 27:  # ESC
        break
    elif key == ord('+') or key == ord('='):
        zoom_scale = min(zoom_scale + 0.1, 5.0)
    elif key == ord('-') or key == ord('_'):
        zoom_scale = max(zoom_scale - 0.1, 0.2)
    elif key == 81:  # left
        offset_x -= 50
    elif key == 82:  # up
        offset_y -= 50
    elif key == 83:  # right
        offset_x += 50
    elif key == 84:  # down
        offset_y += 50

cv2.destroyAllWindows()
