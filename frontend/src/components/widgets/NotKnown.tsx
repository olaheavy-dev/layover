import { Circle } from "lucide-react";

// Missing data is "Not known": never 0, N/A, TBC or a dash (decision 0011 rule 4). Quiet italic
// text with an empty dot; the words carry the meaning.
export function NotKnown({
  missing,
  reason,
  instead,
}: {
  missing: string;
  reason?: string | null;
  instead?: string | null;
}) {
  return (
    <div className="flex flex-col gap-1 text-sm">
      <p className="text-status-not-known inline-flex items-center gap-1.5 italic">
        <Circle className="size-3" aria-hidden="true" />
        <span>Not known</span>
      </p>
      <p className="text-text-primary">{missing}</p>
      {reason ? <p className="text-text-secondary">{reason}</p> : null}
      {instead ? <p className="text-text-secondary">{instead}</p> : null}
    </div>
  );
}
