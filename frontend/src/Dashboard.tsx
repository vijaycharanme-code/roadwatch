import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import axios from 'axios';
import L from 'leaflet';

// Fix leaflet marker icons
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

interface Incident {
  id: number;
  latitude: number;
  longitude: number;
  aggregated_severity: string;
  status: string;
  report_count: number;
}

const Dashboard: React.FC = () => {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [route, setRoute] = useState<Incident[]>([]);

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    try {
      // In a real app, this points to localhost:8000 via env variables
      const res = await axios.get('http://localhost:8000/api/routing/incidents/');
      setIncidents(res.data);
    } catch (error) {
      console.error("Error fetching incidents", error);
    }
  };

  const calculateRoute = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/routing/incidents/route/');
      setRoute(res.data.route);
    } catch (error) {
      console.error("Error calculating route", error);
    }
  };

  const getMarkerColor = (severity: string) => {
    if (severity === 'CRITICAL') return 'red';
    if (severity === 'MEDIUM') return 'orange';
    return 'green';
  };

  // Create custom icons based on severity
  const createIcon = (color: string) => new L.Icon({
    iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
  });

  const routePositions: [number, number][] = route.map(inc => [inc.latitude, inc.longitude]);

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Arial' }}>
      <div style={{ width: '300px', padding: '20px', backgroundColor: '#f5f5f5', overflowY: 'auto' }}>
        <h2>RoadWatch Dashboard</h2>
        <button
          onClick={calculateRoute}
          style={{ padding: '10px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', width: '100%', marginBottom: '20px' }}
        >
          Calculate Optimal Route
        </button>

        <h3>Pending Incidents ({incidents.length})</h3>
        {incidents.map(inc => (
          <div key={inc.id} style={{ border: '1px solid #ddd', padding: '10px', marginBottom: '10px', borderRadius: '4px', backgroundColor: 'white' }}>
            <strong>Incident #{inc.id}</strong><br/>
            Severity: <span style={{ color: getMarkerColor(inc.aggregated_severity) }}>{inc.aggregated_severity}</span><br/>
            Reports merged: {inc.report_count}
          </div>
        ))}
      </div>
      <div style={{ flex: 1 }}>
        <MapContainer center={[13.0827, 80.2707]} zoom={12} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {incidents.map(inc => (
            <Marker key={inc.id} position={[inc.latitude, inc.longitude]} icon={createIcon(getMarkerColor(inc.aggregated_severity))}>
              <Popup>
                <strong>Incident #{inc.id}</strong><br/>
                Severity: {inc.aggregated_severity}<br/>
                Reports: {inc.report_count}
              </Popup>
            </Marker>
          ))}

          {routePositions.length > 0 && (
            <Polyline positions={routePositions} color="blue" weight={4} dashArray="5, 10" />
          )}
        </MapContainer>
      </div>
    </div>
  );
};

export default Dashboard;
