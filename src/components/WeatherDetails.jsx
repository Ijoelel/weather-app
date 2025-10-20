import { Fragment } from "react";
import PropTypes from "prop-types";

function WeatherDetails({ details, loading, errorMessage }) {
  if (loading) {
    return (
      <aside className="details-panel">
        <div className="details-panel__loading">Loading details…</div>
      </aside>
    );
  }

  if (errorMessage) {
    return (
      <aside className="details-panel">
        <h2>Details</h2>
        <div className="details-panel__error">{errorMessage}</div>
      </aside>
    );
  }

  if (!details) {
    return (
      <aside className="details-panel">
        <h2>Details</h2>
        <div className="details-panel__hint">
          Double-click anywhere on the map to explore the latest weather metrics for that spot.
        </div>
      </aside>
    );
  }

  return (
    <aside className="details-panel">
      <h2>Details</h2>

      <section className="details-panel__section">
        <h3>{details.location.heading}</h3>
        <div className="details-panel__rows">
          <span className="details-panel__label">latitude</span>
          <span className="details-panel__value">{details.coords.lat.toFixed(4)}</span>
          <span className="details-panel__label">longitude</span>
          <span className="details-panel__value">{details.coords.lng.toFixed(4)}</span>
          {details.location.fields.map((field) => (
            <Fragment key={field.label}>
              <span className="details-panel__label">{field.label}</span>
              <span className="details-panel__value">{field.value}</span>
            </Fragment>
          ))}
        </div>
      </section>

      <section className="details-panel__section">
        <h3>{`${details.layer} metrics`}</h3>
        <div className="details-panel__rows">
          {details.weather.map((field) => (
            <Fragment key={field.label}>
              <span className="details-panel__label">{field.label.replace(/_/g, " ")}</span>
              <span className="details-panel__value">{field.value}</span>
            </Fragment>
          ))}
        </div>
      </section>
    </aside>
  );
}

WeatherDetails.propTypes = {
  details: PropTypes.shape({
    coords: PropTypes.shape({
      lat: PropTypes.number.isRequired,
      lng: PropTypes.number.isRequired
    }).isRequired,
    location: PropTypes.shape({
      heading: PropTypes.string.isRequired,
      fields: PropTypes.arrayOf(
        PropTypes.shape({
          label: PropTypes.string.isRequired,
          value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired
        })
      ).isRequired
    }).isRequired,
    weather: PropTypes.arrayOf(
      PropTypes.shape({
        label: PropTypes.string.isRequired,
        value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired
      })
    ).isRequired,
    layer: PropTypes.string.isRequired
  }),
  loading: PropTypes.bool,
  errorMessage: PropTypes.string
};

WeatherDetails.defaultProps = {
  details: null,
  loading: false,
  errorMessage: ""
};

export default WeatherDetails;
