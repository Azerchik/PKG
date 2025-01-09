import tkinter as tk
from tkinter import colorchooser, messagebox
import colorsys

class ColorConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Converter")

        self.rgb_vars = [tk.IntVar(value=255) for _ in range(3)]
        self.hsv_vars = [tk.DoubleVar(value=1.0) for _ in range(3)]
        self.cmyk_vars = [tk.DoubleVar(value=0.0) for _ in range(4)]

        self.create_widgets()
        self.update_all_from_rgb()

    def create_widgets(self):
        # RGB Controls
        rgb_frame = tk.LabelFrame(self.root, text="RGB", padx=10, pady=10)
        rgb_frame.grid(row=0, column=0, padx=10, pady=10)
        self.create_color_controls(rgb_frame, self.rgb_vars, ["R", "G", "B"], self.update_all_from_rgb)

        # HSV Controls
        hsv_frame = tk.LabelFrame(self.root, text="HSV", padx=10, pady=10)
        hsv_frame.grid(row=0, column=1, padx=10, pady=10)
        self.create_color_controls(hsv_frame, self.hsv_vars, ["H", "S", "V"], self.update_all_from_hsv, scale_max=[360, 1, 1])

        # CMYK Controls
        cmyk_frame = tk.LabelFrame(self.root, text="CMYK", padx=10, pady=10)
        cmyk_frame.grid(row=0, column=2, padx=10, pady=10)
        self.create_color_controls(cmyk_frame, self.cmyk_vars, ["C", "M", "Y", "K"], self.update_all_from_cmyk, scale_max=[1, 1, 1, 1])

        # Color Preview and Palette
        preview_frame = tk.Frame(self.root)
        preview_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.color_preview = tk.Label(preview_frame, text="Preview", bg="#FFFFFF", width=30, height=5)
        self.color_preview.pack()

        palette_button = tk.Button(preview_frame, text="Choose Color from Palette", command=self.choose_color)
        palette_button.pack(pady=5)

    def create_color_controls(self, parent, vars, labels, command, scale_max=None):
        if scale_max is None:
            scale_max = [255] * len(vars)

        for i, (var, label, max_value) in enumerate(zip(vars, labels, scale_max)):
            frame = tk.Frame(parent)
            frame.pack(fill="x", pady=2)

            lbl = tk.Label(frame, text=label, width=3)
            lbl.pack(side="left")

            entry = tk.Entry(frame, textvariable=var, width=5)
            entry.pack(side="left")

            scale = tk.Scale(frame, from_=0, to=max_value, variable=var, orient="horizontal", command=lambda x, v=var: command())
            scale.pack(side="left", fill="x", expand=True)

    def update_all_from_rgb(self):
        r, g, b = [var.get() for var in self.rgb_vars]

        # Update HSV
        h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        self.hsv_vars[0].set(h * 360)
        self.hsv_vars[1].set(s)
        self.hsv_vars[2].set(v)

        # Update CMYK
        c, m, y, k = self.rgb_to_cmyk(r, g, b)
        self.cmyk_vars[0].set(c)
        self.cmyk_vars[1].set(m)
        self.cmyk_vars[2].set(y)
        self.cmyk_vars[3].set(k)

        self.update_preview()

    def update_all_from_hsv(self):
        h, s, v = [var.get() for var in self.hsv_vars]

        # Update RGB
        r, g, b = colorsys.hsv_to_rgb(h / 360, s, v)
        self.rgb_vars[0].set(int(r * 255))
        self.rgb_vars[1].set(int(g * 255))
        self.rgb_vars[2].set(int(b * 255))

        # Update CMYK
        self.update_all_from_rgb()

    def update_all_from_cmyk(self):
        c, m, y, k = [var.get() for var in self.cmyk_vars]

        # Update RGB
        r, g, b = self.cmyk_to_rgb(c, m, y, k)
        self.rgb_vars[0].set(r)
        self.rgb_vars[1].set(g)
        self.rgb_vars[2].set(b)

        # Update HSV
        self.update_all_from_rgb()

    def rgb_to_cmyk(self, r, g, b):
        if r == 0 and g == 0 and b == 0:
            return 0, 0, 0, 1
        
        c = 1 - r / 255
        m = 1 - g / 255
        y = 1 - b / 255

        k = min(c, m, y)
        c = (c - k) / (1 - k)
        m = (m - k) / (1 - k)
        y = (y - k) / (1 - k)
        return round(c, 4), round(m, 4), round(y, 4), round(k, 4)

    def cmyk_to_rgb(self, c, m, y, k):
        r = 255 * (1 - c) * (1 - k)
        g = 255 * (1 - m) * (1 - k)
        b = 255 * (1 - y) * (1 - k)
        return int(r), int(g), int(b)

    def update_preview(self):
        r, g, b = [var.get() for var in self.rgb_vars]
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.color_preview.config(bg=hex_color)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[0]
        if color_code:
            r, g, b = map(int, color_code)
            self.rgb_vars[0].set(r)
            self.rgb_vars[1].set(g)
            self.rgb_vars[2].set(b)
            self.update_all_from_rgb()

if __name__ == "__main__":
    root = tk.Tk()
    app = ColorConverterApp(root)
    root.mainloop()
