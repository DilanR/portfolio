import { useRustpiler } from "./hooks/useRustpiler";
import { CodeEditor } from "./components/CodeEditor";
import { OptionsPanel } from "./components/OptionsPanel";
import { RunButton } from "./components/RunButton";
import { OutputPanel } from "./components/OutputPanel";

export function RustpilerPage() {
  const rustpiler = useRustpiler();

  return (
    <div style={{ padding: 20 }}>
      <h2>RnR Compiler</h2>

      <CodeEditor
        code={rustpiler.code}
        setCode={rustpiler.setCode}
      />

      <OptionsPanel
        options={rustpiler.options}
        toggle={rustpiler.toggleOption}
      />

      <RunButton
        loading={rustpiler.loading}
        onRun={rustpiler.run}
      />

      <OutputPanel
        output={rustpiler.output}
        assembly={rustpiler.assembly}
        error={rustpiler.error}
      />
    </div>
  );
}
