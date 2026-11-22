import "server-only";

import { serverApi } from "@/lib/api/server";
import type { components } from "@/lib/api/schema";

export type Trip = components["schemas"]["Trip"];
export type SampleWidget = components["schemas"]["SampleWidget"];

// The shared samples (schemas/samples) are read through the API (GET /v1/sample/trip and
// /v1/sample/widgets): the backend owns the files. They are samples, never real figures. Reading
// the API needs the request, so the pages that use these render at request time.
export { SAMPLE_TRIP_ID } from "@/lib/links";

// The sample's own "today": ages in the samples are measured from here, and a shared sample is "as
// of" this day. Source: schemas/samples/README.md ("today" is 18 Nov 2026; an age of "3 days old"
// is a captured_at of 15 Nov 2026 at 09:00 UTC) and docs/design/boards/sample-data.md.
export const SAMPLE_TODAY = new Date("2026-11-18T09:00:00Z");

export async function getSampleTrip(): Promise<Trip> {
  const { data } = await (await serverApi()).GET("/v1/sample/trip");
  if (!data) throw new Error("The sample trip could not be read from the API.");
  return data;
}

// One entry per kind and state, in kind then state order (the API sorts them).
export async function getSampleWidgets(): Promise<SampleWidget[]> {
  const { data } = await (await serverApi()).GET("/v1/sample/widgets");
  if (!data) throw new Error("The sample widgets could not be read from the API.");
  return data;
}
