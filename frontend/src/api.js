const BASE = "/api";

async function request(path, options) {
  const res = await fetch(BASE + path, options);
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = typeof body.detail === "string" ? body.detail : null;
    throw new Error(detail || `Request failed (${res.status})`);
  }
  return res.json();
}

export const getRooms = () => request("/rooms");

export const getUsers = () => request("/users");

export const getBookings = (date) => request(`/bookings?date=${date}`);

export const createBooking = (booking) =>
  request("/bookings", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(booking),
  });
