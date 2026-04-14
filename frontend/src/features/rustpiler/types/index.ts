export type CompileOptions = {
  type_check: boolean;
  virtual_machine: boolean;
  code_gen: boolean;
  run: boolean;
  asm: boolean;
};

export type CompileResponse = {
  output: string;
  assembly: string;
  error: string;
};
