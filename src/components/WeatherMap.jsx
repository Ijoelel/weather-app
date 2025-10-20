import { useEffect } from "react";
import PropTypes from "prop-types";
import { MapContainer, TileLayer, useMap, useMapEvents } from "react-leaflet";

const BASE_TILE_URL = "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png";
const BASE_ATTRIBUTION =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>';
const OVERLAY_ATTRIBUTION =
  'Weather overlays &copy; <a href="https://openweathermap.org/">OpenWeatherMap</a>';

function WeatherMap({ center, overlayUrl, onDoubleClick }) {
  return (
    <MapContainer
      center={center}
      zoom={13}
      className="map"
      doubleClickZoom={false}
      scrollWheelZoom
    >
      <TileLayer attribution={BASE_ATTRIBUTION} url={BASE_TILE_URL} />
      {overlayUrl ? <TileLayer key={overlayUrl} url={overlayUrl} attribution={OVERLAY_ATTRIBUTION} opacity={0.7} /> : null}
      <Recenter position={center} />
      <MapEvents onDoubleClick={onDoubleClick} />
    </MapContainer>
  );
}

function Recenter({ position }) {
  const map = useMap();

  useEffect(() => {
    map.setView(position);
  }, [map, position]);

  return null;
}

function MapEvents({ onDoubleClick }) {
  useMapEvents({
    dblclick(event) {
      if (onDoubleClick) {
        onDoubleClick(event.latlng);
      }
    }
  });

  return null;
}

WeatherMap.propTypes = {
  center: PropTypes.shape({
    lat: PropTypes.number.isRequired,
    lng: PropTypes.number.isRequired
  }).isRequired,
  overlayUrl: PropTypes.string,
  onDoubleClick: PropTypes.func
};

WeatherMap.defaultProps = {
  overlayUrl: null,
  onDoubleClick: undefined
};

Recenter.propTypes = {
  position: PropTypes.shape({
    lat: PropTypes.number.isRequired,
    lng: PropTypes.number.isRequired
  }).isRequired
};

MapEvents.propTypes = {
  onDoubleClick: PropTypes.func
};

MapEvents.defaultProps = {
  onDoubleClick: undefined
};

export default WeatherMap;
