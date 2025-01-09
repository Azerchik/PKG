import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processing Application")
        self.master.geometry("800x600")  # Установим фиксированный размер окна

        self.image_label = Label(master)
        self.image_label.pack()

        self.load_button = Button(master, text="Load Image", command=self.load_image)
        self.load_button.pack()

        self.smooth_button = Button(master, text="Apply Low-pass Filter", command=self.apply_low_pass_filter)
        self.smooth_button.pack()

        self.global_threshold_button = Button(master, text="Global Thresholding", command=self.global_threshold)
        self.global_threshold_button.pack()

        self.adaptive_threshold_button = Button(master, text="Adaptive Thresholding", command=self.adaptive_threshold)
        self.adaptive_threshold_button.pack()

        self.image = None
        self.processed_image = None  # Для хранения обработанного изображения

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is not None:
                print("Image loaded successfully.")
                self.processed_image = self.image.copy()  # Сохраняем оригинал для обработки
                self.show_image(self.image)
            else:
                print("Failed to load image.")
                messagebox.showerror("Error", "Failed to load image.")
    
    def show_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)

        # Масштабируем изображение для отображения в окне
        img_pil.thumbnail((800, 600), Image.LANCZOS)  # Устанавливаем максимальный размер
        img_tk = ImageTk.PhotoImage(img_pil)
        
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def apply_low_pass_filter(self):
        if self.image is not None:
            kernel = np.ones((5, 5), np.float32) / 25  # Simple averaging filter
            self.processed_image = cv2.filter2D(self.image, -1, kernel)
            print("Low-pass filter applied.")
            self.show_image(self.processed_image)
        else:
            print("No image loaded for low-pass filter.")
            messagebox.showwarning("Warning", "Please load an image first.")

    def global_threshold(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            _, self.processed_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)  # Simple global threshold
            print("Global thresholding applied.")
            self.show_image(self.processed_image)
        else:
            print("No image loaded for global thresholding.")
            messagebox.showwarning("Warning", "Please load an image first.")

    def adaptive_threshold(self):
        if self.image is not None:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.processed_image = cv2.adaptiveThreshold(gray_image, 255, 
                                                         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                         cv2.THRESH_BINARY, 11, 2)
            print("Adaptive thresholding applied.")
            self.show_image(self.processed_image)
        else:
            print("No image loaded for adaptive thresholding.")
            messagebox.showwarning("Warning", "Please load an image first.")

if __name__ == "__main__":
    root = Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
