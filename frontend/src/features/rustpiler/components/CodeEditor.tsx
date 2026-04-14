type Props = {
  code: string;
  setCode: (v: string) => void;
};

export function CodeEditor({ code, setCode }: Props) {
  return (
    <textarea
      value={code}
      onChange={(e) => setCode(e.target.value)}
      rows={12}
      style={{ width: "100%", fontFamily: "monospace" }}
    />
  );
}
