import { render, screen, within } from "@testing-library/react";

import { TimeDifference } from "./TimeDifference";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/time_difference and the "Time in ..." section of
// docs/design/boards/screens/widgets-proposed.html. Offsets are shown as the contract gives them:
// 60 min = UTC+1, 120 min = UTC+2, a difference of 60 min = 1 hour.
describe("TimeDifference", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("time_difference")).sort()).toEqual([
      "error",
      "filled",
      "hours_ahead",
      "loading",
      "not_known",
      "same_time",
    ]);
  });

  it("same_time: the phrase, the date note and both offsets", async () => {
    const { container } = render(
      <TimeDifference widget={await sampleOf("time_difference", "same_time")} />,
    );
    expect(screen.getByRole("heading", { name: "Time in Lisbon" })).toBeInTheDocument();
    expect(screen.getByText("Same time as the UK")).toBeInTheDocument();
    expect(
      screen.getByText("On 15 May, the middle of the month: your dates are not set yet"),
    ).toBeInTheDocument();
    expect(screen.getByText("UK").nextSibling).toHaveTextContent("UTC+1");
    expect(screen.getByText("Lisbon", { selector: "dt" }).nextSibling).toHaveTextContent("UTC+1");
    const footer = container.querySelector("footer") as HTMLElement;
    expect(within(footer).getByText("Cached, data released 1 Nov 2026")).toBeInTheDocument();
    expect(within(footer).getByText("IANA time zone database")).toBeInTheDocument();
  });

  it("filled: the same figures as same_time", async () => {
    render(<TimeDifference widget={await sampleOf("time_difference", "filled")} />);
    expect(screen.getByText("Same time as the UK")).toBeInTheDocument();
  });

  it("hours_ahead: one hour ahead, naming the place and the date, with UTC+1 and UTC+2", async () => {
    render(<TimeDifference widget={await sampleOf("time_difference", "hours_ahead")} />);
    expect(screen.getByRole("heading", { name: "Time in Valletta" })).toBeInTheDocument();
    expect(screen.getByText("1 hour ahead")).toBeInTheDocument();
    expect(
      screen.getByText("Valletta is ahead of the UK on 15 May, the middle of the month"),
    ).toBeInTheDocument();
    expect(screen.getByText("UK").nextSibling).toHaveTextContent("UTC+1");
    expect(screen.getByText("Valletta", { selector: "dt" }).nextSibling).toHaveTextContent("UTC+2");
  });

  it("behind and part-hour differences are said in words", async () => {
    const base = await sampleOf("time_difference", "hours_ahead");
    const { rerender } = render(
      <TimeDifference widget={{ ...base, difference_minutes: -330, place_offset_minutes: -270 }} />,
    );
    expect(screen.getByText("5 hours 30 minutes behind")).toBeInTheDocument();
    expect(screen.getByText(/Valletta is behind the UK on 15 May/)).toBeInTheDocument();
    rerender(<TimeDifference widget={{ ...base, difference_minutes: 120 }} />);
    expect(screen.getByText("2 hours ahead")).toBeInTheDocument();
  });

  it("set dates drop the middle-of-the-month wording", async () => {
    const base = await sampleOf("time_difference", "hours_ahead");
    render(<TimeDifference widget={{ ...base, dates_set: true }} />);
    expect(screen.getByText("Valletta is ahead of the UK on 15 May")).toBeInTheDocument();
    expect(screen.queryByText(/middle of the month/)).toBeNull();
  });

  it("loading: a busy status", async () => {
    render(<TimeDifference widget={await sampleOf("time_difference", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Time in Lisbon");
  });

  it("error: Unavailable, what failed, Try again, and no difference", async () => {
    render(<TimeDifference widget={await sampleOf("time_difference", "error")} />);
    const alert = screen.getByRole("alert");
    expect(within(alert).getByText("Unavailable")).toBeInTheDocument();
    expect(
      within(alert).getByText(
        "Layover could not read the time zone data just now. No time difference is shown.",
      ),
    ).toBeInTheDocument();
    expect(within(alert).getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(screen.queryByText(/ahead|behind|Same time/)).toBeNull();
  });

  it("not_known: Not known with the contract's missing text", async () => {
    render(<TimeDifference widget={await sampleOf("time_difference", "not_known")} />);
    expect(screen.getByRole("heading", { name: "Time in this place" })).toBeInTheDocument();
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText("a time zone for this place")).toBeInTheDocument();
    expect(screen.queryByText(/ahead|behind|Same time/)).toBeNull();
  });

  it("filled with no difference is Not known, never 'same time'", async () => {
    const base = await sampleOf("time_difference", "filled");
    render(<TimeDifference widget={{ ...base, difference_minutes: null }} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.queryByText("Same time as the UK")).toBeNull();
  });

  it("a missing offset says Not known in its own row", async () => {
    const base = await sampleOf("time_difference", "hours_ahead");
    render(<TimeDifference widget={{ ...base, place_offset_minutes: null }} />);
    const row = screen.getByText("Valletta", { selector: "dt" }).nextSibling as HTMLElement;
    expect(row).toHaveTextContent("Not known");
    expect(screen.getByText("1 hour ahead")).toBeInTheDocument();
  });
});
