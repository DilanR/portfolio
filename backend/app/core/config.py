from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

RUSTPILER_BIN = Path(os.getenv("RUSTPILER_BIN", "/usr/local/bin/rustpiler"))
NSJAIL_CFG = Path(os.getenv("NSJAIL_CFG", BASE_DIR / "nsjail.cfg"))
TMP_ROOT = Path(os.getenv("TMP_ROOT", "/tmp"))

RUSTPILER_BIN = RUSTPILER_BIN.resolve()
NSJAIL_CFG = NSJAIL_CFG.resolve()
TMP_ROOT = TMP_ROOT.resolve()
