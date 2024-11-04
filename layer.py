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

    def fill_frame(self , event):
        self.clear_all_inside_frame()

        cloud_icon = customtkinter.CTkImage(light_image=Image.open("x.png"),
                                  size=(16, 16))

        self.frame_close_button = customtkinter.CTkButton(master=self.frame, width=20, height=20, text="", image=cloud_icon, fg_color="transparent", hover=False, command=self.close_frame)
        self.frame_close_button.grid(row=0, column=2, padx=5, pady=(4, 0))
        
        self.frame_label = customtkinter.CTkLabel(master=self.frame, text="Details", text_color='black')
        self.frame_label.grid(row=0, columnspan=2)

        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        data_url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lon}&apiKey=0d010075997245ca8559e806edf4a67c"
        headers = {"accept": "application/json"}

        data_response = (requests.get(data_url, headers=headers)).json()['features'][0]['properties']

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

    def get_data(self, layer, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)

    def close_frame(self):
        self.frame.place_forget()

    def clear_all_inside_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

class CloudLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def on_map_double_click(self, event):
        self.fill_frame(event)

        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        weather_url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat}, {lon}&apikey=AqwaRL5CVxt61JpyfxrCHeZAto4W6zlH"
        headers = {"accept": "application/json"}
        
        weather_response = (requests.get(weather_url, headers=headers)).json()["data"]["values"]
        
        cloud_cover_label = customtkinter.CTkLabel(master=self.frame, text="cloud_cover", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        cloud_cover_label.grid(row=3, column=0)
        cloud_base_label = customtkinter.CTkLabel(master=self.frame, text="cloud_base", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        cloud_base_label.grid(row=4, column=0)
        cloud_ceiling_label = customtkinter.CTkLabel(master=self.frame, text="cloud_ceiling", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        cloud_ceiling_label.grid(row=5, column=0)

        cloud_cover_label = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['cloudCover']}%" if weather_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
        cloud_cover_label.grid(row=3, column=1)
        cloud_base_label = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['cloudBase']} km", text_color="black", anchor='w', justify='left',width=120, padx=8)
        cloud_base_label.grid(row=4, column=1)
        cloud_ceiling_label = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['cloudCeiling']} km" if weather_response['cloudCeiling'] != None else "null", text_color="black", anchor='w', justify='left',width=120, padx=8)
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
        self.fill_frame(event)
        
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        weather_url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat}, {lon}&apikey=AqwaRL5CVxt61JpyfxrCHeZAto4W6zlH"
        headers = {"accept": "application/json"}

        weather_response = (requests.get(weather_url, headers=headers)).json()["data"]["values"]
        
        precipitation_label = customtkinter.CTkLabel(master=self.frame, text="precipitation", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        precipitation_label.grid(row=3, column=0)
        rain_label = customtkinter.CTkLabel(master=self.frame, text="rain-intensity", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        rain_label.grid(row=4, column=0)
        humidity_label = customtkinter.CTkLabel(master=self.frame, text="humidity_level", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        humidity_label.grid(row=5, column=0)

        precipitation_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['precipitationProbability']}%" if weather_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
        precipitation_data.grid(row=3, column=1)
        rain_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['rainIntensity']}mm/hr", text_color="black", anchor='w', justify='left',width=120, padx=8)
        rain_data.grid(row=4, column=1)
        humidity_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['humidity']}%" if weather_response['humidity'] != None else "null", text_color="black", anchor='w', justify='left',width=120, padx=8)
        humidity_data.grid(row=5, column=1)

        if self.map_widget.winfo_width() - event.x < self.frame._current_width and self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y - self.frame._current_height)
        elif self.map_widget.winfo_width() - event.x < self.frame._current_width:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y)
        elif self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x, y=event.y - self.frame._current_height)
        else:
            self.frame.place(x=event.x, y=event.y)

class PressureLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def on_map_double_click(self, event):
        self.fill_frame(event)

        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        weather_url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat}, {lon}&apikey=AqwaRL5CVxt61JpyfxrCHeZAto4W6zlH"
        headers = {"accept": "application/json"}

        weather_response = (requests.get(weather_url, headers=headers)).json()["data"]["values"]
        
        pressure_label = customtkinter.CTkLabel(master=self.frame, text="pressure_level", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        pressure_label.grid(row=3, column=0)

        pressure_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['pressureSurfaceLevel']}hPa" if weather_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
        pressure_data.grid(row=3, column=1)

        if self.map_widget.winfo_width() - event.x < self.frame._current_width and self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y - self.frame._current_height)
        elif self.map_widget.winfo_width() - event.x < self.frame._current_width:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y)
        elif self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x, y=event.y - self.frame._current_height)
        else:
            self.frame.place(x=event.x, y=event.y)


class WindLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def on_map_double_click(self, event):
        self.fill_frame(event)

        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        weather_url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat}, {lon}&apikey=AqwaRL5CVxt61JpyfxrCHeZAto4W6zlH"
        headers = {"accept": "application/json"}

        weather_response = (requests.get(weather_url, headers=headers)).json()["data"]["values"]
        
        wind_direction_label = customtkinter.CTkLabel(master=self.frame, text="wind_direction", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        wind_direction_label.grid(row=3, column=0)
        wind_gust_label = customtkinter.CTkLabel(master=self.frame, text="wind_gust", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        wind_gust_label.grid(row=4, column=0)
        wind_speed_label = customtkinter.CTkLabel(master=self.frame, text="wind_speed", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        wind_speed_label.grid(row=5, column=0)

        wind_direction_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['windDirection']}" + u"\N{DEGREE SIGN}" if weather_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
        wind_direction_data.grid(row=3, column=1)
        wind_gust_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['windGust']}m/s", text_color="black", anchor='w', justify='left',width=120, padx=8)
        wind_gust_data.grid(row=4, column=1)
        wind_speed_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['windSpeed']}m/s" if weather_response['humidity'] != None else "null", text_color="black", anchor='w', justify='left',width=120, padx=8)
        wind_speed_data.grid(row=5, column=1)

        if self.map_widget.winfo_width() - event.x < self.frame._current_width and self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y - self.frame._current_height)
        elif self.map_widget.winfo_width() - event.x < self.frame._current_width:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y)
        elif self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x, y=event.y - self.frame._current_height)
        else:
            self.frame.place(x=event.x, y=event.y)

class TemperatureLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def on_map_double_click(self, event):
        self.fill_frame(event)
        
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        weather_url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat}, {lon}&apikey=AqwaRL5CVxt61JpyfxrCHeZAto4W6zlH"
        headers = {"accept": "application/json"}

        weather_response = (requests.get(weather_url, headers=headers)).json()["data"]["values"]
        
        temperature_label = customtkinter.CTkLabel(master=self.frame, text="temperature", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        temperature_label.grid(row=3, column=0)
        temp_apparent_label = customtkinter.CTkLabel(master=self.frame, text="temperature_apparent", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        temp_apparent_label.grid(row=4, column=0)
        dew_label = customtkinter.CTkLabel(master=self.frame, text="dew_point", text_color="#888", anchor='e', justify='right',width=100, padx=8)
        dew_label.grid(row=5, column=0)

        temperature_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['temperature']}" + u"\N{DEGREE SIGN}" +"C" if weather_response else 'null', text_color="black", anchor='w', justify='left',width=120, padx=8)
        temperature_data.grid(row=3, column=1)
        temp_apparent_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['temperatureApparent']}" + u"\N{DEGREE SIGN}" +"C", text_color="black", anchor='w', justify='left',width=120, padx=8)
        temp_apparent_data.grid(row=4, column=1)
        dew_data = customtkinter.CTkLabel(master=self.frame, text=f"{weather_response['dewPoint']}" + u"\N{DEGREE SIGN}" +"C" if weather_response['humidity'] != None else "null", text_color="black", anchor='w', justify='left',width=120, padx=8)
        dew_data.grid(row=5, column=1)

        if self.map_widget.winfo_width() - event.x < self.frame._current_width and self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y - self.frame._current_height)
        elif self.map_widget.winfo_width() - event.x < self.frame._current_width:
            self.frame.place(x=event.x - self.frame._current_width, y=event.y)
        elif self.map_widget.winfo_height() - event.y < self.frame._current_height:
            self.frame.place(x=event.x, y=event.y - self.frame._current_height)
        else:
            self.frame.place(x=event.x, y=event.y)
