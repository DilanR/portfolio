import type { CompileOptions, CompileResponse } from "../types";

export async function compileCode(
  code: string,
  options: CompileOptions
): Promise<CompileResponse> {
  const file = new File([code], "input.rnr");

  const formData = new FormData();
  formData.append("file", file);
  formData.append("options", JSON.stringify(options));

  const res = await fetch(
    "http://localhost:5000/api/rustpiler/compile",
    {
      method: "POST",
      body: formData,
    }
  );

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || "Request failed");
  }

  return data;
}
