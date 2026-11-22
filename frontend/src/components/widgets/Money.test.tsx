import { render, screen, within } from "@testing-library/react";

import { Money } from "./Money";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/money (GBP to EUR, rate "1.15" dated 2026-11-18; conversion of
// 50000 pence to 57500 cents). The frontend does no conversion: every figure is the contract's.
// Working: 50000 minor units / 100 = £500; 57500 / 100 = €575.
describe("Money", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("money")).sort()).toEqual([
      "conversion",
      "error",
      "filled",
      "loading",
      "not_known",
    ]);
  });

  it("filled: the rate as given, its date and the source", async () => {
    const { container } = render(<Money widget={await sampleOf("money", "filled")} />);
    expect(screen.getByRole("heading", { name: "Money" })).toBeInTheDocument();
    expect(screen.getByText("£1 = €1.15")).toBeInTheDocument();
    expect(screen.getByText("Rate for 18 Nov 2026")).toBeInTheDocument();
    expect(screen.getByText("Live")).toBeInTheDocument();
    expect(screen.getByText("Frankfurter")).toBeInTheDocument();
    // The sample has no conversion, so none is shown.
    expect(container.textContent).not.toMatch(/about €/);
  });

  it("conversion: the amount and the converted figure as the contract gives them", async () => {
    render(<Money widget={await sampleOf("money", "conversion")} />);
    expect(screen.getByText("£500")).toBeInTheDocument();
    expect(screen.getByText("is about €575 at £1 = €1.15")).toBeInTheDocument();
    expect(screen.getByText("Worked out by Layover's code, not by the model.")).toBeInTheDocument();
  });

  it("filled with no rate says Not known, never a rate of 0", async () => {
    const widget = { ...(await sampleOf("money", "filled")), rate: null };
    const { container } = render(<Money widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/= /);
  });

  it("not_known: the reason and no rate", async () => {
    const { container } = render(<Money widget={await sampleOf("money", "not_known")} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText("the local currency is not in the European Central Bank's reference rates"),
    ).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/=/);
  });

  it("loading: a busy status", async () => {
    render(<Money widget={await sampleOf("money", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Money");
  });

  it("error: what could not be checked, no rate, Try again", async () => {
    const { container } = render(<Money widget={await sampleOf("money", "error")} />);
    expect(
      screen.getByText("Layover could not check the exchange rate just now. No rate is shown."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(within(screen.getByRole("alert")).getByText("Unavailable")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/=/);
  });
});
