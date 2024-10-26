import tkinter as tk
import sys
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tkintermapview.map_widget import TkinterMapView


class TemperatureLabel:
    def __init__(self, map_widget: "TkinterMapView", map_width, map_height):
        self.map_widget = map_widget
        self.map_width = map_width
        self.map_height = map_height

        self.width = 200  # Lebar skala suhu
        self.height = 20  # Tinggi skala suhu
        self.border_width = 3

        self.canvas_rect = None
        self.canvas_text = None

        self.draw()

    def draw(self):
        # Buat canvas baru
        self.canvas = tk.Canvas(self.map_widget, width=self.width + 40, height=self.height + 30)
        self.canvas.place(x=self.map_width - self.width - 60, y=self.map_height - self.height - 50)

        # Gambar skala suhu
        self.draw_temperature_scale()

        # Tambahkan label teks di atas skala suhu
        self.canvas.create_text(self.width / 2 + 20, 10, text="Temperature, °C", font=("Arial", 10))

    def draw_temperature_scale(self):
        colors = ["#0000FF", "#800080", "#FFFFFF", "#FFFF00", "#FF4500"]  # Biru - Ungu - Putih - Kuning - Merah
        steps = len(colors) - 1
        for i in range(steps):
            start_color = self.canvas.winfo_rgb(colors[i])
            end_color = self.canvas.winfo_rgb(colors[i + 1])
            r_delta = (end_color[0] - start_color[0]) // 100
            g_delta = (end_color[1] - start_color[1]) // 100
            b_delta = (end_color[2] - start_color[2]) // 100
            for j in range(100):
                r = int(start_color[0] + (r_delta * j)) // 256
                g = int(start_color[1] + (g_delta * j)) // 256
                b = int(start_color[2] + (b_delta * j)) // 256
                color = f"#{r:02x}{g:02x}{b:02x}"
                x0 = 20 + (self.width // steps) * i + (self.width // steps) * j // 100
                x1 = 20 + (self.width // steps) * i + (self.width // steps) * (j + 1) // 100
                self.canvas.create_rectangle(x0, 20, x1, self.height + 2, fill=color, outline="")

        # Tambahkan label suhu di bawah skala
        self.canvas.create_text(20, self.height + 10, text="-40", font=("Arial", 8), anchor="w")
        self.canvas.create_text(self.width / 2 + 20, self.height + 10, text="0", font=("Arial", 8))
        self.canvas.create_text(self.width + 20, self.height + 10, text="40", font=("Arial", 8), anchor="e")
