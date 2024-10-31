import customtkinter
from tkintermapview import TkinterMapView
from tkintermapview.canvas_button import CanvasButton
import requests
from layer import *

customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):

    APP_NAME = "WeatherMaps"
    WIDTH = 1000
    HEIGHT = 550

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(App.APP_NAME)
        self.geometry(str(App.WIDTH) + "x" + str(App.HEIGHT))
        self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)
        self.bind("<Configure>", self.resize)
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

        # Entry input dan tombol search
        self.search_button = customtkinter.CTkButton(master=self.map_widget, width=90, height=30, text="Search", command=self.search_event)
        self.search_button.grid(row=0, column=0, padx=5, pady=5)
        self.search_button.place(x=self.winfo_width() - self.search_button._current_width - 20, y=20)
        
        self.entry = customtkinter.CTkEntry(master=self.map_widget, width=400, height=30, placeholder_text="Type address")
        self.entry.grid(padx=(5, 10), pady=5)
        self.entry.place(x= App.WIDTH - self.entry._current_width - self.search_button._current_width - 30, y=20)
        self.entry.bind("<Return>", self.search_event)

        # Layer Selector
        options = ["Cloud", "Precipitation", "Pressure", "Wind", "Temperature"]
        self.layer_selector = customtkinter.CTkOptionMenu(master=self.map_widget, values=options, command=self.change_layer)
        self.layer_selector.grid(row=0, column=0, padx=10, pady=10)
        self.layer_selector.place(x=App.WIDTH - self.entry._current_width - self.layer_selector._current_width - self.search_button._current_width - 50, y=20)

        # Set default values
        self.map_widget.set_position(-7.2461420, 112.7367966)  # Surabaya
        self.map_widget.set_zoom(5)
        self.map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")
        self.map_widget.tile_server = "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"

        # Set default layer (e.g., CloudLayer)
        self.active_layer = CloudLayer(self.map_widget)

    def resize(self, event):
        self.search_button.place(x=self.winfo_width() - self.search_button._current_width - 20, y=20)
        self.entry.place(x= self.winfo_width() - self.entry._current_width - self.search_button._current_width - 30, y=20)
        self.layer_selector.place(x=self.winfo_width() - self.entry._current_width - self.layer_selector._current_width - self.search_button._current_width - 50, y=20)

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
            url = f"https://api-v2.distancematrix.ai/maps/api/geocode/json?address={location_query}&key=89rzA8N4hHGOm25oStS6aRKDLKuOEex9wekgHZyBgkbXKzKP5FMisNVj8bu5MiTs"
            print(url)
            response = requests.get(url)
            print(response.json()['result'][0]['geometry']['location'])
            data = response.json()['result'][0]['geometry']['location']

            if data:
                # Ambil latitude dan longitude dari hasil
                latitude = float(data["lat"])
                longitude = float(data["lng"])

                # Atur posisi pada peta
                self.map_widget.set_position(latitude, longitude)
                self.map_widget.set_zoom(17)

                print(f"Location found: at {latitude}, {longitude}")
            else:
                print("Location not found.")

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