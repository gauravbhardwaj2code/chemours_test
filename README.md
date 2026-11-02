# RoomBook

A small meeting-room booking app: FastAPI backend, React frontend.

The task is in [ASSIGNMENT.md](ASSIGNMENT.md).

## Requirements

- Python 3.11+
- Node 18+
- Optional: Docker (for PostgreSQL). Without it, the backend uses a local SQLite file.

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed          # resets the database and loads sample data
uvicorn app.main:app --reload
```

The API runs on http://localhost:8000. Interactive docs are at http://localhost:8000/docs.

### Using PostgreSQL instead of SQLite

```bash
docker compose up -d
export DATABASE_URL=postgresql+psycopg://roombook:roombook@localhost:5432/roombook
python -m app.seed
uvicorn app.main:app --reload
```

### Settings

| Variable | Default | Meaning |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./roombook.db` | SQLAlchemy database URL |
| `SIMULATED_LATENCY_MS` | `800` | Adds a random 0–N ms delay to GET requests, to make local dev behave more like a real network. Set to `0` to turn it off. |

### Tests

```bash
cd backend
pytest
```

Tests use an in-memory SQLite database with the same sample data as `app/seed.py`.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The dev server proxies `/api/*` to the backend on port 8000.

## Sample data

`python -m app.seed` loads 6 users, 3 rooms and a few bookings. Most bookings are on **Monday 2026-12-07**, and there are some on the days around it. The frontend opens on that date.

| id | User | Role |
|---|---|---|
| 1 | Asha | employee |
| 2 | Ben | employee |
| 3 | Chen | manager |
| 4 | Divya | intern |
| 5 | Eli | employee |
| 6 | Farah | employee |

| id | Room | Capacity |
|---|---|---|
| 1 | Focus Room | 4 |
| 2 | Board Room | 12 |
| 3 | Huddle | 6 |

## API

| Method | Path | Notes |
|---|---|---|
| GET | `/rooms` | |
| GET | `/rooms/{id}` | |
| POST | `/rooms` | `{name, capacity}` |
| GET | `/users` | |
| GET | `/bookings?date=YYYY-MM-DD&room_id=` | Both filters optional |
| POST | `/bookings` | `{room_id, creator_id, title, attendee_ids, start, end}`; returns `409` if the room is taken |

### Examples

```bash
curl -s "localhost:8000/bookings?date=2026-12-07&room_id=3"
```

```bash
curl -s -X POST localhost:8000/bookings \
  -H 'Content-Type: application/json' \
  -d '{"room_id": 3, "creator_id": 2, "title": "Pairing", "attendee_ids": [2],
       "start": "2026-12-07T12:15:00+05:30", "end": "2026-12-07T12:45:00+05:30"}'
```
