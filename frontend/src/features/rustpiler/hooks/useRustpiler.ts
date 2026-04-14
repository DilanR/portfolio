import { useState } from "react";
import { compileCode } from "../api/compile";
import type { CompileOptions } from "../types";

export function useRustpiler() {
  const [code, setCode] = useState(`fn main() -> i32 {
  let mut x = 1;
  x = x + 1;
  x
}`);

  const [output, setOutput] = useState("");
  const [assembly, setAssembly] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [options, setOptions] = useState<CompileOptions>({
    type_check: false,
    virtual_machine: true,
    code_gen: false,
    run: false,
    asm: false,
  });

  const toggleOption = (key: keyof CompileOptions) => {
    setOptions((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const run = async () => {
    setLoading(true);
    setOutput("");
    setAssembly("");
    setError("");

    try {
      const res = await compileCode(code, options);
      setOutput(res.output);
      setAssembly(res.assembly);
      setError(res.error);
    } catch (err: any) {
      setError(err.message || "Network error");
    } finally {
      setLoading(false);
    }
  };

  return {
    code,
    setCode,
    output,
    assembly,
    error,
    loading,
    options,
    toggleOption,
    run,
  };
}
