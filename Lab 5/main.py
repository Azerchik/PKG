import tkinter as tk
from tkinter import ttk
import time

class RasterGraphicsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raster Graphics with Sutherland-Cohen and Polygon Clipping")
        self.grid_step = 40
        self.grid_range = 15
        self.create_interface()

        self.canvas_size = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=12, padx=10, pady=10)
        self.clip_window = (-100, -100, 100, 100)  # xmin, ymin, xmax, ymax
        self.segments = []

        self.draw_grid()

    def create_interface(self):
        ttk.Label(self.root, text="Choose Algorithm:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.algorithm = tk.StringVar(value="sutherland_cohen")
        ttk.Combobox(
            self.root,
            textvariable=self.algorithm,
            values=["sutherland_cohen", "polygon_clipping"],
            state="readonly"
        ).grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Load Segments", command=self.load_segments_from_file).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.root, text="Zoom Grid:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.grid_scale = tk.Scale(self.root, from_=15, to_=80, orient="horizontal", command=self.update_grid_step)
        self.grid_scale.set(self.grid_step)
        self.grid_scale.grid(row=2, column=1, padx=5, pady=5)

        self.time_label = ttk.Label(self.root, text="Elapsed Time: ---")
        self.time_label.grid(row=2, column=2, columnspan=12, padx=10, pady=5)

    def update_grid_step(self, value):
        self.grid_step = int(value)
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        step = self.grid_step
        grid_range = self.grid_range
        canvas_mid = self.canvas_size // 2

        for i in range(-grid_range, grid_range + 1):
            coord = canvas_mid + i * step
            self.canvas.create_line(coord, 0, coord, self.canvas_size, fill="#ddd")
            self.canvas.create_line(0, coord, self.canvas_size, coord, fill="#ddd")

            if i != 0:
                self.canvas.create_text(coord, canvas_mid + 15, text=str(i), fill="black")
                self.canvas.create_text(canvas_mid - 15, coord, text=str(-i), fill="black")

        self.canvas.create_line(canvas_mid, 0, canvas_mid, self.canvas_size, width=2, arrow=tk.LAST)
        self.canvas.create_line(0, canvas_mid, self.canvas_size, canvas_mid, width=2, arrow=tk.LAST)

    def to_canvas_coordinates(self, x, y):
        step = self.grid_step
        canvas_mid = self.canvas_size // 2
        canvas_x = canvas_mid + x * step
        canvas_y = canvas_mid - y * step
        return canvas_x, canvas_y

    def draw_pixel(self, x, y, color="black"):
        canvas_x, canvas_y = self.to_canvas_coordinates(x, y)
        self.canvas.create_rectangle(canvas_x - 2, canvas_y - 2, canvas_x + 2, canvas_y + 2, fill=color, outline=color)

    def draw_segment(self, x1, y1, x2, y2, color="green"):
        self.canvas.create_line(*self.to_canvas_coordinates(x1, y1),
                               *self.to_canvas_coordinates(x2, y2), fill=color, width=2)

    def sutherland_cohen(self, x1, y1, x2, y2, clip_window):
        xmin, ymin, xmax, ymax = clip_window

        def compute_outcode(x, y):
            code = 0
            if x < xmin: code |= 1  # LEFT
            if x > xmax: code |= 2  # RIGHT
            if y < ymin: code |= 4  # BOTTOM
            if y > ymax: code |= 8  # TOP
            return code

        code1 = compute_outcode(x1, y1)
        code2 = compute_outcode(x2, y2)

        while True:
            if not (code1 | code2):
                return x1, y1, x2, y2

            elif code1 & code2:
                return None

            else:
                edge = code1 if code1 else code2

                if edge == 1:
                    x = xmin
                    y = y1 + (xmin - x1) * (y2 - y1) / (x2 - x1)


                elif edge == 2:
                    x = xmax
                    y = y1 + (xmax - x1) * (y2 - y1) / (x2 - x1)

                elif edge == 4:
                    y = ymin
                    x = x1 + (ymin - y1) * (x2 - x1) / (y2 - y1)

                elif edge == 8:
                    y = ymax
                    x = x1 + (ymax - y1) * (x2 - x1) / (y2 - y1)

                if code1:
                    x1, y1 = x, y
                    code1 = compute_outcode(x1, y1)

                else:
                    x2, y2 = x, y
                    code2 = compute_outcode(x2, y2)

    def load_segments_from_file(self):
        with open('segments.txt') as f:
            lines = f.read().splitlines()

        num_segments = int(lines[0])
        self.segments = []

        for i in range(1, num_segments + 1):
            x1, y1, x2, y2 = map(int, lines[i].split())
            self.segments.append((x1, y1, x2, y2))

        self.clip_window = tuple(map(int, lines[num_segments + 1].split()))

        self.run_algorithm()

    def run_algorithm(self):
        self.draw_grid()

        start_time = time.time()

        if self.algorithm.get() == "sutherland_cohen":
            for x1, y1, x2, y2 in self.segments:
                result = self.sutherland_cohen(x1, y1, x2, y2, self.clip_window)
                if result:
                    nx1, ny1, nx2, ny2 = result
                    self.draw_segment(nx1, ny1, nx2, ny2)

        elapsed_time = time.time() - start_time
        self.time_label.config(text=f"Elapsed Time: {elapsed_time:.6f} seconds")


if __name__ == "__main__":
    root = tk.Tk()
    app = RasterGraphicsApp(root)
    root.mainloop()
