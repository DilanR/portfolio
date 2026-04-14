from pathlib import Path
from pydantic import BaseModel, ConfigDict
import asyncio
import tempfile
import shutil
import os


class CompileOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type_check: bool = False
    virtual_machine: bool = False
    code_gen: bool = False
    run: bool = False

    ast: bool = False
    asm: bool = False


# limit concurrent executions
semaphore = asyncio.Semaphore(4)


def validate_options(opts: CompileOptions):
    if opts.asm and not opts.code_gen:
        raise ValueError("--asm requires code_gen (-c)")

    if opts.run and not opts.code_gen:
        raise ValueError("-r requires code_gen (-c)")


def build_args(input_path: str, opts: CompileOptions) -> list[str]:
    args = ["-i", input_path]

    if opts.type_check:
        args.append("-t")

    if opts.virtual_machine:
        args.append("-v")

    if opts.code_gen:
        args.append("-c")

    if opts.run:
        args.append("-r")

    return args


async def execute(file_bytes: bytes, opts: CompileOptions) -> dict:
    validate_options(opts)

    async with semaphore:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # write input file
            input_path = tmpdir_path / "input.rnr"
            input_path.write_bytes(file_bytes)

            # output file
            asm_path = tmpdir_path / "out.asm"

            # copy binary into jail
            shutil.copy("/usr/local/bin/rustpiler", tmpdir_path / "rustpiler")

            # build args using jail paths
            cli_args = build_args("/input.rnr", opts)

            if opts.asm:
                cli_args += ["--asm", "/out.asm"]

            nsjail_cfg = (
                os.getenv("BACKEND_ROOT", "/backend") + "/nsjail.cfg",
            )  # change for Docker later

            cmd = [
                "nsjail",
                "--config",
                nsjail_cfg,
                "--",
                "/rustpiler",
                *cli_args,
            ]

            print(" ".join(cmd))  # debug

            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=tmpdir,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(), timeout=5
                )
            except asyncio.TimeoutError:
                process.kill()
                return {
                    "success": False,
                    "output": "",
                    "error": "Execution timed out",
                    "assembly": None,
                    "returncode": -1,
                }

            asm_content = None
            if opts.asm and asm_path.exists():
                asm_content = asm_path.read_text()

            return {
                "success": process.returncode == 0,
                "output": stdout.decode(),
                "error": stderr.decode(),
                "assembly": asm_content,
                "returncode": process.returncode,
            }
