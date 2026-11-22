import { render, screen, within } from "@testing-library/react";

import { MapWidget } from "./MapWidget";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/map (Lisbon centre and Sample Hotel Alfama).
describe("MapWidget", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("map")).sort()).toEqual([
      "centre_only",
      "error",
      "filled",
      "loading",
    ]);
  });

  it("filled: the centre and the chosen hotel in a list with links", async () => {
    render(<MapWidget widget={await sampleOf("map", "filled")} />);
    expect(screen.getByRole("heading", { name: "Map" })).toBeInTheDocument();
    const items = within(screen.getByRole("list", { name: "Places on the map" })).getAllByRole(
      "listitem",
    );
    expect(items).toHaveLength(2);
    expect(items[0]).toHaveTextContent("Lisbon centre (the place you chose)");
    expect(items[1]).toHaveTextContent("Sample Hotel Alfama (your base)");
    expect(within(items[1] as HTMLElement).getByRole("link")).toHaveAttribute(
      "href",
      "https://www.openstreetmap.org/",
    );
    expect(screen.getByText("Live")).toBeInTheDocument();
  });

  it("centre_only: one place and a note that no hotel or stops exist yet", async () => {
    render(<MapWidget widget={await sampleOf("map", "centre_only")} />);
    const items = within(screen.getByRole("list", { name: "Places on the map" })).getAllByRole(
      "listitem",
    );
    expect(items).toHaveLength(1);
    expect(items[0]).toHaveTextContent("Lisbon centre");
    expect(screen.getByText("No hotel or stops yet.")).toBeInTheDocument();
  });

  it("stops are listed after the hotel", async () => {
    const widget = {
      ...(await sampleOf("map", "filled")),
      stops: [{ name: "Time Out Market", lat: 38.7, lon: -9.14, url: null }],
    };
    render(<MapWidget widget={widget} />);
    const items = within(screen.getByRole("list", { name: "Places on the map" })).getAllByRole(
      "listitem",
    );
    expect(items.map((i) => i.textContent)).toEqual([
      expect.stringContaining("Lisbon centre"),
      expect.stringContaining("Sample Hotel Alfama"),
      "Time Out Market",
    ]);
    expect(within(items[2] as HTMLElement).queryByRole("link")).not.toBeInTheDocument();
  });

  it("error: the map could not load, so the places show as a list and nothing is missing", async () => {
    render(<MapWidget widget={await sampleOf("map", "error")} />);
    expect(
      screen.getByText(
        "The map could not load. The places are listed here instead, so nothing is missing.",
      ),
    ).toBeInTheDocument();
    const items = within(screen.getByRole("list", { name: "Places on the map" })).getAllByRole(
      "listitem",
    );
    expect(items).toHaveLength(2);
    expect(items[1]).toHaveTextContent("Sample Hotel Alfama");
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(within(screen.getByRole("alert")).getByText("Unavailable")).toBeInTheDocument();
  });

  it("loading: a busy status and no places", async () => {
    render(<MapWidget widget={await sampleOf("map", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Map");
    expect(screen.queryByRole("list", { name: "Places on the map" })).not.toBeInTheDocument();
  });

  it("filled with no places at all says Not known", async () => {
    render(<MapWidget widget={{ kind: "map", state: "filled", sources: [] }} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.queryByRole("list", { name: "Places on the map" })).not.toBeInTheDocument();
  });
});
