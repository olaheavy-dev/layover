import { render, screen, within } from "@testing-library/react";

import { FareList } from "./FareList";
import { nth, sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

const TITLE = "Lowest cached fares from Bristol";
const NOTE =
  "Lowest fare first. A cached fare can have changed since. No comparison with usual prices is made.";

// Source: schemas/samples/widgets/fare_list and the "Lowest cached fares" section of
// docs/design/boards/screens/widgets-proposed.html. Test time is 18 Nov 2026 09:00 UTC. Ages are
// whole days: Faro captured 15 Nov = 3 days; Valencia 17 Nov = 1 day; Lisbon 16 Nov = 2 days;
// Valletta 13 Nov = 5 days. Prices are amount_minor / 100: 5900 = £59, 6400 = £64, 7100 = £71,
// 9800 = £98.
describe("FareList", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("fare_list")).sort()).toEqual([
      "empty",
      "error",
      "filled",
      "loading",
      "not_known",
      "one_place_not_known",
    ]);
  });

  it("filled: rows in the order given, each with its price, wording, own age and live-price link", async () => {
    render(<FareList widget={await sampleOf("fare_list", "filled")} />);
    expect(screen.getByRole("heading", { name: TITLE })).toBeInTheDocument();
    expect(screen.getByText("From Bristol (BRS), leaving in March 2027")).toBeInTheDocument();
    const rows = screen.getAllByRole("listitem");
    expect(rows).toHaveLength(4);
    const expected = [
      ["Faro", "£59", "Cached, 3 days old"],
      ["Valencia", "£64", "Cached, 1 day old"],
      ["Lisbon", "£71", "Cached, 2 days old"],
      ["Valletta", "£98", "Cached, 5 days old"],
    ];
    expected.forEach(([place, price, age], index) => {
      const row = nth(rows, index);
      expect(within(row).getByText(place as string)).toBeInTheDocument();
      expect(within(row).getByText(price as string)).toBeInTheDocument();
      expect(within(row).getByText("return, per person")).toBeInTheDocument();
      expect(within(row).getByText(age as string)).toBeInTheDocument();
      const link = within(row).getByRole("link", { name: `Check live price for ${place}` });
      expect(link).toHaveAttribute("href", "https://www.aviasales.com/");
    });
    expect(screen.getByText(NOTE)).toBeInTheDocument();
    expect(screen.queryByText(/cheap|usual price is/i)).toBeNull();
  });

  it("one_place_not_known: that place says Not known with its own reason and keeps the link", async () => {
    render(<FareList widget={await sampleOf("fare_list", "one_place_not_known")} />);
    const rows = screen.getAllByRole("listitem");
    expect(rows).toHaveLength(4);
    const naples = nth(rows, 3);
    expect(within(naples).getByText("Naples")).toBeInTheDocument();
    expect(within(naples).getByText("Not known")).toBeInTheDocument();
    expect(
      within(naples).getByText("No cached fare from Bristol in March 2027."),
    ).toBeInTheDocument();
    expect(within(naples).queryByText(/£/)).toBeNull();
    expect(within(naples).queryByText("return, per person")).toBeNull();
    expect(
      within(naples).getByRole("link", { name: "Check live price for Naples" }),
    ).toBeInTheDocument();
    // The others keep their price.
    expect(within(nth(rows, 0)).getByText("£59")).toBeInTheDocument();
  });

  it("loading: a busy status", async () => {
    render(<FareList widget={await sampleOf("fare_list", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent(`Loading ${TITLE}`);
  });

  it("error: Unavailable, what failed, the search link, Try again, and no fare", async () => {
    const { container } = render(<FareList widget={await sampleOf("fare_list", "error")} />);
    const alert = screen.getByRole("alert");
    expect(within(alert).getByText("Unavailable")).toBeInTheDocument();
    expect(
      within(alert).getByText(
        "Layover could not check fares from Bristol just now. No fare is shown.",
      ),
    ).toBeInTheDocument();
    expect(
      within(alert).getByRole("link", { name: "Search flights on Aviasales" }),
    ).toHaveAttribute("href", "https://www.aviasales.com/");
    expect(within(alert).getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(container.textContent).not.toMatch(/£/);
  });

  it("not_known: the contract's missing text, the board's note, the search link and Change month", async () => {
    render(<FareList widget={await sampleOf("fare_list", "not_known")} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText("Travelpayouts has no cached fares from Bristol (BRS) in March 2027"),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Layover looked at fares to any place and found none. A different month or airport may have some.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Search flights on Aviasales" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Change month" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("empty: the same looked-and-found-none state, with Not known and no price", async () => {
    const { container } = render(<FareList widget={await sampleOf("fare_list", "empty")} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText(/found none/)).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(container.textContent).not.toMatch(/£/);
  });

  it("a search link that is not http or https is not made a link", async () => {
    const base = await sampleOf("fare_list", "filled");
    render(
      <FareList
        widget={{
          ...base,
          rows: [{ ...nth(base.rows!, 0), search_url: "javascript:alert(1)" }],
        }}
      />,
    );
    expect(screen.queryByRole("link")).toBeNull();
  });

  it("a fare with no label shows Source: Not known beside it", async () => {
    const base = await sampleOf("fare_list", "filled");
    const row = nth(base.rows!, 0);
    const fare = { ...row.fare!, source: undefined } as unknown as typeof row.fare;
    render(<FareList widget={{ ...base, rows: [{ ...row, fare }] }} />);
    expect(
      within(nth(screen.getAllByRole("listitem"), 0)).getByText("Source: Not known"),
    ).toBeInTheDocument();
  });
});
