from fastapi import APIRouter
from fastapi import UploadFile, File, Form, HTTPException
import json

from app.services.opts import CompileOptions
from app.services.rustpiler import execute as run_rustpiler


router = APIRouter()


@router.post("/rustpiler/compile")
async def compile(file: UploadFile = File(...), options: str = Form(...)):
    try:
        opts = CompileOptions(**json.loads(options))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid options: {e}")

    content = await file.read()

    return await run_rustpiler(content, opts)
