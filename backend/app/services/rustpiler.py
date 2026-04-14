from pathlib import Path
import asyncio
import tempfile
import os

from app.services.opts import CompileOptions, validate_options, build_args
from app.core.config import TMP_ROOT, NSJAIL_CFG

# limit concurrent executions
semaphore = asyncio.Semaphore(4)


async def execute(file_bytes: bytes, opts: CompileOptions) -> dict:
    validate_options(opts)

    async with semaphore:
        with tempfile.TemporaryDirectory(dir=TMP_ROOT) as tmpdir:
            tmpdir_path = Path(tmpdir)

            # write input file
            input_path = tmpdir_path / "input.rnr"
            input_path.write_bytes(file_bytes)

            # output file
            asm_path = tmpdir_path / "out.asm"

            # link binary into jail
            os.link(TMP_ROOT / "rustpiler", tmpdir_path / "rustpiler")

            # build args using jail paths
            cli_args = build_args("/input.rnr", opts)

            if opts.asm:
                cli_args += ["--asm", "/out.asm"]

            cmd = [
                "nsjail",
                "--really_quiet",
                "--log",
                "tmp/nsjail.log",
                "--config",
                str(NSJAIL_CFG),
                "--chroot",
                tmpdir,
                "--",
                "/rustpiler",
                *cli_args,
            ]

            # print(" ".join(cmd))  # debug

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

                rc = process.returncode
                stderr_text = stderr.decode()
                if rc is None:
                    raise RuntimeError("Process did not terminate properly")
                if rc < 0:
                    signal = -rc

                    if signal == 6:
                        error = "Stack overflow"
                    elif signal == 9:
                        error = "Execution killed (timeout or limit)"
                    elif signal == 11:
                        error = "Segmentation fault"
                    else:
                        error = f"Process terminated by signal {signal}"
                else:
                    error = stderr_text

            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return {
                    "success": False,
                    "output": "",
                    "error": "Execution timed out",
                    "assembly": None,
                    "returncode": 1,
                }

            asm_content = None
            if opts.asm and asm_path.exists():
                asm_content = asm_path.read_text()

            return {
                "success": process.returncode == 0,
                "output": stdout.decode(),
                "error": error if rc != 0 else "",
                "assembly": asm_content,
                "returncode": rc,
            }
