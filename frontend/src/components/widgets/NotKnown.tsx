import { Circle } from "lucide-react";

// The words shown for a value Layover does not have, and the fallback when no reason is given.
export const NOT_KNOWN_TEXT = "Not known";

// Missing data is "Not known": never 0, N/A, TBC or a dash (decision 0011 rule 4). Quiet italic
// text with an empty dot; the words carry the meaning.
export function NotKnown({
  missing,
  reason,
  instead,
}: {
  missing?: string | null;
  reason?: string | null;
  instead?: string | null;
}) {
  return (
    <div className="flex flex-col gap-1 text-sm">
      <p className="text-status-not-known inline-flex items-center gap-1.5 italic">
        <Circle className="size-3" aria-hidden="true" />
        <span>{NOT_KNOWN_TEXT}</span>
      </p>
      {missing ? <p className="text-text-primary">{missing}</p> : null}
      {reason ? <p className="text-text-secondary">{reason}</p> : null}
      {instead ? <p className="text-text-secondary">{instead}</p> : null}
    </div>
  );
}
