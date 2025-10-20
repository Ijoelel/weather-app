import { useEffect, useMemo, useState } from "react";
import axios from "axios";
import WeatherMap from "./components/WeatherMap.jsx";
import WeatherDetails from "./components/WeatherDetails.jsx";
import "leaflet/dist/leaflet.css";
import "./App.css";

const DEFAULT_POSITION = { lat: -6.1754, lng: 106.8272 }; // Jakarta

const LAYER_CONFIG = {
  Cloud: {
    label: "Cloud",
    overlayUrl:
      "https://tile.openweathermap.org/map/clouds_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471",
    weatherFields: (data) => [
      { label: "cloud_cover", value: withUnit(data.cloudCover, "%") },
      { label: "cloud_base", value: withUnit(data.cloudBase, " km") },
      { label: "cloud_ceiling", value: withUnit(data.cloudCeiling, " km") }
    ]
  },
  Precipitation: {
    label: "Precipitation",
    overlayUrl:
      "https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471",
    weatherFields: (data) => [
      { label: "precipitation_probability", value: withUnit(data.precipitationProbability, "%") },
      { label: "rain_intensity", value: withUnit(data.rainIntensity, " mm/hr") },
      { label: "humidity", value: withUnit(data.humidity, "%") }
    ]
  },
  Pressure: {
    label: "Pressure",
    overlayUrl:
      "https://tile.openweathermap.org/map/pressure_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471",
    weatherFields: (data) => [
      { label: "surface_pressure", value: withUnit(data.pressureSurfaceLevel, " hPa") }
    ]
  },
  Wind: {
    label: "Wind",
    overlayUrl:
      "https://tile.openweathermap.org/map/wind_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471",
    weatherFields: (data) => [
      { label: "wind_direction", value: withDegree(data.windDirection) },
      { label: "wind_gust", value: withUnit(data.windGust, " m/s") },
      { label: "wind_speed", value: withUnit(data.windSpeed, " m/s") }
    ]
  },
  Temperature: {
    label: "Temperature",
    overlayUrl:
      "https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid=bdb5a3638f7c947577e361feb6a14471",
    weatherFields: (data) => [
      { label: "temperature", value: withUnit(data.temperature, "°C") },
      { label: "temperature_apparent", value: withUnit(data.temperatureApparent, "°C") },
      { label: "dew_point", value: withUnit(data.dewPoint, "°C") }
    ]
  }
};

function withUnit(value, unit) {
  if (value === undefined || value === null) {
    return "—";
  }
  return `${value}${unit}`;
}

function withDegree(value) {
  if (value === undefined || value === null) {
    return "—";
  }
  return `${value}°`;
}

function App() {
  const [selectedLayer, setSelectedLayer] = useState("Cloud");
  const [position, setPosition] = useState(DEFAULT_POSITION);
  const [searchValue, setSearchValue] = useState("");
  const [details, setDetails] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    if (!navigator.geolocation) {
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (result) => {
        const { latitude, longitude } = result.coords;
        setPosition({ lat: latitude, lng: longitude });
      },
      () => {
        // Ignore geolocation errors and keep the default position
      }
    );
  }, []);

  const overlayUrl = useMemo(() => LAYER_CONFIG[selectedLayer].overlayUrl, [selectedLayer]);

  const handleSearch = async (event) => {
    event?.preventDefault();
    if (!searchValue.trim()) {
      return;
    }

    setErrorMessage("");

    try {
      const response = await axios.get(
        "https://api-v2.distancematrix.ai/maps/api/geocode/json",
        {
          params: {
            address: searchValue,
            key: "89rzA8N4hHGOm25oStS6aRKDLKuOEex9wekgHZyBgkbXKzKP5FMisNVj8bu5MiTs"
          }
        }
      );

      const geometry = response.data?.result?.[0]?.geometry?.location;
      if (!geometry) {
        throw new Error("Location not found");
      }

      const nextPosition = { lat: parseFloat(geometry.lat), lng: parseFloat(geometry.lng) };
      setPosition(nextPosition);
      setDetails(null);
    } catch (error) {
      console.error("Search error", error);
      setErrorMessage("Unable to find the requested location. Try another search term.");
    }
  };

  const handleMapDoubleClick = async ({ lat, lng }) => {
    setLoadingDetails(true);
    setErrorMessage("");

    try {
      const [locationResponse, weatherResponse] = await Promise.all([
        axios.get("https://api.geoapify.com/v1/geocode/reverse", {
          params: {
            lat,
            lon: lng,
            apiKey: "0d010075997245ca8559e806edf4a67c"
          }
        }),
        axios.get("https://api.tomorrow.io/v4/weather/realtime", {
          params: {
            location: `${lat}, ${lng}`,
            apikey: "AqwaRL5CVxt61JpyfxrCHeZAto4W6zlH"
          }
        })
      ]);

      const properties = locationResponse.data?.features?.[0]?.properties;
      const weatherData = weatherResponse.data?.data?.values;

      if (!properties || !weatherData) {
        throw new Error("Missing data");
      }

      const locationDetails = buildLocationDetails(properties);
      const weatherDetails = LAYER_CONFIG[selectedLayer].weatherFields(weatherData);

      setDetails({
        coords: { lat, lng },
        location: locationDetails,
        weather: weatherDetails,
        layer: selectedLayer
      });
    } catch (error) {
      console.error("Detail error", error);
      setErrorMessage("We couldn't load detailed data for that location. Please try another spot.");
    } finally {
      setLoadingDetails(false);
    }
  };

  return (
    <div className="app">
      <header className="app__header">
        <div>
          <h1>WeatherMaps</h1>
          <p>Interactive weather overlays and local insights for any point on the globe.</p>
        </div>
        <form className="search" onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Search for a place"
            value={searchValue}
            onChange={(event) => setSearchValue(event.target.value)}
            aria-label="Search for a location"
          />
          <button type="submit">Search</button>
        </form>
      </header>

      <main className="app__content">
        <div className="map-panel">
          <div className="map-panel__toolbar">
            <label htmlFor="layer-select">Layer</label>
            <select
              id="layer-select"
              value={selectedLayer}
              onChange={(event) => {
                setSelectedLayer(event.target.value);
                setDetails(null);
              }}
            >
              {Object.keys(LAYER_CONFIG).map((layer) => (
                <option key={layer} value={layer}>
                  {LAYER_CONFIG[layer].label}
                </option>
              ))}
            </select>
          </div>
          <WeatherMap
            center={position}
            overlayUrl={overlayUrl}
            onDoubleClick={handleMapDoubleClick}
          />
        </div>

        <WeatherDetails
          details={details}
          loading={loadingDetails}
          errorMessage={errorMessage}
        />
      </main>

      <footer className="app__footer">
        <p>
          Double-click the map to load local details. Data provided by Geoapify, Tomorrow.io, and OpenWeatherMap.
        </p>
      </footer>
    </div>
  );
}

function buildLocationDetails(properties) {
  if (!properties) {
    return { heading: "Unknown location", fields: [] };
  }

  if (properties.country) {
    return {
      heading: properties.formatted || properties.city || properties.country,
      fields: filterFields([
        { label: "country", value: properties.country },
        { label: "state", value: properties.state },
        { label: "city", value: properties.city },
        { label: "postcode", value: properties.postcode }
      ])
    };
  }

  if (properties.ocean) {
    return {
      heading: properties.name || properties.ocean,
      fields: filterFields([
        { label: "ocean", value: properties.ocean },
        { label: "sea", value: properties.sea }
      ])
    };
  }

  if (properties.marinearea) {
    return {
      heading: properties.name || properties.marinearea,
      fields: filterFields([
        { label: "sea", value: properties.marinearea },
        { label: "feature", value: properties.feature_name }
      ])
    };
  }

  return {
    heading: properties.name || properties.formatted || "Unknown location",
    fields: []
  };
}

function filterFields(fields) {
  return fields.filter((field) => field.value !== undefined && field.value !== null && field.value !== "");
}

export default App;
