import cv2
import numpy as np
import easyocr
import pandas as pd

IMAGE_PATH = "image.png"
OUTPUT_FILE = "nama_clean.csv"

# ---- STEP 1: Load & preprocess ----
image = cv2.imread(IMAGE_PATH)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# ---- STEP 2: Detect outer table ----
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
dilated = cv2.dilate(thresh, kernel, iterations=2)

contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
table_box = max(contours, key=cv2.contourArea)
x,y,w,h = cv2.boundingRect(table_box)
table_img = image[y:y+h, x:x+w]

# ---- STEP 3: Detect vertical lines inside table ----
gray_table = cv2.cvtColor(table_img, cv2.COLOR_BGR2GRAY)
thresh_table = cv2.threshold(gray_table, 150, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

vert_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))
detect_vert = cv2.morphologyEx(thresh_table, cv2.MORPH_OPEN, vert_kernel, iterations=2)

contours, _ = cv2.findContours(detect_vert, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
col_x = sorted([cv2.boundingRect(c)[0] for c in contours if cv2.boundingRect(c)[3] > table_img.shape[0]*0.5])

# Nama column = between 2nd and 3rd vertical lines
nama_x_min = col_x[0] + 20   # add margin to avoid "No" column
nama_x_max = col_x[1] - 5

# ---- STEP 4: OCR only Nama column ----
nama_col_img = table_img[:, nama_x_min:nama_x_max]

reader = easyocr.Reader(['en','id'])
results = reader.readtext(nama_col_img)

# ---- STEP 5: Group by row ----
rows = {}
for (bbox, text, conf) in results:
    if conf < 0.4:   # skip low confidence
        continue
    y_min = min([p[1] for p in bbox])
    row_id = int(y_min // 40)  # group every ~40px as one row
    rows.setdefault(row_id, []).append(text)

# Join fragments per row
final_names = [" ".join(parts) for row_id, parts in sorted(rows.items())]

# ---- STEP 6: Save clean names ----
df = pd.DataFrame(final_names, columns=["Nama"])
df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print("âœ… Nama kolom berhasil diekstrak lebih bersih:", OUTPUT_FILE)
print(df)