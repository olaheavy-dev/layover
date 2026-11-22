import "server-only";

import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

import type { components } from "@/lib/api/schema";

export type Trip = components["schemas"]["Trip"];
export type SampleWidget = components["schemas"]["SampleWidget"];

// The shared sample files (schemas/samples). They are samples, never real figures. The folder is
// `SAMPLES_DIR`, or `../schemas/samples` from the frontend folder, as the backend does.
// Note: the frontend's Docker build context is `frontend/` only, so a container needs the folder
// copied in and `SAMPLES_DIR` set (see the task report).
function samplesDir(): string {
  return process.env.SAMPLES_DIR ?? path.resolve(process.cwd(), "..", "schemas", "samples");
}

export async function getSampleTrip(): Promise<Trip> {
  const text = await readFile(path.join(samplesDir(), "trip", "sample-lisbon.json"), "utf8");
  return JSON.parse(text) as Trip;
}

// One entry per file in widgets/<kind>/<state>.json, sorted by kind then state. The file name is the
// state the sample shows, which can differ from the widget's own `state` field.
export async function getSampleWidgets(): Promise<SampleWidget[]> {
  const root = path.join(samplesDir(), "widgets");
  const kinds = (await readdir(root, { withFileTypes: true }))
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
  const samples: SampleWidget[] = [];
  for (const kind of kinds) {
    const files = (await readdir(path.join(root, kind))).filter((f) => f.endsWith(".json")).sort();
    for (const file of files) {
      const text = await readFile(path.join(root, kind, file), "utf8");
      samples.push({
        is_sample: true,
        kind,
        state: file.slice(0, -".json".length),
        widget: JSON.parse(text) as SampleWidget["widget"],
      });
    }
  }
  return samples;
}
