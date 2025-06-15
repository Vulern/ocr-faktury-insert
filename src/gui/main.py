# gui/main.py

from ttkbootstrap import Style
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

from ocr.ocr import extract_invoice_data
from export import exporter


class OCRApp(ttk.Window):
    def __init__(self):
        super().__init__(title="OCR Faktury", themename="darkly")  # <--- tu wybierasz motyw

        self.geometry("800x600")
        self.image_label = None
        self.file_path = None

        # Przycisk wyboru faktury
        self.select_btn = ttk.Button(self, text="📄 Wybierz fakturę", command=self.select_file, bootstyle="primary")
        self.select_btn.pack(pady=10)

        # Etykiety i pola edycji danych
        self.fields = {}
        for label in ["NIP", "Numer faktury", "Data", "Kwota brutto"]:
            frame = ttk.Frame(self)
            frame.pack(fill="x", padx=10, pady=5)
            ttk.Label(frame, text=label + ":", width=20).pack(side="left")
            entry = ttk.Entry(frame)
            entry.pack(fill="x", expand=True, side="left")
            self.fields[label] = entry

        # Podgląd faktury (obrazek)
        self.image_label = ttk.Label(self)
        self.image_label.pack(pady=10)

        # Przycisk zapisu
        self.save_btn = ttk.Button(self, text="💾 Zapisz dane", command=self.save_data, bootstyle="success")
        self.save_btn.pack(pady=10)

    def select_file(self):
        filetypes = [("Pliki graficzne", "*.png *.jpg *.jpeg"), ("Wszystkie pliki", "*.*")]
        self.file_path = filedialog.askopenfilename(title="Wybierz fakturę", filetypes=filetypes)
        if self.file_path:
            try:
                data = extract_invoice_data(self.file_path)
                for k, v in self.fields.items():
                    v.delete(0, "end")
                    v.insert(0, data.get(k, ""))
                self.show_image(self.file_path)
            except Exception as e:
                messagebox.showerror("Błąd OCR", str(e))

    def show_image(self, path):
        image = Image.open(path)
        max_size = (600, 300)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def save_data(self):
        data = {k: v.get() for k, v in self.fields.items()}
        try:
            exporter.save_to_csv(data)
            exporter.save_to_json(data)
            messagebox.showinfo("Sukces", "Dane zapisane pomyślnie!")
        except Exception as e:
            messagebox.showerror("Błąd zapisu", str(e))


if __name__ == "__main__":
    app = OCRApp()
    app.mainloop()
