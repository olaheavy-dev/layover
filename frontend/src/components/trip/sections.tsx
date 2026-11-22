import type { SectionId } from "@/components/layout/SectionIndex";
import type { Trip } from "@/lib/samples";

// The place's facts, in the order of the information architecture ("Working trip", item 3): cost
// and fares first because the brief has a budget, then FCDO advice because it can stop a trip.
const PLACE_ORDER = [
  "fare_card",
  "cost_estimate",
  "advice_card",
  "climate_chart",
  "money",
  "sea_conditions",
  "daylight",
  "place_intro",
  "map",
  "public_holidays",
  "time_difference",
];

export function placeWidgetsInOrder(trip: Trip): Trip["place_widgets"] {
  const rank = (kind: string) => {
    const at = PLACE_ORDER.indexOf(kind);
    return at === -1 ? PLACE_ORDER.length : at;
  };
  // Sorting keeps the sample's own order for kinds with the same rank.
  return [...trip.place_widgets].sort((a, b) => rank(a.kind) - rank(b.kind));
}

// A shared trip shows the stay only once the traveller has decided: chosen a hotel or skipped it.
export function stayShown(trip: Trip): boolean {
  return trip.stay != null && trip.stay.selection !== "undecided";
}

// A section is in the index only when it has content (information architecture, "Navigation model").
export function sectionsOf(trip: Trip, { shared = false }: { shared?: boolean } = {}): SectionId[] {
  const sections: SectionId[] = [];
  if (trip.brief) sections.push("brief");
  if (trip.comparison) sections.push("compare");
  if (trip.chosen_place && trip.place_widgets.length > 0) sections.push("place");
  if (trip.stay && (!shared || stayShown(trip))) sections.push("stay");
  if (trip.days.length > 0) sections.push("days");
  // A shared trip is a copy of the plan, not of the sandbox order.
  if (trip.booking && !shared) sections.push("booking");
  return sections;
}

export const SECTION_TITLES: Record<Exclude<SectionId, "place">, string> = {
  brief: "Brief",
  compare: "Compare",
  stay: "Stay",
  days: "Days",
  booking: "Booking",
};

export function Section({
  id,
  title,
  kicker,
  children,
}: {
  id: SectionId;
  title: string;
  kicker?: string;
  children: React.ReactNode;
}) {
  return (
    <section id={id} aria-labelledby={`${id}-title`} className="flex scroll-mt-16 flex-col gap-3">
      {kicker ? (
        <p className="text-text-secondary text-xs font-medium tracking-wide uppercase">{kicker}</p>
      ) : null}
      <h2 id={`${id}-title`} className="font-display text-2xl font-semibold">
        {title}
      </h2>
      {children}
    </section>
  );
}
