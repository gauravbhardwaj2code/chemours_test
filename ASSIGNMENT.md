# RoomBook: take-home assignment

RoomBook is a small meeting-room booking app. You'll get a working starter repo, then fix a bug, build a slot-finding API, make booking safe under concurrency, and add a small React UI.

- **Stack:** FastAPI (Python 3.11+), SQLAlchemy, PostgreSQL (via `docker compose`) or SQLite, React + Vite
- **Time box:** 3–4 hours. Please stop at 4 hours. Unfinished parts are fine if DECISIONS.md says what you would do next.
- **AI tools:** allowed. Tell us how you used them (see Task 5).
- **After you submit:** a 60-minute call where you walk us through your code and make a few small changes to it live, on screen share. Please be ready to run the app and tests locally during that call.

---

## The starter repo

```
backend/    FastAPI app, models, seed data, pytest tests
frontend/   React app (Vite)
```

It already has:

- `GET/POST /rooms`, `GET/POST /bookings`, `GET /users`
- Users have a `role`: `employee`, `manager` or `intern`
- A booking has a room, a start, an end, a creator and a list of attendees (users)
- A React page that lists rooms and the bookings for a chosen date
- A seed script with sample rooms, users and bookings

See `README.md` in the starter repo for setup commands.

### Office rules (apply to everything below)

- Office time is **IST (Asia/Kolkata)**. Working hours are **09:30–18:30 IST**, Monday to Friday.
- Times are half-open intervals: a meeting from 10:00 to 11:00 does **not** clash with one from 11:00 to 12:00.
- Durations are multiples of 15 minutes, from 15 to 240.

---

## Task 1: Fix the reported bug (~30 min)

A user reported: **"Back-to-back bookings are rejected. I can't book 11:00–12:00 when someone has 10:00–11:00."**

1. Fix it.
2. Add a test that would have caught it.
3. In `DECISIONS.md`, list **any other problems you notice** in the codebase (bugs, risks, missing validation). You don't have to fix them, but say how serious you think each one is.

## Task 2: "Find me a slot" API (~1.5 hrs)

Add `POST /rooms/{room_id}/suggest`.

Request:

```json
{
  "requester_id": 3,
  "attendee_ids": [1, 2],
  "duration_minutes": 45,
  "date": "2026-12-07"
}
```

Response: the **first 3** valid slots on that date, earliest first. Return fewer if fewer exist.

```json
{
  "slots": [
    { "start": "2026-12-07T14:00:00+05:30", "end": "2026-12-07T14:45:00+05:30" }
  ]
}
```

A slot is valid only if all of these hold:

- Slot starts fall on 15-minute boundaries (09:30, 09:45, 10:00, ...).
- The meeting starts and ends within working hours.
- The room has no overlapping booking.
- No attendee has an overlapping booking **in any room**.
- **Cleaning buffer:** a meeting longer than 60 minutes needs a 15-minute cleaning buffer after it, during which the room can't be used.
- **Restricted room:** users with role `intern` can't book the **Board Room**.
- **Lunch hour:** no meeting may overlap 13:00–14:00, **unless** it is 30 minutes or shorter.

Where these rules don't say exactly what to do, make a reasonable choice and write it down in DECISIONS.md. Add tests for the rules.

## Task 3: Prevent double booking (~30 min)

If two users book the same room for overlapping times at the same moment, exactly one must succeed. The other gets a clear error (`409 Conflict`).

Choose the approach yourself (database constraint, transaction/locking, or something else). Explain in DECISIONS.md why you chose it and where it would stop working. Add a test if you can.

## Task 4: React UI (~1 hr)

Add a "Find a slot" form:

- Pick a room, attendees, a duration and a date
- Show the suggested slots
- Book a slot with one click
- Handle loading and error states, and the case where **the slot was taken by someone else** between showing it and clicking it

Plain CSS is fine. We care about behaviour, not looks.

## Task 5: DECISIONS.md (~15 min)

Keep it short. Bullet points are fine.

- **Assumptions** you made where the spec was unclear
- **Trade-offs** you chose, and the alternatives you rejected
- **Other problems** you noticed (from Task 1)
- **With more time**, what you'd do next
- **AI usage:** which tools, for which parts, and **at least one place where the AI was wrong** or you rejected its suggestion, and why

---

## Submission: one pull request per task

Work the way you would on a team: each task is its own pull request, reviewed in your own **private** repo.

### Setup (5 min)

Please **don't fork** this repo and don't open pull requests against it. Forks of a public repo are public, so your solution would be visible to other candidates.

1. Create a new **private** GitHub repo (for example `roombook-<your-name>`).
2. Push this starter's `main` to it:
   ```bash
   git clone <this repo URL> roombook && cd roombook
   git remote set-url origin <your private repo URL>
   git push -u origin main
   ```
3. Add **REVIEWER_GITHUB_USERNAME** as a collaborator with read access.

### Pull requests

Open these PRs against `main`, in this order:

| PR | Branch (suggested) | Contains |
|---|---|---|
| 1 | `fix/back-to-back-bookings` | Task 1: the fix, its test, and `DECISIONS.md` with your list of other problems |
| 2 | `feat/suggest-slots` | Task 2: the `/suggest` endpoint and its tests |
| 3 | `feat/prevent-double-booking` | Task 3: your double-booking guard |
| 4 | `feat/find-slot-ui` | Task 4: the React form |

- **Merge each PR into `main` yourself before you start the next one.** Use a normal merge commit, not squash, so we can see your commits.
- **Commit as you go** inside each PR. Please don't squash a whole task into one commit; we read the history.
- **Each PR description** should say, in a few lines:
  - what changed, and why this way
  - how to test it (commands, or steps in the UI)
  - how you used AI for this task, if at all
- Add to `DECISIONS.md` in the PR it relates to (Task 5), rather than writing it all at the end.
- Keep `README.md` up to date with any new setup steps, and keep tests runnable with one command (for example `pytest`).

If you run out of time, open the unfinished PR as a **draft** and say in its description what's left.

When you're done, send us the link to your private repo.

Questions about the spec? Make an assumption, write it down, and keep going. That's part of the exercise.
