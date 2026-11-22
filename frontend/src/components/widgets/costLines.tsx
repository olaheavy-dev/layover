import type { components } from "@/lib/api/schema";

import { monthYear } from "./format";

export type CostLine = components["schemas"]["CostLine"];
export type Label = components["schemas"]["SourceLabel"];
export type Part = "flights" | "stay" | "meals";

// A line the sources could not answer just now is "Unavailable"; one they have no answer for is
// "Not known". The contract marks both with `missing`; the widget's source labels say which: the
// unavailable label names the provider that failed (fares: Travelpayouts; stay and meals:
// Wikivoyage).
const PROVIDER: Record<Part, string> = {
  flights: "Travelpayouts",
  stay: "Wikivoyage",
  meals: "Wikivoyage",
};

export function unavailableLabel(part: Part, sources: Label[]): Label | undefined {
  return sources.find((s) => s.status === "unavailable" && s.source.startsWith(PROVIDER[part]));
}

// "from 6 Wikivoyage listings", using only what the line carries ("" when it carries no source).
export function listingSource(line: CostLine): string {
  const provider = line.source?.source.split(",")[0] ?? "";
  if (!provider) return "";
  return line.listing_count != null
    ? `from ${line.listing_count} ${provider} listings`
    : `from ${provider}`;
}

// "March 2026", from the line's `page_edited`.
export function pageEdited(line: CostLine): string | null {
  return line.page_edited ? monthYear(line.page_edited) : null;
}
