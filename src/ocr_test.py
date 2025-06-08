# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image
import cv2
import numpy as np
import re

from parsing import parser

# Œcie¿ka do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Œcie¿ka do obrazu faktury
image_path = r"C:\Users\Thevu\ocr-faktury-insert\sample\faktura-vat.jpg"

# 1. Wczytaj obraz
img = cv2.imread(image_path)

# 2. Konwertuj do odcieni szaroœci
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Zastosuj progowanie (czarno-bia³y kontrast)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# 4. OCR
custom_config = r'--oem 3 --psm 6'
text = pytesseract.image_to_string(thresh, config=custom_config, lang='pol')

# 5. Wyœwietl tekst (debug)
print("=== ROZPOZNANY TEKST Z FAKTURY ===\n")
print(text)

# 6. Parsowanie danych
print("\n=== Wydobyte dane z faktury ===")
print("NIP:", parser.extract_nip(text))
print("Numer faktury:", parser.extract_invoice_number(text))
print("Data:", parser.extract_date(text))
print("Kwota brutto:", parser.extract_total(text))
