# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from ocr.ocr import extract_invoice_data
from export import exporter


class InvoiceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("OCR Faktury - Insert GT")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Przycisk do wyboru pliku
        self.select_btn = ttk.Button(self, text="Wybierz fakturę", command=self.select_file)
        self.select_btn.pack(pady=10)

        # Pole tekstowe do wyświetlania wyniku
        self.text_box = tk.Text(self, height=15, width=70)
        self.text_box.pack(padx=10, pady=10)

        # Przycisk do zapisania danych
        self.save_btn = ttk.Button(self, text="Zapisz do CSV/JSON", command=self.save_data)
        self.save_btn.pack(pady=10)
        self.save_btn["state"] = tk.DISABLED

    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Wybierz plik faktury",
            filetypes=[("Pliki graficzne", "*.jpg *.jpeg *.png *.tiff")]
        )
        if file_path:
            try:
                self.data = extract_invoice_data(file_path)
                self.text_box.delete(1.0, tk.END)
                for k, v in self.data.items():
                    self.text_box.insert(tk.END, f"{k}: {v}\n")
                self.save_btn["state"] = tk.NORMAL
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił problem: {str(e)}")

    def save_data(self):
        try:
            exporter.save_to_csv(self.data)
            exporter.save_to_json(self.data)
            messagebox.showinfo("Zapisano", "Dane zapisane do output/faktura.csv i faktura.json")
        except Exception as e:
            messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać danych:\n{str(e)}")


if __name__ == "__main__":
    app = InvoiceApp()
    app.mainloop()
