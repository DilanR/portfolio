from pathlib import Path
from pydantic import BaseModel, ConfigDict
import subprocess
import tempfile
import os

DOCKER_IMAGE = "dilan/rustpiler:latest"


class CompileOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type_check: bool = False
    virtual_machine: bool = False
    code_gen: bool = False
    run: bool = False

    ast: bool = False
    asm: bool = False


def validate_options(opts: CompileOptions):
    # asm requires code_gen
    if opts.asm and not opts.code_gen:
        raise ValueError("--asm requires code_gen (-c)")

    # run requires code_gen
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


def execute(file_bytes: bytes, opts) -> dict:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".rnr") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    with tempfile.TemporaryDirectory() as out_dir:
        out_dir_path = Path(out_dir)
        asm_host_path = out_dir_path / "out.asm"

        try:
            cli_args = build_args("/input.rnr", opts)

            # if asm requested → force container path
            if opts.asm:
                cli_args += ["--asm", "/out/out.asm"]

            result = subprocess.run(
                [
                    "docker",
                    "run",
                    "--rm",
                    "--memory=64m",
                    "--cpus=0.5",
                    "--pids-limit=64",
                    "--network=none",
                    "--read-only",
                    "-v",
                    f"{tmp_path}:/input.rnr:ro",
                    "-v",
                    f"{out_dir}:/out",
                    DOCKER_IMAGE,
                    *cli_args,
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )

            asm_content = None
            if opts.asm and asm_host_path.exists():
                asm_content = asm_host_path.read_text()

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "assembly": asm_content,
                "returncode": result.returncode,
            }

        finally:
            os.remove(tmp_path)
