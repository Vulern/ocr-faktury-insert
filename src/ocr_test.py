# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image
import cv2
import numpy as np

# Œcie¿ka do pliku wykonywalnego Tesseract (zmieñ jeœli masz inn¹!)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Œcie¿ka do faktury (upewnij siê, ¿e plik tam jest)
image_path = r"C:\Users\Thevu\ocr-faktury-insert\sample\faktura-vat.jpg"

# Wczytaj obraz
img = cv2.imread(image_path)

# Konwertuj na szaro
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Popraw kontrast progowaniem
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# OCR
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(thresh, config=custom_config, lang='pol')

# Wyœwietl wynik
print("=== ROZPOZNANY TEKST Z FAKTURY ===")
print(text)
