import React, { useEffect, useState } from "react";
import "./DroneFlight.css";

function DroneFlight() {
  const [droneflight, setDroneflight] = useState([]);
  const [loading, setLoading] = useState(true);
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/droneflights")
      .then((response) => response.json())
      .then((data) => {
        setDroneflight(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching droneflight data:", error);
        setLoading(false);
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      if (response.ok) {
        const data = await response.json();
        setResponse(data.response);
      }
    } catch (error) {
      console.error("Network error: ", error);
      setResponse("Network error occurred. Please try again later.");
    }
  };

  return (
    <div className="queries">
      <form onSubmit={handleSubmit}>
        <label htmlFor="Description">Enter your query</label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="What is the battery level of the drone during the last image?"
        />
        <button type="submit">Submit</button>
      </form>

      {response && (
        <div className="response">
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}

      {loading ? (
        <p>Loading drone data...</p>
      ) : (
        <div className="drone-data-container">
          <table className="drone-data-table">
            <thead>
              <tr>
                <th>Image ID</th>
                <th>Timestamp</th>
                <th>Latitude</th>
                <th>Longitude</th>
                <th>Altitude (m)</th>
                <th>Heading (°)</th>
                <th>File Name</th>
                <th>Camera Tilt (°)</th>
                <th>Focal Length (mm)</th>
                <th>ISO</th>
                <th>Shutter Speed</th>
                <th>Aperture</th>
                <th>Color Temperature (K)</th>
                <th>Image Format</th>
                <th>File Size (MB)</th>
                <th>Drone Speed (m/s)</th>
                <th>Battery Level (%)</th>
                <th>GPS Accuracy (m)</th>
                <th>Gimbal Mode</th>
                <th>Subject Detection</th>
                <th>Image Tags</th>
              </tr>
            </thead>
            <tbody>
              {droneflight.map((flight) => (
                <tr key={flight.image_id}>
                  <td>{flight.image_id}</td>
                  <td>{flight.timestamp}</td>
                  <td>{flight.latitude}</td>
                  <td>{flight.longitude}</td>
                  <td>{flight.altitude_m}</td>
                  <td>{flight.heading_deg}</td>
                  <td>{flight.file_name}</td>
                  <td>{flight.camera_tilt_deg}</td>
                  <td>{flight.focal_length_mm}</td>
                  <td>{flight.iso}</td>
                  <td>{flight.shutter_speed}</td>
                  <td>{flight.aperture}</td>
                  <td>{flight.color_temp_k}</td>
                  <td>{flight.image_format}</td>
                  <td>{flight.file_size_mb}</td>
                  <td>{flight.drone_speed_mps}</td>
                  <td>{flight.battery_level_pct}</td>
                  <td>{flight.gps_accuracy_m}</td>
                  <td>{flight.gimbal_mode}</td>
                  <td>{flight.subject_detection}</td>
                  <td>{flight.image_tags?.join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default DroneFlight;
