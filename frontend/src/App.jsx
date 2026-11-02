import { useState } from "react";
import DateNav from "./components/DateNav.jsx";
import RoomList from "./components/RoomList.jsx";
import BookingList from "./components/BookingList.jsx";

const FIRST_SEEDED_DAY = "2026-12-07";

export default function App() {
  const [date, setDate] = useState(FIRST_SEEDED_DAY);

  return (
    <main>
      <header>
        <h1>RoomBook</h1>
        <DateNav date={date} onChange={setDate} />
      </header>
      <div className="layout">
        <RoomList />
        <BookingList date={date} />
      </div>
    </main>
  );
}
