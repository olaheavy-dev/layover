import { render, screen } from "@testing-library/react";

import { PlaceIntro } from "./PlaceIntro";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/place_intro (Lisbon; Wikivoyage page cached 14 Nov 2026, so
// 4 days old at TEST_NOW, 18 Nov 2026).
describe("PlaceIntro", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("place_intro")).sort()).toEqual([
      "error",
      "fallback",
      "filled",
      "loading",
      "not_known",
    ]);
  });

  it("filled: the heading, the hero line, both paragraphs and the Wikivoyage label", async () => {
    render(<PlaceIntro widget={await sampleOf("place_intro", "filled")} />);
    expect(screen.getByRole("heading", { name: "About Lisbon" })).toBeInTheDocument();
    expect(screen.getByText("Portugal’s capital, on the river Tagus.")).toBeInTheDocument();
    expect(
      screen.getByText("Lisbon is the capital of Portugal, on the river Tagus."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Alfama is one of its old quarters, above the river."),
    ).toBeInTheDocument();
    expect(screen.getByText("Cached, 4 days old")).toBeInTheDocument();
    expect(screen.getByText("Wikivoyage, Lisbon")).toBeInTheDocument();
    expect(screen.queryByText(/so Layover used Wikipedia/)).not.toBeInTheDocument();
  });

  it("fallback: says Wikipedia was used and shows the Fallback label", async () => {
    render(<PlaceIntro widget={await sampleOf("place_intro", "fallback")} />);
    expect(
      screen.getByText("Wikivoyage has no guide for this place, so Layover used Wikipedia."),
    ).toBeInTheDocument();
    expect(screen.getByText("Fallback")).toBeInTheDocument();
    expect(screen.getByText("Wikipedia, Lisbon")).toBeInTheDocument();
  });

  it("filled with no paragraphs says Not known, never an empty intro", async () => {
    const widget = {
      ...(await sampleOf("place_intro", "filled")),
      paragraphs: [],
      hero_line: null,
    };
    render(<PlaceIntro widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
  });

  it("not_known: the reason and both sources as Unavailable", async () => {
    render(<PlaceIntro widget={await sampleOf("place_intro", "not_known")} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText(
        "an introduction: neither Wikivoyage nor Wikipedia has a page for this place",
      ),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Unavailable")).toHaveLength(2);
    expect(screen.getByText("Wikivoyage, Lisbon")).toBeInTheDocument();
    expect(screen.getByText("Wikipedia, Lisbon")).toBeInTheDocument();
  });

  it("loading: a busy status", async () => {
    render(<PlaceIntro widget={await sampleOf("place_intro", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading About Lisbon");
  });

  it("error: what could not be read, no introduction, Try again", async () => {
    const { container } = render(<PlaceIntro widget={await sampleOf("place_intro", "error")} />);
    expect(
      screen.getByText(
        "Layover could not read the introduction just now. No introduction is shown.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/capital/);
  });
});
