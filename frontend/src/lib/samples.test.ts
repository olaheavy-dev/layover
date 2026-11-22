// @vitest-environment node
import * as fs from "node:fs/promises";

import { getSampleTrip, getSampleWidgets } from "./samples";

const GET = vi.fn();
vi.mock("@/lib/api/server", () => ({ serverApi: async () => ({ GET }) }));
vi.mock("node:fs/promises");

const TRIP = { is_sample: true, name: "Lisbon, May" };
const WIDGETS = [{ is_sample: true, kind: "money", state: "filled", widget: {} }];

describe("the sample loaders", () => {
  beforeEach(() => GET.mockReset());

  it("read the sample trip from GET /v1/sample/trip, and not from disk", async () => {
    GET.mockResolvedValue({ data: TRIP });
    await expect(getSampleTrip()).resolves.toBe(TRIP);
    expect(GET).toHaveBeenCalledWith("/v1/sample/trip");
    expect(fs.readFile).not.toHaveBeenCalled();
    expect(fs.readdir).not.toHaveBeenCalled();
  });

  it("read the widget samples from GET /v1/sample/widgets, and not from disk", async () => {
    GET.mockResolvedValue({ data: WIDGETS });
    await expect(getSampleWidgets()).resolves.toBe(WIDGETS);
    expect(GET).toHaveBeenCalledWith("/v1/sample/widgets");
    expect(fs.readFile).not.toHaveBeenCalled();
    expect(fs.readdir).not.toHaveBeenCalled();
  });

  it("throw when the API answers with an error, so the error page shows, never a blank canvas", async () => {
    GET.mockResolvedValue({ error: { status: 503 }, response: { status: 503 } });
    await expect(getSampleTrip()).rejects.toThrow(/sample trip/i);
    await expect(getSampleWidgets()).rejects.toThrow(/sample widgets/i);
  });
});
