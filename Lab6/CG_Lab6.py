import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import numpy as np

class WatermarkApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Додаток для вбудовування водяного знаку")

        self.input_image = None
        self.watermark_image = None
        self.result_image = None

        self.create_widgets()

    def create_widgets(self):
        self.load_image_button = tk.Button(self.master, text="Завантажити зображення", command=self.load_image)
        self.load_image_button.grid(row=0, column=0, padx=10, pady=10)

        self.load_watermark_button = tk.Button(self.master, text="Завантажити водяний знак", command=self.load_watermark)
        self.load_watermark_button.grid(row=0, column=1, padx=10, pady=10)

        self.bit_plane_label = tk.Label(self.master, text="Площина біта (1-8):")
        self.bit_plane_label.grid(row=1, column=0, padx=10, pady=10)

        self.bit_plane = tk.IntVar(value=1)
        self.bit_plane_entry = tk.Entry(self.master, textvariable=self.bit_plane)
        self.bit_plane_entry.grid(row=1, column=1, padx=10, pady=10)

        self.embed_text_label = tk.Label(self.master, text="Текст для вбудовування:")
        self.embed_text_label.grid(row=2, column=0, padx=10, pady=10)

        self.embed_text_entry = tk.Entry(self.master)
        self.embed_text_entry.grid(row=2, column=1, padx=10, pady=10)

        self.embed_watermark_button = tk.Button(self.master, text="Вбудувати водяний знак", command=self.embed_watermark)
        self.embed_watermark_button.grid(row=3, column=0, padx=10, pady=10)

        self.embed_text_button = tk.Button(self.master, text="Вбудувати текст", command=self.embed_text)
        self.embed_text_button.grid(row=3, column=1, padx=10, pady=10)

        self.save_button = tk.Button(self.master, text="Зберегти результат", command=self.save_result)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.image_label_original = tk.Label(self.master)
        self.image_label_original.grid(row=5, column=0, padx=10, pady=10)

        self.image_label_result = tk.Label(self.master)
        self.image_label_result.grid(row=5, column=1, padx=10, pady=10)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_image = Image.open(file_path)
            self.display_image(self.input_image, self.image_label_original)

    def load_watermark(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.watermark_image = Image.open(file_path).convert('1')
            self.watermark_image = self.watermark_image.resize(self.input_image.size)

    def display_image(self, img, label):
        imgtk = ImageTk.PhotoImage(img)
        label.configure(image=imgtk)
        label.image = imgtk

    def embed_watermark(self):
        if self.input_image is None or self.watermark_image is None:
            messagebox.showerror("Помилка", "Завантажте як зображення, так і водяний знак.")
            return

        bit_plane = self.bit_plane.get()
        if not 1 <= bit_plane <= 8:
            messagebox.showerror("Помилка", "Площина біта повинна бути між 1 та 8.")
            return

        result = self.input_image.copy()
        input_pixels = np.array(result)
        watermark_pixels = np.array(self.watermark_image)

        for i in range(watermark_pixels.shape[0]):
            for j in range(watermark_pixels.shape[1]):
                input_pixels[i, j, 2] = (input_pixels[i, j, 2] & ~(1 << (bit_plane - 1))) | (watermark_pixels[i, j] << (bit_plane - 1))

        self.result_image = Image.fromarray(input_pixels)
        self.display_image(self.result_image, self.image_label_result)

    def embed_text(self):
        if self.input_image is None:
            messagebox.showerror("Помилка", "Спочатку завантажте зображення.")
            return

        text = self.embed_text_entry.get()
        if not text:
            messagebox.showerror("Помилка", "Введіть текст для вбудовування.")
            return

        bit_plane = self.bit_plane.get()
        if not 1 <= bit_plane <= 8:
            messagebox.showerror("Помилка", "Площина біта повинна бути між 1 та 8.")
            return

        result = self.input_image.copy()
        input_pixels = np.array(result)
        text_bits = ''.join(format(ord(char), '08b') for char in text)

        idx = 0
        for i in range(input_pixels.shape[0]):
            for j in range(input_pixels.shape[1]):
                if idx < len(text_bits):
                    input_pixels[i, j, 2] = (input_pixels[i, j, 2] & ~(1 << (bit_plane - 1))) | (int(text_bits[idx]) << (bit_plane - 1))
                    idx += 1

        self.result_image = Image.fromarray(input_pixels)
        self.display_image(self.result_image, self.image_label_result)

    def save_result(self):
        if self.result_image is None:
            messagebox.showerror("Помилка", "Немає результату для збереження.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png")
        if file_path:
            self.result_image.save(file_path)
            messagebox.showinfo("Успіх", "Зображення успішно збережено.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

