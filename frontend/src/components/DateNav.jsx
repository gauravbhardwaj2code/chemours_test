import { shiftDate } from "../dates.js";

export default function DateNav({ date, onChange }) {
  return (
    <div className="date-nav">
      <button onClick={() => onChange(shiftDate(date, -1))} aria-label="Previous day">
        ←
      </button>
      <input type="date" value={date} onChange={(e) => onChange(e.target.value)} />
      <button onClick={() => onChange(shiftDate(date, 1))} aria-label="Next day">
        →
      </button>
    </div>
  );
}
