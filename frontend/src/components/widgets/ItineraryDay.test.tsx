import { render, screen, within } from "@testing-library/react";

import { ItineraryDay } from "./ItineraryDay";
import { nth, sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/itinerary_day, and the "Days" section of
// docs/design/boards/screens/widgets-journey.html. Hours are the sample's own: the frontend fills
// none in. Working: the walk was captured 14 Nov 2026 09:00 and "now" is 18 Nov 2026 09:00, so
// it is 4 days old.
describe("ItineraryDay", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("itinerary_day")).sort()).toEqual([
      "empty",
      "error",
      "filled",
      "from_centre",
      "loading",
      "not_known",
      "rebuilt",
    ]);
  });

  it("filled: the base, numbered stops, hours as given and each stop's source", async () => {
    const { container } = render(
      <ItineraryDay widget={await sampleOf("itinerary_day", "filled")} />,
    );
    expect(screen.getByRole("heading", { name: "Day 1" })).toBeInTheDocument();
    expect(screen.getByText("Starts from Sample Hotel Alfama.")).toBeInTheDocument();
    const stops = screen.getAllByRole("listitem");
    expect(stops).toHaveLength(3);
    expect(within(nth(stops, 0)).getByText("Castelo de São Jorge")).toBeInTheDocument();
    expect(within(nth(stops, 0)).getByText("Open 10:00 to 18:00")).toBeInTheDocument();
    expect(within(nth(stops, 1)).getByText("Miradouro de Santa Luzia")).toBeInTheDocument();
    expect(within(nth(stops, 1)).getByText("Opening times: Not known")).toBeInTheDocument();
    expect(within(nth(stops, 1)).queryByText(/Open \d/)).toBeNull();
    expect(within(nth(stops, 2)).getByText("A walk through Alfama")).toBeInTheDocument();
    expect(within(nth(stops, 2)).getByText("Cached, 4 days old")).toBeInTheDocument();
    expect(within(nth(stops, 2)).getByText("Wikivoyage, Lisbon")).toBeInTheDocument();
    expect(within(nth(stops, 2)).queryByText(/Open|Opening/)).toBeNull();
    // The footer carries the widget's own sources.
    const footer = container.querySelector("footer") as HTMLElement;
    expect(within(footer).getByText("OpenStreetMap, through Overpass")).toBeInTheDocument();
    expect(within(footer).getByText("Live")).toBeInTheDocument();
  });

  it("not_known: the stop without hours says so and the other stop keeps its hours", async () => {
    render(<ItineraryDay widget={await sampleOf("itinerary_day", "not_known")} />);
    expect(screen.getByRole("heading", { name: "Day 2" })).toBeInTheDocument();
    const stops = screen.getAllByRole("listitem");
    expect(within(nth(stops, 0)).getByText("Torre de Belém")).toBeInTheDocument();
    expect(within(nth(stops, 0)).getByText("Opening times: Not known")).toBeInTheDocument();
    expect(within(nth(stops, 1)).getByText("Open 10:00 to 17:30")).toBeInTheDocument();
  });

  it("not_known with no stops shows the contract's missing text", async () => {
    const widget = { ...(await sampleOf("itinerary_day", "not_known")), stops: [] };
    render(<ItineraryDay widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText("opening times for Torre de Belém: the source has none"),
    ).toBeInTheDocument();
  });

  it("from_centre: a banner says the days start from the centre", async () => {
    render(<ItineraryDay widget={await sampleOf("itinerary_day", "from_centre")} />);
    expect(screen.getByText("Days start from the centre.")).toBeInTheDocument();
    expect(screen.queryByText(/Starts from/)).toBeNull();
  });

  it("rebuilt: a note names the new hotel", async () => {
    render(<ItineraryDay widget={await sampleOf("itinerary_day", "rebuilt")} />);
    expect(
      screen.getByText("Rebuilt after you changed your hotel to Sample Hotel Belém."),
    ).toBeInTheDocument();
  });

  it("a stop whose hours depend on the day says so and offers Add your dates", async () => {
    const base = await sampleOf("itinerary_day", "filled");
    const widget = {
      ...base,
      stops: [
        {
          ...nth(base.stops!, 0),
          hours_status: "depends_on_day" as const,
          opens: null,
          closes: null,
        },
      ],
    };
    render(<ItineraryDay widget={widget} />);
    expect(
      screen.getByText("Opening times depend on the day. Add your dates to see them."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Add your dates" })).toBeInTheDocument();
    expect(screen.queryByText(/Open \d/)).toBeNull();
  });

  it("a known stop missing a closing time is Not known, never half a range", async () => {
    const base = await sampleOf("itinerary_day", "filled");
    const widget = { ...base, stops: [{ ...nth(base.stops!, 0), closes: null }] };
    render(<ItineraryDay widget={widget} />);
    expect(screen.getByText("Opening times: Not known")).toBeInTheDocument();
    expect(screen.queryByText(/Open \d/)).toBeNull();
  });

  it("a day with a date shows its weekday", async () => {
    const widget = { ...(await sampleOf("itinerary_day", "filled")), day: "2027-05-15" };
    render(<ItineraryDay widget={widget} />);
    expect(
      screen.getByRole("heading", { name: "Day 1, Saturday 15 May 2027" }),
    ).toBeInTheDocument();
  });

  it("empty: says so, leaves it free, offers a wider area, and shows no stops", async () => {
    render(<ItineraryDay widget={await sampleOf("itinerary_day", "empty")} />);
    expect(screen.getByRole("heading", { name: "Day 3" })).toBeInTheDocument();
    expect(screen.getByText("Too few sourced places for the afternoon.")).toBeInTheDocument();
    expect(
      screen.getByText("Layover leaves it free rather than guessing.", { exact: false }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Look in a wider area" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Leave it free" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("loading: a busy status", async () => {
    render(<ItineraryDay widget={await sampleOf("itinerary_day", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Day 1");
  });

  it("error: Unavailable, what failed, Try again, and no stops", async () => {
    render(<ItineraryDay widget={await sampleOf("itinerary_day", "error")} />);
    const alert = screen.getByRole("alert");
    expect(within(alert).getByText("Unavailable")).toBeInTheDocument();
    expect(
      within(alert).getByText(
        "Layover could not read places for Day 2 from OpenStreetMap or Wikivoyage just now.",
      ),
    ).toBeInTheDocument();
    expect(within(alert).getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });
});
