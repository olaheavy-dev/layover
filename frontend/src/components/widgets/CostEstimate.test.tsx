import { render, screen, within } from "@testing-library/react";

import { CostEstimate } from "./CostEstimate";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

function line(name: string): HTMLElement {
  return screen.getByText(name, { selector: "span" }).closest("li") as HTMLElement;
}

describe("CostEstimate", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("cost_estimate")).sort()).toEqual([
      "error",
      "filled",
      "loading",
      "not_known",
      "over_budget",
      "partial",
    ]);
  });

  it("filled: the shown total and gap, never the exact £782, and lines without a value say Not known", async () => {
    const { container } = render(
      <CostEstimate widget={await sampleOf("cost_estimate", "filled")} />,
    );
    expect(screen.getByRole("heading", { name: "Cost estimate" })).toBeInTheDocument();
    expect(screen.getByText("about £780")).toBeInTheDocument();
    expect(
      screen.getByText(
        "estimate of the known costs, partial: local transport and activities are not known",
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText("About £20 under your £800 budget on the known costs."),
    ).toBeInTheDocument();
    expect(screen.getByText(/The costs that are not known could take it over/)).toBeInTheDocument();
    expect(container.textContent).not.toContain("782");
    expect(container.textContent).not.toContain("£18");

    const flights = within(line("Flights"));
    expect(flights.getByText("£192")).toBeInTheDocument();
    expect(flights.getByText("£96 each")).toBeInTheDocument();
    expect(flights.getByText("Cached, 3 days old")).toBeInTheDocument();

    const stay = within(line("Stay, 5 nights"));
    expect(stay.getByText("about £350")).toBeInTheDocument();
    expect(stay.getByText("estimate")).toBeInTheDocument();
    expect(
      stay.getByText("About £70 a night, from 6 Wikivoyage listings (page edited March 2026)"),
    ).toBeInTheDocument();
    expect(stay.getByText("Cached, 4 days old")).toBeInTheDocument();

    const meals = within(line("Meals"));
    expect(meals.getByText("about £240")).toBeInTheDocument();
    expect(
      meals.getByText("About £12 a meal, from Wikivoyage (page edited March 2026)"),
    ).toBeInTheDocument();

    const local = within(line("Local transport and activities"));
    expect(local.getByText("Not known")).toBeInTheDocument();
    expect(local.getByText("no source Layover uses has it")).toBeInTheDocument();
  });

  it("over_budget: says over, in words, on the known costs alone", async () => {
    render(<CostEstimate widget={await sampleOf("cost_estimate", "over_budget")} />);
    expect(screen.getByText("about £900")).toBeInTheDocument();
    expect(
      screen.getByText("About £100 over your £800 budget on the known costs alone."),
    ).toBeInTheDocument();
    expect(screen.getByText(/The costs that are not known would add to it/)).toBeInTheDocument();
    expect(within(line("Flights")).getByText("£242")).toBeInTheDocument();
  });

  it("partial: a line Unavailable, the total 'so far', and no comparison with the budget", async () => {
    const { container } = render(
      <CostEstimate widget={await sampleOf("cost_estimate", "partial")} />,
    );
    expect(screen.getByText("about £590")).toBeInTheDocument();
    expect(
      screen.getByText(
        "so far, partial: flights could not be checked, and local transport and activities are not known",
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "This total is not complete, so Layover is not comparing it with your £800 budget.",
      ),
    ).toBeInTheDocument();
    const flights = within(line("Flights"));
    expect(flights.getByText("Unavailable")).toBeInTheDocument();
    expect(flights.getByText("Layover could not check fares just now")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/under|over your/);
  });

  it("not_known: the stay line says Not known and the total is not compared with the budget", async () => {
    render(<CostEstimate widget={await sampleOf("cost_estimate", "not_known")} />);
    expect(screen.getByText("about £390")).toBeInTheDocument();
    expect(
      screen.getByText(
        "estimate of the known costs, partial: stay, local transport and activities are not known",
      ),
    ).toBeInTheDocument();
    expect(
      screen.getByText(
        "Stay is not known, so Layover cannot compare this total with your £800 budget.",
      ),
    ).toBeInTheDocument();
    const stay = within(line("Stay, 5 nights"));
    expect(stay.getByText("Not known")).toBeInTheDocument();
    expect(stay.getByText("too few priced listings")).toBeInTheDocument();
    expect(
      within(line("Meals")).getByText(
        "About £11 a meal, from 5 Wikivoyage listings (page edited February 2026)",
      ),
    ).toBeInTheDocument();
  });

  it("loading: a busy status and no figures", async () => {
    const { container } = render(
      <CostEstimate widget={await sampleOf("cost_estimate", "loading")} />,
    );
    expect(screen.getByRole("status")).toHaveTextContent("Loading Cost estimate");
    expect(container.textContent).not.toMatch(/£/);
  });

  it("error: an alert, both sources Unavailable and no figure", async () => {
    const { container } = render(
      <CostEstimate widget={await sampleOf("cost_estimate", "error")} />,
    );
    expect(screen.getByRole("alert")).toBeInTheDocument();
    expect(screen.getAllByText("Unavailable")).toHaveLength(2);
    expect(container.textContent).not.toMatch(/£\d/);
  });

  it("shows Not known for a total that is missing, never zero", async () => {
    const widget = {
      ...(await sampleOf("cost_estimate", "filled")),
      total: null,
      budget_gap: null,
    };
    const { container } = render(<CostEstimate widget={widget} />);
    const block = screen.getByText("The total").parentElement as HTMLElement;
    expect(within(block).getByText("Not known")).toBeInTheDocument();
    expect(block).not.toHaveTextContent(/£/);
    expect(container.textContent).not.toMatch(/£0\b/);
  });
});
