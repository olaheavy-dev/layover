import { render, screen, within } from "@testing-library/react";

import { Daylight } from "./Daylight";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/daylight (Lisbon, 15 May 2027, dates not set, sunrise 06:20:00,
// sunset 20:40:00, 860 minutes).
// Working: 860 minutes = 14 x 60 + 20, so "14 h 20 min".
describe("Daylight", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("daylight")).sort()).toEqual([
      "error",
      "filled",
      "loading",
      "not_known",
    ]);
  });

  it("filled: the day, sunrise, sunset, day length, credit link and source", async () => {
    render(<Daylight widget={await sampleOf("daylight", "filled")} />);
    expect(screen.getByRole("heading", { name: "Daylight" })).toBeInTheDocument();
    expect(screen.getByText("15 May: your dates are not set yet")).toBeInTheDocument();
    const value = (term: string) => {
      const dt = screen.getByText(term, { selector: "dt" });
      return within(dt.parentElement as HTMLElement).getByText((_, el) => el?.tagName === "DD");
    };
    expect(value("Sunrise")).toHaveTextContent("06:20");
    expect(value("Sunset")).toHaveTextContent("20:40");
    expect(value("Day length")).toHaveTextContent("14 h 20 min");
    expect(screen.getByRole("link", { name: /sunrise-sunset\.org/ })).toHaveAttribute(
      "href",
      "https://sunrise-sunset.org/",
    );
    expect(screen.getByText("Live")).toBeInTheDocument();
  });

  it("when the dates are set the day shows without the not-set line", async () => {
    const widget = { ...(await sampleOf("daylight", "filled")), dates_set: true };
    render(<Daylight widget={widget} />);
    expect(screen.getByText("15 May")).toBeInTheDocument();
    expect(screen.queryByText(/not set yet/)).not.toBeInTheDocument();
  });

  it("a missing sunset is Not known in its own row, never a made-up time", async () => {
    const widget = { ...(await sampleOf("daylight", "filled")), sunset: null };
    render(<Daylight widget={widget} />);
    const dt = screen.getByText("Sunset", { selector: "dt" });
    expect(within(dt.parentElement as HTMLElement).getByText("Not known")).toBeInTheDocument();
    expect(screen.queryByText("20:40")).not.toBeInTheDocument();
  });

  it("not_known: the missing value in words and no times", async () => {
    const { container } = render(<Daylight widget={await sampleOf("daylight", "not_known")} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText("sunrise and sunset times for this place and date"),
    ).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/\d{2}:\d{2}/);
  });

  it("loading: a busy status", async () => {
    render(<Daylight widget={await sampleOf("daylight", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Daylight");
  });

  it("error: what could not be checked, no times, Try again", async () => {
    const { container } = render(<Daylight widget={await sampleOf("daylight", "error")} />);
    expect(
      screen.getByText("Layover could not check sunrise and sunset just now. No times are shown."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/\d{2}:\d{2}/);
  });
});
