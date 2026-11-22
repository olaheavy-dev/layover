import { fireEvent, render, screen, within } from "@testing-library/react";

import { ComparisonTable } from "./ComparisonTable";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

function card(place: string): HTMLElement {
  return screen.getByRole("heading", { level: 4, name: place }).closest("li") as HTMLElement;
}

describe("ComparisonTable", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("comparison_table")).sort()).toEqual([
      "chosen",
      "empty",
      "error",
      "filled",
      "loading",
      "not_known",
      "swapped",
    ]);
  });

  it("filled: three cards with the same rows, the shown figures and Choose and Swap actions", async () => {
    const { container } = render(
      <ComparisonTable widget={await sampleOf("comparison_table", "filled")} />,
    );
    expect(screen.getByRole("heading", { level: 3, name: "Compare places" })).toBeInTheDocument();

    const lisbon = within(card("Lisbon"));
    expect(lisbon.getByText("£192")).toBeInTheDocument();
    expect(lisbon.getByText("£96 each")).toBeInTheDocument();
    expect(lisbon.getByText("about £350")).toBeInTheDocument();
    expect(
      lisbon.getByText(
        "£70 a night, an estimate from 6 Wikivoyage listings, page edited March 2026",
      ),
    ).toBeInTheDocument();
    expect(lisbon.getByText("about £240")).toBeInTheDocument();
    expect(lisbon.getByText("about £780")).toBeInTheDocument();
    expect(
      lisbon.getByText("Partial: local transport and activities are not known"),
    ).toBeInTheDocument();
    expect(lisbon.getByText("About £20 under")).toBeInTheDocument();
    expect(lisbon.getByText(/The costs that are not known could take it over/)).toBeInTheDocument();
    expect(
      lisbon.getByText(/22°C high, 14°C low, 5 rainy days, averages 1991 to 2020/),
    ).toBeInTheDocument();
    expect(lisbon.getByText("Cached, 3 days old")).toBeInTheDocument();
    expect(lisbon.getByText("Live")).toBeInTheDocument();
    expect(lisbon.getByRole("button", { name: "Choose Lisbon" })).toBeInTheDocument();
    expect(
      lisbon.getByRole("button", { name: "Swap Lisbon for a place of your own" }),
    ).toBeInTheDocument();

    const valletta = within(card("Valletta"));
    expect(valletta.getByText("£242")).toBeInTheDocument();
    expect(valletta.getByText("about £900")).toBeInTheDocument();
    expect(valletta.getByText("About £100 over")).toBeInTheDocument();
    expect(valletta.getByText(/on the known costs alone/)).toBeInTheDocument();
    expect(container.textContent).not.toContain("782");
    expect(container.textContent).not.toContain("902");

    const footer = within(screen.getByRole("contentinfo"));
    expect(footer.getByText("Travelpayouts")).toBeInTheDocument();
    expect(footer.getByText("Wikivoyage")).toBeInTheDocument();
    expect(footer.getByText("Open-Meteo")).toBeInTheDocument();
  });

  it("not_known: Valencia's stay and its comparison with the budget say Not known", async () => {
    render(<ComparisonTable widget={await sampleOf("comparison_table", "not_known")} />);
    const valencia = within(card("Valencia"));
    expect(valencia.getByText("£168")).toBeInTheDocument();
    expect(valencia.getByText("too few priced listings")).toBeInTheDocument();
    expect(valencia.getByText("about £390")).toBeInTheDocument();
    expect(
      valencia.getByText("Partial: stay, local transport and activities are not known"),
    ).toBeInTheDocument();
    expect(valencia.getByText("the stay is missing")).toBeInTheDocument();
    expect(valencia.getAllByText("Not known").length).toBeGreaterThanOrEqual(3);
    expect(valencia.queryByText(/about £\d+ (under|over)/i)).not.toBeInTheDocument();
    expect(valencia.queryByText("£0")).not.toBeInTheDocument();
  });

  it("loading: finished cards keep their figures, the others show shapes and keep their names", async () => {
    render(<ComparisonTable widget={await sampleOf("comparison_table", "loading")} />);
    expect(within(card("Lisbon")).getByText("£192")).toBeInTheDocument();
    for (const place of ["Valencia", "Valletta"]) {
      const c = within(card(place));
      expect(c.getByText("Checking fares, costs and weather")).toBeInTheDocument();
      expect(c.getByRole("status")).toHaveTextContent(`Checking ${place}`);
      expect(c.queryByText(/£/)).not.toBeInTheDocument();
    }
  });

  it("empty: says what rules places out and offers Edit brief", async () => {
    render(<ComparisonTable widget={await sampleOf("comparison_table", "empty")} />);
    expect(screen.getByRole("heading", { name: "No place fits yet" })).toBeInTheDocument();
    expect(screen.getByText("£800 in total")).toBeInTheDocument();
    expect(screen.getByText("rules places out")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Edit brief" })).toBeInTheDocument();
  });

  it("error: the failed card says Unavailable with Try again and no figure; the others stay", async () => {
    render(<ComparisonTable widget={await sampleOf("comparison_table", "error")} />);
    const valletta = within(card("Valletta"));
    expect(valletta.getByText("Unavailable")).toBeInTheDocument();
    expect(
      valletta.getByText(/Layover could not check fares, costs or weather for Valletta just now/),
    ).toBeInTheDocument();
    expect(valletta.getByRole("button", { name: "Try again for Valletta" })).toBeInTheDocument();
    expect(valletta.queryByText(/£/)).not.toBeInTheDocument();
    expect(within(card("Lisbon")).getByText("£192")).toBeInTheDocument();
    expect(within(card("Valencia")).getByText("£168")).toBeInTheDocument();
  });

  it("swapped: the traveller's own place is researching, with no figures", async () => {
    render(<ComparisonTable widget={await sampleOf("comparison_table", "swapped")} />);
    const porto = within(card("Porto"));
    expect(porto.getByText("Your place")).toBeInTheDocument();
    expect(porto.getByText("Researching your place")).toBeInTheDocument();
    expect(porto.getByText("Checking fares, costs and weather for Porto.")).toBeInTheDocument();
    expect(porto.getByRole("status")).toHaveTextContent("Researching Porto");
    expect(porto.getByRole("button", { name: "Swap back" })).toBeInTheDocument();
    expect(porto.queryByText(/£/)).not.toBeInTheDocument();
  });

  it("chosen: folds to one row, and Show again brings the cards back", async () => {
    render(<ComparisonTable widget={await sampleOf("comparison_table", "chosen")} />);
    expect(screen.getByText("Compared 3 places: you chose Lisbon")).toBeInTheDocument();
    expect(screen.getByText("You chose this")).toBeInTheDocument();
    expect(screen.getAllByText("Also compared")).toHaveLength(2);
    expect(screen.queryByRole("button", { name: "Choose Lisbon" })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Show again" }));
    expect(screen.getByRole("button", { name: "Choose Lisbon" })).toBeInTheDocument();
    expect(screen.queryByText("Compared 3 places: you chose Lisbon")).not.toBeInTheDocument();
  });
});
