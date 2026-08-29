import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users, auth, bookings, spaces, dashboard
from app.core.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_tables()
        print("Tablas creadas correctamente", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"No se pudieron crear las tablas: {e}", file=sys.stderr, flush=True)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(users.router)
app.include_router(auth.router)
app.include_router(bookings.router)
app.include_router(spaces.router)
app.include_router(dashboard.router)


@app.get("/")
def root():
    return {"message": "Welcome to the API"}
