from pydantic import BaseModel, ConfigDict


class CompileOptions(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type_check: bool = False
    virtual_machine: bool = False
    code_gen: bool = False
    run: bool = False

    ast: bool = False
    asm: bool = False


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
