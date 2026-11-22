import { render, screen, within } from "@testing-library/react";

import { PublicHolidays } from "./PublicHolidays";
import { nth, sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

const TITLE = "Public holidays";
const LOCAL_NOTE =
  "Layover looked at the national list for Portugal. Local holidays in one town or region may be missing from it.";

// Source: schemas/samples/widgets/public_holidays and the "Public holidays" section of
// docs/design/boards/screens/widgets-proposed.html. 17 May 2027 is a Monday, so 19 May is a Wednesday.
describe("PublicHolidays", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("public_holidays")).sort()).toEqual([
      "empty",
      "error",
      "filled",
      "loading",
      "not_known",
    ]);
  });

  it("filled: country and month, each holiday with weekday date and name, both notes, its label", async () => {
    const { container } = render(
      <PublicHolidays widget={await sampleOf("public_holidays", "filled")} />,
    );
    expect(screen.getByRole("heading", { name: TITLE })).toBeInTheDocument();
    expect(screen.getByText("Portugal, May 2027")).toBeInTheDocument();
    const rows = screen.getAllByRole("listitem");
    expect(rows).toHaveLength(2);
    expect(within(nth(rows, 0)).getByText("Mon 17 May 2027")).toBeInTheDocument();
    expect(within(nth(rows, 0)).getByText("Sample holiday")).toBeInTheDocument();
    expect(within(nth(rows, 1)).getByText("Wed 19 May 2027")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Some places may close or run fewer services on a public holiday. Check opening times before you go.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByText(LOCAL_NOTE)).toBeInTheDocument();
    const footer = container.querySelector("footer") as HTMLElement;
    expect(within(footer).getByText("Cached, data released 1 Nov 2026")).toBeInTheDocument();
    expect(within(footer).getByText("Python holidays library")).toBeInTheDocument();
  });

  it("loading: a busy status", async () => {
    render(<PublicHolidays widget={await sampleOf("public_holidays", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent(`Loading ${TITLE}`);
  });

  it("error: Unavailable, what failed, that it does not mean none, Try again, no holidays", async () => {
    render(<PublicHolidays widget={await sampleOf("public_holidays", "error")} />);
    const alert = screen.getByRole("alert");
    expect(within(alert).getByText("Unavailable")).toBeInTheDocument();
    expect(
      within(alert).getByText(
        "Layover could not work out the public holidays for Portugal just now. No holidays are shown. That does not mean there are none.",
      ),
    ).toBeInTheDocument();
    expect(within(alert).getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(screen.getByText("Portugal, May 2027")).toBeInTheDocument();
  });

  it("not_known: Not known with the contract's missing text, no holiday claim", async () => {
    render(<PublicHolidays widget={await sampleOf("public_holidays", "not_known")} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText(
        "a holiday list for this place, so Layover cannot say if any fall in May 2027",
      ),
    ).toBeInTheDocument();
    expect(screen.queryByText(/No public holidays/)).toBeNull();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("empty: says none in the month, with the national-list note", async () => {
    render(<PublicHolidays widget={await sampleOf("public_holidays", "empty")} />);
    expect(screen.getByText("No public holidays in May 2027.")).toBeInTheDocument();
    expect(screen.getByText(LOCAL_NOTE)).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("filled with no holidays is Not known, never 'none'", async () => {
    const widget = { ...(await sampleOf("public_holidays", "filled")), holidays: [] };
    render(<PublicHolidays widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.queryByText(/No public holidays/)).toBeNull();
  });

  it("a missing country and month fall back to the place, with no blank", async () => {
    const widget = {
      ...(await sampleOf("public_holidays", "filled")),
      country: null,
      month: null,
      year: null,
    };
    render(<PublicHolidays widget={widget} />);
    expect(screen.getByText("Lisbon")).toBeInTheDocument();
    expect(screen.queryByText(/undefined|null/)).toBeNull();
  });

  it("a filled widget with no source says Source: Not known", async () => {
    const widget = { ...(await sampleOf("public_holidays", "filled")), sources: [] };
    const { container } = render(<PublicHolidays widget={widget} />);
    expect(
      within(container.querySelector("footer") as HTMLElement).getByText("Source: Not known"),
    ).toBeInTheDocument();
  });

  it("empty with no month or year is Not known, never a clean 'none'", async () => {
    const base = await sampleOf("public_holidays", "empty");
    const { container } = render(
      <PublicHolidays widget={{ ...base, month: null, year: null, missing: null }} />,
    );
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText("the public holidays for Portugal")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/No public holidays/);
  });

  it("empty with no month uses the contract's missing text", async () => {
    const base = await sampleOf("public_holidays", "empty");
    render(
      <PublicHolidays widget={{ ...base, month: null, year: null, missing: "a trip month" }} />,
    );
    expect(screen.getByText("a trip month")).toBeInTheDocument();
    expect(screen.queryByText(/No public holidays/)).toBeNull();
  });
});
