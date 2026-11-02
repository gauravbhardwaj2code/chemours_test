"""Reset the database and load sample data.

    python -m app.seed
"""

from datetime import datetime

from sqlalchemy.orm import Session

from .db import Base, SessionLocal, engine
from .models import Booking, Room, User

USERS = [
    (1, "Asha", "employee"),
    (2, "Ben", "employee"),
    (3, "Chen", "manager"),
    (4, "Divya", "intern"),
    (5, "Eli", "employee"),
    (6, "Farah", "employee"),
]

ROOMS = [
    (1, "Focus Room", 4),
    (2, "Board Room", 12),
    (3, "Huddle", 6),
]

# (room_id, title, date, start, end, attendee_ids). The first attendee is the creator.
BOOKINGS = [
    (3, "Customer call", "2026-12-04", "16:00", "17:00", [5]),
    (1, "1:1", "2026-12-07", "09:30", "10:00", [1]),
    (1, "Hiring panel", "2026-12-07", "10:00", "11:30", [3]),
    (3, "Standup sync", "2026-12-07", "11:45", "12:15", [2]),
    (1, "Vendor call", "2026-12-07", "14:00", "14:30", [5]),
    (2, "Quarterly review", "2026-12-07", "15:00", "17:00", [1, 3]),
    (1, "Design review", "2026-12-07", "16:00", "16:30", [2]),
    (3, "Retro", "2026-12-07", "17:30", "18:30", [1]),
    (2, "Budget planning", "2026-12-07", "09:30", "13:00", [6]),
    (1, "Interview debrief", "2026-12-08", "10:00", "11:00", [2, 3]),
    (3, "Onboarding", "2026-12-08", "15:00", "15:30", [3, 4]),
    (2, "Roadmap", "2026-12-09", "11:00", "12:00", [1, 6]),
]


def _at(day: str, hhmm: str) -> datetime:
    return datetime.fromisoformat(f"{day}T{hhmm}")


def seed(db: Session) -> None:
    # Insert in order so ids match the tables above on a fresh database.
    users = {}
    for uid, name, role in USERS:
        users[uid] = User(name=name, role=role)
        db.add(users[uid])
        db.flush()
    for rid, name, cap in ROOMS:
        db.add(Room(name=name, capacity=cap))
        db.flush()
    for room_id, title, day, start, end, attendee_ids in BOOKINGS:
        db.add(
            Booking(
                room_id=room_id,
                creator_id=attendee_ids[0],
                title=title,
                start=_at(day, start),
                end=_at(day, end),
                attendees=[users[uid] for uid in attendee_ids],
            )
        )
    db.commit()


def main() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    print(f"Seeded {len(USERS)} users, {len(ROOMS)} rooms, {len(BOOKINGS)} bookings.")


if __name__ == "__main__":
    main()
