import re

def extract_nip(text):
    # Elastyczne dopasowanie: NIP, ewentualnie z literówkami, i 10 cyfr
    match = re.search(r'\bN[I1l][Pp]?[^\d]{0,5}(\d[\d\s]{9,})', text, re.IGNORECASE)
    if match:
        return match.group(1).replace(" ", "")
    
    # Awaryjnie: wyci¹gnij pierwszy ci¹g 10 cyfr
    possible_nips = re.findall(r'\b\d{10}\b', text)
    if possible_nips:
        return possible_nips[0]
    
    return "Nie znaleziono"


def extract_invoice_number(text):
    # Przyk³ad: Nr 2014/02/2 lub podobne
    match = re.search(r'Nr\s+(\d{4}/\d{2}/\d+)', text, re.IGNORECASE)
    return match.group(1) if match else "Nie znaleziono"

def extract_date(text):
    # Szuka daty w formacie RRRR-MM-DD
    match = re.search(r'(\d{4}-\d{2}-\d{2})', text)
    return match.group(1) if match else "Nie znaleziono"

def extract_total(text):
    # Szuka najwiêkszej kwoty z "PLN" — typowo kwota brutto
    amounts = re.findall(r'(\d{1,3}(?: \d{3})*,\d{2})\s*PLN', text)
    return amounts[-1] if amounts else "Nie znaleziono"
