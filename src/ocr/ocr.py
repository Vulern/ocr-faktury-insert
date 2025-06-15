# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image
import cv2
from parsing import parser

# Ścieżka do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_invoice_data(image_path):
    """
    Wczytuje obraz faktury, wykonuje OCR i zwraca dane jako słownik.
    """
    # Wczytaj obraz
    img = cv2.imread(image_path)

    # Konwertuj do skali szarości
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Progowanie
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # OCR
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh, config=config, lang='pol')

    # Parsowanie danych
    data = {
        "NIP": parser.extract_nip(text),
        "Numer faktury": parser.extract_invoice_number(text),
        "Data": parser.extract_date(text),
        "Kwota brutto": parser.extract_total(text),
    }

    return data
