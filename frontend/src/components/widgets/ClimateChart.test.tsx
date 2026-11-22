import { render, screen, within } from "@testing-library/react";

import { ClimateChart } from "./ClimateChart";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/climate_chart (Lisbon, April to June, highlight month 5).
describe("ClimateChart", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("climate_chart")).sort()).toEqual([
      "error",
      "filled",
      "loading",
      "not_known",
    ]);
  });

  it("filled: the highlighted month in words, the legend, the table and the source", async () => {
    render(<ClimateChart widget={await sampleOf("climate_chart", "filled")} />);
    expect(
      screen.getByRole("heading", { name: "Weather in April, May and June" }),
    ).toBeInTheDocument();
    expect(
      screen.getByText("May: highs of 22°C, lows of 14°C and 5 rainy days, typically."),
    ).toBeInTheDocument();
    expect(screen.getByText("Typical high (line)")).toBeInTheDocument();
    expect(screen.getByText("Typical low (dotted line)")).toBeInTheDocument();
    expect(screen.getByText("Rainy days in the month (bars)")).toBeInTheDocument();
    const table = screen.getByRole("table", {
      name: "Typical weather, averages for 1991 to 2020",
    });
    const june = within(table).getByRole("row", { name: /June/ });
    expect(
      within(june)
        .getAllByRole("cell")
        .map((c) => c.textContent),
    ).toEqual(["25°C", "16°C", "2"]);
    expect(screen.getByText("Live")).toBeInTheDocument();
    expect(screen.getByText("Open-Meteo")).toBeInTheDocument();
  });

  it("says 1 rainy day, not 1 rainy days", async () => {
    const widget = await sampleOf("climate_chart", "filled");
    const months = widget.months?.map((m) => (m.month === 5 ? { ...m, rainy_days: 1 } : m));
    render(<ClimateChart widget={{ ...widget, months }} />);
    expect(
      screen.getByText("May: highs of 22°C, lows of 14°C and 1 rainy day, typically."),
    ).toBeInTheDocument();
  });

  it("gives no summary line when every reading for the month is missing", async () => {
    const widget = await sampleOf("climate_chart", "filled");
    const months = widget.months?.map((m) =>
      m.month === 5 ? { ...m, high_c: null, low_c: null, rainy_days: null } : m,
    );
    render(<ClimateChart widget={{ ...widget, months }} />);
    expect(screen.queryByText(/typically\./)).not.toBeInTheDocument();
    expect(screen.queryByText(/^May:/)).not.toBeInTheDocument();
  });

  it("not_known: temperatures show, the missing rainy days say Not known in their own cells", async () => {
    render(<ClimateChart widget={await sampleOf("climate_chart", "not_known")} />);
    expect(screen.getByText("May: highs of 22°C and lows of 14°C, typically.")).toBeInTheDocument();
    expect(screen.queryByText(/rainy days, typically/)).not.toBeInTheDocument();
    expect(screen.queryByText("Rainy days in the month (bars)")).not.toBeInTheDocument();
    expect(
      screen.getByText("rainy days: no source Layover uses has them for this place and period"),
    ).toBeInTheDocument();
    const may = within(screen.getByRole("table")).getByRole("row", { name: /May/ });
    const cells = within(may).getAllByRole("cell");
    expect(cells.map((c) => c.textContent)).toEqual(["22°C", "14°C", "Not known"]);
  });

  it("loading: a busy status and no figure", async () => {
    const { container } = render(
      <ClimateChart widget={await sampleOf("climate_chart", "loading")} />,
    );
    expect(screen.getByRole("status")).toHaveTextContent("Loading");
    expect(container.textContent).not.toMatch(/°C/);
  });

  it("error: says what could not be checked, shows no figure and offers Try again", async () => {
    const { container } = render(
      <ClimateChart widget={await sampleOf("climate_chart", "error")} />,
    );
    expect(
      screen.getByText(
        "Layover could not check the typical weather just now. No temperatures or rainy days are shown.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(within(screen.getByRole("alert")).getByText("Unavailable")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/°C/);
  });

  it("filled with no months says nothing is known rather than drawing an empty chart", async () => {
    const widget = { ...(await sampleOf("climate_chart", "filled")), months: [] };
    render(<ClimateChart widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.queryByRole("table")).not.toBeInTheDocument();
  });
});
