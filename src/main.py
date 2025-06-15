# -*- coding: utf-8 -*-

from ocr.ocr import extract_invoice_data
from export import exporter

image_path = r"C:\Users\Thevu\ocr-faktury-insert\sample\faktura-vat.jpg"
data = extract_invoice_data(image_path)

print("Wydobyte dane z faktury:")
for k, v in data.items():
    print(f"{k}: {v}")

exporter.save_to_csv(data)
exporter.save_to_json(data)

print("Dane zapisane")

