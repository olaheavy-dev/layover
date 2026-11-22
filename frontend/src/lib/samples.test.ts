// @vitest-environment node
import { getSampleTrip, getSampleWidgets } from "./samples";

describe("the sample loaders", () => {
  it("read the sample trip, marked as a sample", async () => {
    const trip = await getSampleTrip();
    expect(trip.is_sample).toBe(true);
    expect(trip.name).toBeTruthy();
  });

  it("read every widget sample, one per file, in kind then state order", async () => {
    const widgets = await getSampleWidgets();
    const keys = widgets.map((w) => `${w.kind}/${w.state}`);
    expect(keys).toContain("money/filled");
    expect(keys).toContain("not_known/not_known");
    expect(keys).toEqual([...keys].sort());
    expect(widgets.every((w) => w.is_sample)).toBe(true);
  });
});
