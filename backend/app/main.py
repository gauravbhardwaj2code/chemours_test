import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401  (registers tables)
from .db import Base, engine
from .latency import SimulatedLatencyMiddleware
from .routers import bookings, rooms, users

SIMULATED_LATENCY_MS = int(os.getenv("SIMULATED_LATENCY_MS", "800"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="RoomBook", lifespan=lifespan)
app.add_middleware(SimulatedLatencyMiddleware, max_ms=SIMULATED_LATENCY_MS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(users.router)
app.include_router(bookings.router)


@app.get("/health")
def health():
    return {"status": "ok"}
