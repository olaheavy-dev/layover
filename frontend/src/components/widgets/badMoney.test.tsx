import { render, screen } from "@testing-library/react";

import { BookingApproval } from "./BookingApproval";
import { BriefSummary } from "./BriefSummary";
import { ComparisonTable } from "./ComparisonTable";
import { CostEstimate } from "./CostEstimate";
import { FareCard } from "./FareCard";
import { FareList } from "./FareList";
import { Money } from "./Money";
import { sampleOf, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// A money value the contract should never carry (a fraction of a minor unit), put in every place the
// sample has an amount. The widget must show Not known for it, never throw and never print a figure.
function withBadAmounts<T>(value: T): T {
  return JSON.parse(
    JSON.stringify(value, (key, inner) => (key === "amount_minor" ? 1.5 : inner)),
  ) as T;
}

function expectNoFigure(container: HTMLElement) {
  expect(container.textContent).not.toMatch(/£|NaN|undefined|null/);
}

describe("a bad amount shows Not known and never crashes the page", () => {
  it("FareCard", async () => {
    const { container } = render(
      <FareCard widget={withBadAmounts(await sampleOf("fare_card", "filled"))} />,
    );
    expectNoFigure(container);
    expect(screen.getByText(/Not known/)).toBeInTheDocument();
  });

  it("FareList", async () => {
    const { container } = render(
      <FareList widget={withBadAmounts(await sampleOf("fare_list", "filled"))} />,
    );
    expectNoFigure(container);
    expect(screen.getAllByText(/Not known/).length).toBeGreaterThan(0);
  });

  it("Money: the rate stays, the conversion says Not known", async () => {
    const { container } = render(
      <Money widget={withBadAmounts(await sampleOf("money", "conversion"))} />,
    );
    expect(container.textContent).not.toMatch(/is about|NaN|undefined|null/);
    expect(screen.getByText("£1 = €1.15")).toBeInTheDocument();
    expect(screen.getByText(/Not known/)).toBeInTheDocument();
  });

  it("BriefSummary: no budget chip", async () => {
    const { container } = render(
      <BriefSummary widget={withBadAmounts(await sampleOf("brief_summary", "waiting"))} />,
    );
    expectNoFigure(container);
    expect(screen.queryByText(/in total/)).not.toBeInTheDocument();
  });

  it.each(["filled", "price_changed"])(
    "BookingApproval %s: no price and no Approve",
    async (state) => {
      const { container } = render(
        <BookingApproval widget={withBadAmounts(await sampleOf("booking_approval", state))} />,
      );
      expectNoFigure(container);
      expect(screen.queryByRole("button", { name: /Approve/ })).not.toBeInTheDocument();
    },
  );

  it.each(["filled", "not_known"])("ComparisonTable %s", async (state) => {
    const { container } = render(
      <ComparisonTable widget={withBadAmounts(await sampleOf("comparison_table", state))} />,
    );
    expectNoFigure(container);
  });

  it.each(["filled", "partial", "over_budget", "not_known"])("CostEstimate %s", async (state) => {
    const { container } = render(
      <CostEstimate widget={withBadAmounts(await sampleOf("cost_estimate", state))} />,
    );
    expectNoFigure(container);
    expect(screen.getAllByText(/Not known/).length).toBeGreaterThan(0);
  });
});
