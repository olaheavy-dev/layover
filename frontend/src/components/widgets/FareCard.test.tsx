import { render, screen } from "@testing-library/react";

import { FareCard } from "./FareCard";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

describe("FareCard", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("fare_card")).sort()).toEqual([
      "error",
      "filled",
      "loading",
      "not_known",
      "older_fare",
    ]);
  });

  it("filled: the fare as given, its age, the caveat and the Aviasales link", async () => {
    render(<FareCard widget={await sampleOf("fare_card", "filled")} />);
    expect(screen.getByRole("heading", { name: "Flights" })).toBeInTheDocument();
    expect(screen.getByText("£96")).toBeInTheDocument();
    expect(screen.getByText("return, per person, from Manchester (MAN)")).toBeInTheDocument();
    expect(screen.getAllByText("Cached, 3 days old").length).toBeGreaterThan(0);
    expect(screen.getByText("A cached fare can have changed since.")).toBeInTheDocument();
    expect(screen.getByText("Travelpayouts")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Check the live price on Aviasales/ })).toHaveAttribute(
      "href",
      "https://www.aviasales.com/",
    );
  });

  it("older_fare: the older figure with its own age", async () => {
    render(<FareCard widget={await sampleOf("fare_card", "older_fare")} />);
    expect(screen.getByText("£121")).toBeInTheDocument();
    expect(screen.getAllByText("Cached, 6 days old").length).toBeGreaterThan(0);
  });

  it("loading: a busy status and no figure", async () => {
    render(<FareCard widget={await sampleOf("fare_card", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Flights");
    expect(screen.queryByText(/£/)).not.toBeInTheDocument();
  });

  it("error: Unavailable, no fare, a search link and Try again", async () => {
    const { container } = render(<FareCard widget={await sampleOf("fare_card", "error")} />);
    expect(screen.getAllByText("Unavailable").length).toBeGreaterThan(0);
    expect(screen.getByText(/No fare is shown/)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Search flights on Aviasales/ })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/£/);
  });

  it("not_known: says Not known with the reason, never a price, and still links to Aviasales", async () => {
    const { container } = render(<FareCard widget={await sampleOf("fare_card", "not_known")} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText("there is no cached fare for Manchester (MAN) to Lisbon in May 2027"),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: /Check the live price on Aviasales/ }),
    ).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/£/);
  });

  it("does not link when the contract gives no search_url", async () => {
    const widget = { ...(await sampleOf("fare_card", "filled")), search_url: null };
    render(<FareCard widget={widget} />);
    expect(screen.queryByRole("link")).not.toBeInTheDocument();
  });
});
