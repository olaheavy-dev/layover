export type SectionId = "brief" | "compare" | "place" | "stay" | "days" | "booking";

// The journey order (information architecture, "Navigation model").
const ORDER: SectionId[] = ["brief", "compare", "place", "stay", "days", "booking"];

const LABELS: Record<Exclude<SectionId, "place">, string> = {
  brief: "Brief",
  compare: "Compare",
  stay: "Stay",
  days: "Days",
  booking: "Booking",
};

// Jumps between the canvas sections. `sections` is the sections that have content; the index lists
// only those, always in journey order. The chosen place is named by `place`. The current section is
// bold and underlined and has aria-current, so colour is never the only cue.
export function SectionIndex({
  sections,
  place,
  current,
}: {
  sections: SectionId[];
  place?: string;
  current?: SectionId;
}) {
  const shown = ORDER.filter((id) => sections.includes(id));
  if (shown.length === 0) return null;
  return (
    <nav
      aria-label="Sections of the trip"
      className="bg-bg-primary border-border-primary sticky top-0 z-10 overflow-x-auto border-b"
    >
      <ul className="flex gap-1 px-4">
        {shown.map((id) => {
          const isCurrent = id === current;
          return (
            <li key={id} className="shrink-0">
              <a
                href={`#${id}`}
                aria-current={isCurrent ? "true" : undefined}
                className={`inline-flex min-h-11 items-center px-2 text-sm ${
                  isCurrent ? "text-text-primary font-bold underline" : "text-text-link"
                }`}
              >
                {id === "place" ? (place ?? "Place") : LABELS[id]}
              </a>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
