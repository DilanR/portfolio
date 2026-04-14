import type { CompileOptions } from "../types";

type Props = {
  options: CompileOptions;
  toggle: (key: keyof CompileOptions) => void;
};

export function OptionsPanel({ options, toggle }: Props) {
  return (
    <div style={{ marginTop: 10 }}>
      {Object.entries(options).map(([key, value]) => (
        <label key={key} style={{ marginRight: 10 }}>
          <input
            type="checkbox"
            checked={value}
            onChange={() => toggle(key as keyof CompileOptions)}
          />
          {key}
        </label>
      ))}
    </div>
  );
}
