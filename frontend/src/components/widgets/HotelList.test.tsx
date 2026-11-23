import { render, screen, within } from "@testing-library/react";

import { HotelList } from "./HotelList";
import { nth, sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

const TITLE = "Where you’re staying";

// Source: schemas/samples/widgets/hotel_list, and the "Where you’re staying" section of
// docs/design/boards/screens/widgets-journey.html. The contract carries no prices, so none is shown.
describe("HotelList", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("hotel_list")).sort()).toEqual([
      "changed",
      "chosen",
      "empty",
      "error",
      "filled",
      "loading",
      "not_known",
      "skipped",
    ]);
  });

  it("filled: rows with area, stars and website as given, Not known where missing, no prices", async () => {
    const { container } = render(<HotelList widget={await sampleOf("hotel_list", "filled")} />);
    expect(screen.getByRole("heading", { name: TITLE })).toBeInTheDocument();
    expect(
      screen.getByText("No prices: Layover’s sources have none.", { exact: false }),
    ).toBeInTheDocument();
    const rows = screen.getAllByRole("listitem");
    expect(rows).toHaveLength(3);
    expect(within(nth(rows, 0)).getByText("Sample Hotel Alfama")).toBeInTheDocument();
    expect(within(nth(rows, 0)).getByText("Alfama")).toBeInTheDocument();
    expect(within(nth(rows, 0)).getByText("4 stars")).toBeInTheDocument();
    // Alfama has no website: that row alone says Not known.
    expect(within(nth(rows, 0)).getByText("Not known")).toBeInTheDocument();
    expect(within(nth(rows, 1)).getAllByText("Not known")).toHaveLength(2);
    expect(within(nth(rows, 2)).getByText("3 stars")).toBeInTheDocument();
    const link = within(nth(rows, 2)).getByRole("link", { name: "sample.example" });
    expect(link).toHaveAttribute("href", "https://sample.example/");
    expect(within(nth(rows, 2)).queryByText("Not known")).toBeNull();
    for (const row of rows) {
      expect(within(row).getByRole("button", { name: "Stay here" })).toBeInTheDocument();
    }
    expect(screen.getByRole("button", { name: "Skip, start from the centre" })).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/[£€$]/);
    expect(
      within(container.querySelector("footer") as HTMLElement).getByText("Live"),
    ).toBeInTheDocument();
    expect(screen.getByText("OpenStreetMap, through Overpass")).toBeInTheDocument();
  });

  it("not_known: the same rows, with Not known for what the source does not tag", async () => {
    render(<HotelList widget={await sampleOf("hotel_list", "not_known")} />);
    const rows = screen.getAllByRole("listitem");
    expect(within(nth(rows, 1)).getAllByText("Not known")).toHaveLength(2);
  });

  it("chosen: a banner, the base marked, the others offer Choose instead", async () => {
    render(<HotelList widget={await sampleOf("hotel_list", "chosen")} />);
    expect(screen.getByText("Days start from Sample Hotel Alfama.")).toBeInTheDocument();
    const rows = screen.getAllByRole("listitem");
    expect(within(nth(rows, 0)).getByText("Your base")).toBeInTheDocument();
    expect(within(nth(rows, 0)).queryByRole("button")).toBeNull();
    expect(
      within(nth(rows, 1)).getByRole("button", { name: "Choose instead" }),
    ).toBeInTheDocument();
    expect(
      within(nth(rows, 2)).getByRole("button", { name: "Choose instead" }),
    ).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Stay here" })).toBeNull();
  });

  it("changed: the banner names the new base and says the days rebuild", async () => {
    render(<HotelList widget={await sampleOf("hotel_list", "changed")} />);
    expect(
      screen.getByText(
        "You changed your base to Sample Hotel Belém. The days are rebuilt from it.",
      ),
    ).toBeInTheDocument();
    const rows = screen.getAllByRole("listitem");
    expect(within(nth(rows, 2)).getByText("Your base")).toBeInTheDocument();
    expect(
      within(nth(rows, 0)).getByRole("button", { name: "Choose instead" }),
    ).toBeInTheDocument();
  });

  it("skipped: says so, offers Choose a hotel, and lists no hotels", async () => {
    render(<HotelList widget={await sampleOf("hotel_list", "skipped")} />);
    expect(
      screen.getByText("You skipped the hotel. Days start from the centre of Lisbon."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Choose a hotel" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("empty: says what was looked for, that days start from the centre, and offers Go to Days", async () => {
    render(<HotelList widget={await sampleOf("hotel_list", "empty")} />);
    expect(
      screen.getByText("No hotels are tagged near Lisbon in OpenStreetMap."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Layover looked for hotels and guesthouses around the centre.", {
        exact: false,
      }),
    ).toBeInTheDocument();
    expect(screen.getByText("Days start from the centre of Lisbon.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Go to Days" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("loading: a busy status", async () => {
    render(<HotelList widget={await sampleOf("hotel_list", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent(`Loading ${TITLE}`);
  });

  it("error: Unavailable, what failed, Try again and Skip, and no hotels", async () => {
    render(<HotelList widget={await sampleOf("hotel_list", "error")} />);
    const alert = screen.getByRole("alert");
    expect(within(alert).getByText("Unavailable")).toBeInTheDocument();
    expect(
      within(alert).getByText("Layover could not read the hotel list from OpenStreetMap just now."),
    ).toBeInTheDocument();
    expect(within(alert).getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(
      within(alert).getByRole("button", { name: "Skip, start from the centre" }),
    ).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("a website that is not http or https is not made a link", async () => {
    const base = await sampleOf("hotel_list", "filled");
    const widget = {
      ...base,
      hotels: [{ ...nth(base.hotels!, 2), website: "javascript:alert(1)" }],
    };
    render(<HotelList widget={widget} />);
    expect(screen.queryByRole("link")).toBeNull();
    // The website cell says Not known: it is never left blank.
    expect(within(nth(screen.getAllByRole("listitem"), 0)).getAllByText("Not known")).toHaveLength(
      1,
    );
    expect(
      within(nth(screen.getAllByRole("listitem"), 0)).getByText("3 stars"),
    ).toBeInTheDocument();
  });

  it("not_known with no hotels shows the contract's missing text, not a claim about tags", async () => {
    const widget = { ...(await sampleOf("hotel_list", "not_known")), hotels: [] };
    render(<HotelList widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText(
        "stars and website for Sample Guesthouse Baixa: OpenStreetMap does not tag them",
      ),
    ).toBeInTheDocument();
    expect(screen.queryByText(/No hotels are tagged/)).toBeNull();
  });

  it("chosen but not in the list: says the name is not known, with no false Skip or base", async () => {
    const sample = await sampleOf("hotel_list", "chosen");
    render(<HotelList widget={{ ...sample, chosen_hotel: "Hotel Not In The List" }} />);
    expect(screen.getByText("A hotel was chosen. Its name is not known.")).toBeInTheDocument();
    expect(screen.queryByText(/or skip/)).toBeNull();
    expect(screen.queryByText("Your base")).toBeNull();
    expect(screen.queryByRole("button", { name: /Skip/ })).toBeNull();
  });
});
