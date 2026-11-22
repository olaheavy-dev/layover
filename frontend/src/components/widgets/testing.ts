import { getSampleWidgets, type SampleWidget } from "@/lib/samples";

// Test helper: the sample file for one kind and state, as the shared sample files define it.
export async function sampleOf<K extends SampleWidget["widget"]["kind"]>(
  kind: K,
  state: string,
): Promise<Extract<SampleWidget["widget"], { kind: K }>> {
  const all = await getSampleWidgets();
  const found = all.find((s) => s.kind === kind && s.state === state);
  if (!found) throw new Error(`No sample ${kind}/${state}`);
  return found.widget as Extract<SampleWidget["widget"], { kind: K }>;
}

export async function sampleStates(kind: string): Promise<string[]> {
  return (await getSampleWidgets()).filter((s) => s.kind === kind).map((s) => s.state);
}

// "Today" for the tests: the Lisbon fare was captured 15 Nov 2026 (3 days old) and the Wikivoyage
// page on 14 Nov (4 days old), as the journey board shows.
export const TEST_NOW = new Date("2026-11-18T09:00:00Z");
