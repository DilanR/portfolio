type Props = {
  output: string;
  assembly: string;
  error: string;
};

export function OutputPanel({ output, assembly, error }: Props) {
  return (
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
  );
}
