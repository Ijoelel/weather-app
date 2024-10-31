from typing import TYPE_CHECKING
import customtkinter
from PIL import Image
import requests

if TYPE_CHECKING:
    from tkintermapview.map_widget import TkinterMapView
    
class Layer():
    def __init__(self, map_widget: "TkinterMapView"):
        self.map_widget = map_widget
        self.map_widget.canvas.bind("<Double-1>", self.on_map_double_click)

        self.frame = customtkinter.CTkFrame(master=self.map_widget, fg_color="white")
        self.frame.columnconfigure(0, weight=1, minsize=100)
        self.frame.columnconfigure(1, weight=1)

    def set_overlay(self, overlay_url_template):
        self.map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")
        self.map_widget.set_overlay_tile_server(overlay_url_template)

    def on_map_double_click(self, event):
        pass

    def get_data(self, layer, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)

    def close_frame(self):
        self.frame.place_forget()

    def clear_all_inside_frame(self):
        # Iterate through every widget inside the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

class CloudLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def on_map_double_click(self, event):
        self.clear_all_inside_frame()

        # Close Button
        cloud_icon = customtkinter.CTkImage(light_image=Image.open("x.png"),
                                  size=(16, 16))

        self.frame_close_button = customtkinter.CTkButton(master=self.frame, width=20, height=20, text="", image=cloud_icon, fg_color="transparent", hover=False, command=self.close_frame)
        self.frame_close_button.grid(row=0, column=2, padx=5, pady=(4, 0))
        
        # Main Label "Details"
        self.frame_label = customtkinter.CTkLabel(master=self.frame, text="Details", text_color='black')
        self.frame_label.grid(row=0, columnspan=2)

        # Get latitude and longitude from map
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        weather_url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat}, {lon}&apikey=AqwaRL5CVxt61JpyfxrCHeZAto4W6zlH"
        data_url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey=0d010075997245ca8559e806edf4a67c"
        headers = {"accept": "application/json"}

        # Call API
        cloud_response = (requests.get(weather_url, headers=headers)).json()["data"]["values"]
        data_response = (requests.get(data_url, headers=headers)).json()['features'][0]['properties']

        # print(cloud_response)
        print(data_response.get('country', 'hehe'))

        if data_response.get('country'):
            country_label = customtkinter.CTkLabel(master=self.frame, text="country", text_color="#888", anchor='e', justify='right',width=100, padx=8)
            country_label.grid(row=1, column=0)
            state_label = customtkinter.CTkLabel(master=self.frame, text="state", text_color="#888", anchor='e', justify='right',width=100, padx=8)
            state_label.grid(row=2, column=0)

            country_data = customtkinter.CTkLabel(master=self.frame, text=data_response["country"] if data_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
            country_data.grid(row=1, column=1)
            state_label = customtkinter.CTkLabel(master=self.frame, text=data_response['state'] if data_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
            state_label.grid(row=2, column=1)
        elif data_response.get('ocean'):
            ocean_name_label = customtkinter.CTkLabel(master=self.frame, text="name", text_color="#888", anchor='e', justify='right',width=100, padx=8)
            ocean_name_label.grid(row=1, column=0)
            ocean_label = customtkinter.CTkLabel(master=self.frame, text="ocean", text_color="#888", anchor='e', justify='right',width=100, padx=8)
            ocean_label.grid(row=2, column=0)

            country_data = customtkinter.CTkLabel(master=self.frame, text=data_response["name"] if data_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
            country_data.grid(row=1, column=1)
            state_label = customtkinter.CTkLabel(master=self.frame, text=data_response['ocean'] if data_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
            state_label.grid(row=2, column=1)
        elif data_response.get('marinearea'):
            marinearea_name_label = customtkinter.CTkLabel(master=self.frame, text="name", text_color="#888", anchor='e', justify='right',width=100, padx=8)
            marinearea_name_label.grid(row=1, column=0)
            marinearea_label = customtkinter.CTkLabel(master=self.frame, text="sea", text_color="#888", anchor='e', justify='right',width=100, padx=8)
            marinearea_label.grid(row=2, column=0)

            country_data = customtkinter.CTkLabel(master=self.frame, text=data_response["name"] if data_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
            country_data.grid(row=1, column=1)
            state_label = customtkinter.CTkLabel(master=self.frame, text=data_response['marinearea'] if data_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
            state_label.grid(row=2, column=1)
        
        cloud_cover_label = customtkinter.CTkLabel(master=self.frame, text="cloud_cover", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        cloud_cover_label.grid(row=3, column=0)
        cloud_base_label = customtkinter.CTkLabel(master=self.frame, text="cloud_base", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        cloud_base_label.grid(row=4, column=0)
        cloud_ceiling_label = customtkinter.CTkLabel(master=self.frame, text="cloud_ceiling", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        cloud_ceiling_label.grid(row=5, column=0)

        cloud_cover_label = customtkinter.CTkLabel(master=self.frame, text=f"{cloud_response['cloudCover']}%" if cloud_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
        cloud_cover_label.grid(row=3, column=1)
        cloud_base_label = customtkinter.CTkLabel(master=self.frame, text=f"{cloud_response['cloudBase']} km", text_color="black", anchor='w', justify='left',width=120, padx=8)
        cloud_base_label.grid(row=4, column=1)
        cloud_ceiling_label = customtkinter.CTkLabel(master=self.frame, text=f"{cloud_response['cloudCeiling']} km" if cloud_response['cloudCeiling'] != None else "null", text_color="black", anchor='w', justify='left',width=120, padx=8)
        cloud_ceiling_label.grid(row=5, column=1)

        if self.map_widget.winfo_width() - event.x < self.frame._current_width and self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y - self.frame._current_height)
        elif self.map_widget.winfo_width() - event.x < self.frame._current_width:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y)
        elif self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x, y=event.y - self.frame._current_height)
        else:
            self.frame.place(x=event.x, y=event.y)

class PrecipitationLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)

class PressureLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)

class WindLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)

class TemperatureLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)