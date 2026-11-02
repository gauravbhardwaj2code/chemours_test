import { useEffect, useState } from "react";
import { getRooms } from "../api.js";

export default function RoomList() {
  const [rooms, setRooms] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getRooms()
      .then(setRooms)
      .catch((err) => setError(err.message));
  }, []);

  return (
    <section className="card">
      <h2>Rooms</h2>
      {error && <p className="error">{error}</p>}
      <ul>
        {rooms.map((room) => (
          <li key={room.id}>
            <strong>{room.name}</strong>
            <span className="muted"> · seats {room.capacity}</span>
          </li>
        ))}
      </ul>
    </section>
  );
}
