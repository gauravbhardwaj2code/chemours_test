import { useEffect, useState } from "react";
import { getBookings } from "../api.js";
import { formatTime } from "../dates.js";

export default function BookingList({ date }) {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getBookings(date)
      .then(setBookings)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [date]);

  return (
    <section className="card">
      <h2>Bookings for {date}</h2>
      {loading && <p className="muted">Loading…</p>}
      {error && <p className="error">{error}</p>}
      {!loading && !error && bookings.length === 0 && <p className="muted">No bookings.</p>}
      <table>
        <tbody>
          {bookings.map((b) => (
            <tr key={b.id}>
              <td className="time">
                {formatTime(b.start)}–{formatTime(b.end)}
              </td>
              <td>{b.room.name}</td>
              <td>{b.title}</td>
              <td className="muted">{b.attendees.map((a) => a.name).join(", ")}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
