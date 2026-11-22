import { render, screen, within } from "@testing-library/react";

import { TransportRoute } from "./TransportRoute";
import { nth, sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

const TITLE = "To Heathrow Terminals 2 and 3";
const TFL = "https://tfl.gov.uk/plan-a-journey/";
const CREDIT = "Powered by TfL Open Data";
const OS = "Contains OS data © Crown copyright and database rights 2016";

// Source: schemas/samples/widgets/transport_route and the "To Heathrow" section of
// docs/design/boards/screens/widgets-proposed.html. 15 May 2027 is a Saturday (1 May is a Saturday,
// 14 days earlier). The total of 43 min is the contract's total_minutes, not worked out here.
describe("TransportRoute", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("transport_route")).sort()).toEqual([
      "error",
      "filled",
      "loading",
      "not_known",
    ]);
  });

  it("filled: the total as given, each step with its minutes, the plan line, label and credits", async () => {
    const { container } = render(
      <TransportRoute widget={await sampleOf("transport_route", "filled")} />,
    );
    expect(screen.getByRole("heading", { name: TITLE })).toBeInTheDocument();
    expect(screen.getByText("About 43 min")).toBeInTheDocument();
    expect(screen.getByText("from Paddington station")).toBeInTheDocument();
    const steps = screen.getAllByRole("listitem");
    expect(steps).toHaveLength(3);
    const expected = [
      ["Walk to the platform at Paddington station", "5 min"],
      ["Elizabeth line from Paddington to Heathrow Terminals 2 and 3", "32 min"],
      ["Walk to departures", "6 min"],
    ];
    expected.forEach(([text, minutes], index) => {
      expect(within(nth(steps, index)).getByText(text as string)).toBeInTheDocument();
      expect(within(nth(steps, index)).getByText(minutes as string)).toBeInTheDocument();
    });
    expect(
      screen.getByText(
        "TfL plan for Sat 15 May 2027, the middle of the month: your dates are not set yet, leaving 09:00",
      ),
    ).toBeInTheDocument();
    const footer = container.querySelector("footer") as HTMLElement;
    expect(within(footer).getByText("Live")).toBeInTheDocument();
    expect(within(footer).getByText("TfL Unified API (Journey Planner)")).toBeInTheDocument();
    expect(within(footer).getByText(CREDIT)).toBeInTheDocument();
    expect(within(footer).getByText(OS)).toBeInTheDocument();
  });

  it("filled: a step with no description shows its mode, never a blank", async () => {
    const base = await sampleOf("transport_route", "filled");
    const legs = base.legs!.map((leg, index) =>
      index === 1 ? { ...leg, description: null } : leg,
    );
    render(<TransportRoute widget={{ ...base, legs }} />);
    expect(
      within(nth(screen.getAllByRole("listitem"), 1)).getByText("Elizabeth line"),
    ).toBeInTheDocument();
  });

  it("filled with set dates drops the dates-not-set wording", async () => {
    const base = await sampleOf("transport_route", "filled");
    render(<TransportRoute widget={{ ...base, dates_set: true }} />);
    expect(screen.getByText("TfL plan for Sat 15 May 2027, leaving 09:00")).toBeInTheDocument();
  });

  it("filled with no total says Not known for the total, never 0", async () => {
    const base = await sampleOf("transport_route", "filled");
    const { container } = render(<TransportRoute widget={{ ...base, total_minutes: null }} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.queryByText(/About/)).toBeNull();
    expect(container.textContent).not.toMatch(/About 0/);
  });

  it("loading: a busy status", async () => {
    render(<TransportRoute widget={await sampleOf("transport_route", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent(`Loading ${TITLE}`);
  });

  it("error: Unavailable, what failed, the TfL link, Try again, credits, and no route", async () => {
    const { container } = render(
      <TransportRoute widget={await sampleOf("transport_route", "error")} />,
    );
    const alert = screen.getByRole("alert");
    expect(within(alert).getByText("Unavailable")).toBeInTheDocument();
    expect(
      within(alert).getByText(
        "Layover could not ask TfL for a journey just now. No route or duration is shown.",
      ),
    ).toBeInTheDocument();
    expect(
      within(alert).getByRole("link", { name: "Plan it on the TfL Journey Planner" }),
    ).toHaveAttribute("href", TFL);
    expect(within(alert).getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(screen.queryByText(/About/)).toBeNull();
    expect(
      within(container.querySelector("footer") as HTMLElement).getByText(CREDIT),
    ).toBeInTheDocument();
  });

  it("not_known: the contract's missing text, the TfL link and the credits", async () => {
    const { container } = render(
      <TransportRoute widget={await sampleOf("transport_route", "not_known")} />,
    );
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText(
        "a journey: TfL returned none from this start to Heathrow for that day and time",
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: "Plan it on the TfL Journey Planner" }),
    ).toHaveAttribute("href", TFL);
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
    expect(
      within(container.querySelector("footer") as HTMLElement).getByText(OS),
    ).toBeInTheDocument();
  });

  it("empty with no journey is Not known", async () => {
    const base = await sampleOf("transport_route", "filled");
    render(<TransportRoute widget={{ ...base, state: "empty", legs: [], total_minutes: null }} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });
});
