import { useState } from "react";

type Options = {
  type_check: boolean;
  virtual_machine: boolean;
  code_gen: boolean;
  run: boolean;
  asm: boolean;
};
export default function App() {
  const [code, setCode] = useState(`
fn main() -> i32 {
  let x mut = 1;
  x = x + 1;
  x
}`);
  const [output, setOutput] = useState("");
  const [assembly, setAssembly] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [options, setOptions] = useState<Options>({
    type_check: false,
    virtual_machine: true,
    code_gen: false,
    run: false,
    asm: false,
  });

  const handleCheckbox = (key: keyof Options) => {
    setOptions((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const runCode = async () => {
    setLoading(true);
    setOutput("");
    setAssembly("");
    setError("");

    try {
      const file = new File([code], "input.rnr");

      const formData = new FormData();
      formData.append("file", file);
      formData.append("options", JSON.stringify(options));

      const res = await fetch("http://localhost:5000/compile", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Request failed");
      } else {
        setOutput(data.output);
        setAssembly(data.assembly);
        setError(data.error);
      }
    } catch (err) {
      setError("Network error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: "sans-serif" }}>
      <h2>RnR Compiler</h2>

      {/* Code editor */}
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        rows={12}
        style={{ width: "100%", fontFamily: "monospace" }}
      />

      {/* Options */}

      <div style={{ marginTop: 10 }}>
        <label style={{ marginLeft: 10 }}>
          <input
            type="checkbox"
            checked={options.asm}
            onChange={() => handleCheckbox("asm")}
          />
          Output Assembly (--asm)
        </label>
        <label>
          <input
            type="checkbox"
            checked={options.type_check}
            onChange={() => handleCheckbox("type_check")}
          />
          Type Check (-t)
        </label>

        <label style={{ marginLeft: 10 }}>
          <input
            type="checkbox"
            checked={options.virtual_machine}
            onChange={() => handleCheckbox("virtual_machine")}
          />
          Tree VM (-v)
        </label>

        <label style={{ marginLeft: 10 }}>
          <input
            type="checkbox"
            checked={options.code_gen}
            onChange={() => handleCheckbox("code_gen")}
          />
          Code Gen (-c)
        </label>

        <label style={{ marginLeft: 10 }}>
          <input
            type="checkbox"
            checked={options.run}
            onChange={() => handleCheckbox("run")}
          />
          Run MIPS (-r)
        </label>
      </div>

      {/* Run button */}
      <div style={{ marginTop: 10 }}>
        <button onClick={runCode} disabled={loading}>
          {loading ? "Running..." : "Run"}
        </button>
      </div>

      {/* Output */}
      <div style={{ marginTop: 20 }}>
        <h3>Output</h3>
        <pre style={{ background: "#111", color: "#0f0", padding: 10 }}>
          {output}
        </pre>
        {assembly && (
          <>
            <h3>Assembly</h3>
            <pre style={{ background: "#222", color: "#0ff", padding: 10 }}>
              {assembly}
            </pre>
          </>
        )}
        {error && (
          <>
            <h3>Error</h3>
            <pre style={{ background: "#300", color: "#f55", padding: 10 }}>
              {error}
            </pre>
          </>
        )}
      </div>
    </div>
  );
}
