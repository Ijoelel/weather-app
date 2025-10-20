# WeatherMaps

A React web application that visualises global weather data on top of an interactive map. Switch between cloud, precipitation, pressure, wind, and temperature overlays, search for locations, and double-click the map to view detailed metrics.

## Getting started

1. Install dependencies
   ```bash
   npm install
   ```
2. Start the development server
   ```bash
   npm run dev
   ```
3. Visit the app at the URL printed in the terminal (defaults to `http://localhost:5173`).

## Building for production

```bash
npm run build
```

This command outputs the static site to the `dist/` directory, ready to deploy to any static hosting service.

## Data sources

- [OpenWeatherMap](https://openweathermap.org/) for map overlays
- [Tomorrow.io](https://www.tomorrow.io/) for live weather measurements
- [Geoapify](https://www.geoapify.com/) for reverse geocoding
- [DistanceMatrix.ai](https://distancematrix.ai/) for location search
