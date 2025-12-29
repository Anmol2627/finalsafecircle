import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with Webpack
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

function LocationMarker({ onLocationFound }) {
  const [position, setPosition] = useState(null);
  const map = useMap();

  useEffect(() => {
    map.locate().on("locationfound", function (e) {
      setPosition(e.latlng);
      map.flyTo(e.latlng, map.getZoom());
      if (onLocationFound) onLocationFound(e.latlng);
    });
  }, [map, onLocationFound]);

  return position === null ? null : (
    <Marker position={position}>
      <Popup>You are here</Popup>
    </Marker>
  );
}

export default function MapComponent({ incidents = [], className }) {
  const [userLocation, setUserLocation] = useState(null);

  // Default to San Francisco if no location
  const defaultPosition = [37.7749, -122.4194]; 

  return (
    <div className={className || "h-64 w-full rounded-lg overflow-hidden"}>
      <MapContainer 
        center={defaultPosition} 
        zoom={13} 
        scrollWheelZoom={false} 
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <LocationMarker onLocationFound={setUserLocation} />
        
        {incidents.map((incident) => {
            if (incident.location && incident.location.lat && incident.location.lng) {
                return (
                    <Marker 
                        key={incident.id} 
                        position={[incident.location.lat, incident.location.lng]}
                    >
                        <Popup>
                            <strong>{incident.type}</strong><br/>
                            {incident.description}
                        </Popup>
                    </Marker>
                );
            }
            return null;
        })}
      </MapContainer>
    </div>
  );
}
