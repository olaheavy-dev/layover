import { render, screen, within } from "@testing-library/react";

import { SeaConditions } from "./SeaConditions";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/sea_conditions (Lisbon, month 5, 17°C).
describe("SeaConditions", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("sea_conditions")).sort()).toEqual([
      "error",
      "filled",
      "loading",
      "not_known",
    ]);
  });

  it("filled: the temperature as given, the place and month, the source", async () => {
    render(<SeaConditions widget={await sampleOf("sea_conditions", "filled")} />);
    expect(screen.getByRole("heading", { name: "Sea temperature" })).toBeInTheDocument();
    expect(screen.getByText("17°C")).toBeInTheDocument();
    expect(screen.getByText("the sea off Lisbon in May")).toBeInTheDocument();
    expect(screen.getByText("Live")).toBeInTheDocument();
    expect(screen.getByText("Open-Meteo Marine")).toBeInTheDocument();
  });

  it("filled with no temperature says Not known, never 0°C", async () => {
    const widget = { ...(await sampleOf("sea_conditions", "filled")), sea_temp_c: null };
    const { container } = render(<SeaConditions widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/°C/);
  });

  it("a temperature of 0 is shown as 0°C, not as missing", async () => {
    const widget = { ...(await sampleOf("sea_conditions", "filled")), sea_temp_c: 0 };
    render(<SeaConditions widget={widget} />);
    expect(screen.getByText("0°C")).toBeInTheDocument();
  });

  it("not_known: the missing value in words and no figure", async () => {
    const { container } = render(
      <SeaConditions widget={await sampleOf("sea_conditions", "not_known")} />,
    );
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText("sea temperature for this coast")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/°C/);
  });

  it("loading: a busy status", async () => {
    render(<SeaConditions widget={await sampleOf("sea_conditions", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Sea temperature");
  });

  it("error: what could not be checked, no figure, Try again", async () => {
    const { container } = render(
      <SeaConditions widget={await sampleOf("sea_conditions", "error")} />,
    );
    expect(
      screen.getByText("Layover could not check the sea temperature just now. No figure is shown."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(within(screen.getByRole("alert")).getByText("Unavailable")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/°C/);
  });
});
