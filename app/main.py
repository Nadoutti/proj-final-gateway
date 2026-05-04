from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import eventos, ingressos, usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(timeout=30.0)
    yield
    await app.state.http_client.aclose()


app = FastAPI(title="API Gateway", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingressos.router)
app.include_router(eventos.router)
app.include_router(usuarios.router)


@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
