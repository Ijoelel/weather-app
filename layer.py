class Layer:
    def __init__(self, map_widget):
        self.map_widget = map_widget

    def set_overlay(self, overlay_url_template):
        self.map_widget.set_tile_server("https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")
        self.map_widget.set_overlay_tile_server(overlay_url_template)

    def get_data(self, lat, lon):
        pass  # Will be overridden by subclasses to fetch layer-specific data

class CloudLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

class PrecipitationLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

class PressureLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

class WindLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass

class TemperatureLayer(Layer):
    def __init__(self, map_widget):
        super().__init__(map_widget)
        self.set_overlay("https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471")

    def get_data(self, lat, lon):
        pass