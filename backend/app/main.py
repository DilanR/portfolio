from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.core.rate_limiter import RateLimitMiddleware
from app.core.config import RUSTPILER_BIN, TMP_ROOT
from app.routes.rustpiler import router as compile_router

import shutil


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for MVP
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)

app.include_router(compile_router, prefix="/api")

# load binaries to tmp
rustpiler_src = RUSTPILER_BIN
RUSTPILER_TMP = TMP_ROOT / "rustpiler"

if not RUSTPILER_TMP.exists():
    shutil.copy2(rustpiler_src, RUSTPILER_TMP)
    RUSTPILER_TMP.chmod(0o555)
