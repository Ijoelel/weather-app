import customtkinter
import tkinter as tk
from tkintermapview import TkinterMapView
from tkintermapview.canvas_button import CanvasButton
import requests
from layer import *

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "WeatherMaps"
    WIDTH = 1366
    HEIGHT = 736

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.createcommand('tk::mac::Quit', self.on_closing)

        self.marker_list = []

        # ============ create two CTkFrames ============

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.frame.grid(row=0, column=1, rowspan=1, pady=0, padx=0, sticky="nsew")


        # ============ frame ============

        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=0)
        self.frame.grid_columnconfigure(0, weight=1)

        self.map_widget = TkinterMapView(self.frame, corner_radius=0)
        self.map_widget.grid(row=1, rowspan=1, column=0, columnspan=3, sticky="nsew", padx=(0, 0), pady=(0, 0))

        options = ["Cloud", "Precipitation", "Pressure", "Wind", "Temperature"]
        self.layer_selector = customtkinter.CTkOptionMenu(master=self.map_widget, values=options, command=self.change_layer)
        self.layer_selector.grid(row=0, column=0, padx=10, pady=10)

        # Entry input dan tombol search
        self.search_button = customtkinter.CTkButton(master=self.map_widget, width=90, height=30, text="Search", command=self.search_event)
        self.search_button.grid(row=0, column=0, padx=5, pady=5)
        self.search_button.place(x=App.WIDTH - self.search_button._current_width - 20, y=20)
        
        self.entry = customtkinter.CTkEntry(master=self.map_widget, width=400, height=30, placeholder_text="Type address")
        self.entry.grid(padx=(5, 10), pady=5)
        self.entry.place(x= App.WIDTH - self.entry._current_width - self.search_button._current_width - 30, y=20)
        self.entry.bind("<Return>", self.search_event)

        # Set default values
        self.map_widget.set_position(-7.2461420, 112.7367966)  # Surabaya
        self.map_widget.set_zoom(5)
        self.map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")
        self.map_widget.tile_server = "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"

        # Set default layer (e.g., CloudLayer)
        self.active_layer = CloudLayer(self.map_widget)
        
        # Bind mouse click on map to show weather details
        self.map_widget.canvas.bind("<Double-1>", self.on_map_double_click)

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        data = self.active_layer.get_data(lat, lon)
        if data:
            self.display_weather_data(data)

    def display_weather_data(self, data):
        # Show the data in a label or pop-up as desired
        print(data)  # Or replace with code to display in the app

    def change_layer(self, selection):
        layer_map = {
            "Cloud": CloudLayer,
            "Precipitation": PrecipitationLayer,
            "Pressure": PressureLayer,
            "Wind": WindLayer,
            "Temperature": TemperatureLayer,
        }
        self.active_layer = layer_map[selection](self.map_widget)


    def search_event(self, event=None):
        location_query = self.entry.get()
        if location_query:
            url = f"https://nominatim.openstreetmap.org/search?q={location_query}&format=jsonv2&addressdetails=1&limit=1"
            try:
                response = requests.get(url)
                data = response.json()

                if data:
                    # Ambil latitude dan longitude dari hasil
                    latitude = float(data[0]["lat"])
                    longitude = float(data[0]["lon"])

                    # Atur posisi pada peta
                    self.map_widget.set_position(latitude, longitude)

                    print(f"Location found: {data[0]['display_name']} at {latitude}, {longitude}")
                else:
                    print("Location not found.")
            except Exception as e:
                print(f"Error: {e}")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()
        pass

if __name__ == "__main__":
    app = App()
    app.start()


# Next : 
#           - Buat kelas layer sendiri untuk nantinya akan di turunkan menjadi 5 yaitu, CloudLayer, PrecipitationLyaer, SeaPressurelayer, WindLayer dan TemperatureLayer
#           - Tiap layer merupakan class turunan dari parent class Layer
#           - Fitur ketika map di klik atau di hover di salah satu koordinat akan menampilkan detail bergantung pada layer yang digunakan
#           - Gunakan API dari tomorrow.io