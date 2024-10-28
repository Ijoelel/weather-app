from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tkintermapview.map_widget import TkinterMapView

class Layer:
    def __init__(self, map_widget: "TkinterMapView"):
        self.map_widget = map_widget
        self.map_widget.canvas.bind("<Double-1>", self.on_map_double_click)

    def set_overlay(self, overlay_url_template):
        self.map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")
        self.map_widget.set_overlay_tile_server(overlay_url_template)

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        data = self.active_layer.get_data(lat, lon)
        if data:
            self.display_weather_data(data)

    def get_data(self, lat, lon):
        pass  # Will be overridden by subclasses to fetch layer-specific data

class CloudLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)
        # data = self.active_layer.get_data(lat, lon)
        # if data:
        #     self.display_weather_data(data)

class PrecipitationLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)

class PressureLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

    def on_map_double_click(self, event):
        lat, lon = self.map_widget.convert_canvas_coords_to_decimal_coords(event.x, event.y)

class WindLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

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