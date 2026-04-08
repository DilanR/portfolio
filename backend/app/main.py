from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.core.rate_limiter import RateLimitMiddleware
from app.routes.compile import router as compile_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for MVP
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)

app.include_router(compile_router, prefix="/api")
