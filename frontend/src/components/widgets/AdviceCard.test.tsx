import { render, screen, within } from "@testing-library/react";

import { AdviceCard } from "./AdviceCard";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

// Source: schemas/samples/widgets/advice_card (Portugal, updated 2026-11-12, captured 17 Nov 2026
// so 1 day old at TEST_NOW, 18 Nov 2026). Decision 0011 rule 6: always the FCDO link and its date.
describe("AdviceCard", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("advice_card")).sort()).toEqual([
      "error",
      "filled",
      "loading",
      "not_known",
    ]);
  });

  it("filled: the title, the update date, the FCDO link and the cached label", async () => {
    render(<AdviceCard widget={await sampleOf("advice_card", "filled")} />);
    expect(screen.getByRole("heading", { name: "Travel advice" })).toBeInTheDocument();
    expect(screen.getByText("FCDO travel advice: Portugal")).toBeInTheDocument();
    expect(screen.getByText("Updated 12 Nov 2026")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Read the FCDO advice for Portugal/ })).toHaveAttribute(
      "href",
      "https://www.gov.uk/foreign-travel-advice/portugal",
    );
    expect(screen.getByText("Cached, 1 day old")).toBeInTheDocument();
    expect(screen.getByText("Layover’s copy")).toBeInTheDocument();
    expect(screen.getByText("FCDO, gov.uk")).toBeInTheDocument();
  });

  it("filled with no update date still links, and says the date is Not known", async () => {
    const widget = { ...(await sampleOf("advice_card", "filled")), updated_on: null };
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});
    render(<AdviceCard widget={widget} />);
    // No <div> inside a <p> (React logs this as a hydration error).
    expect(spy).not.toHaveBeenCalled();
    spy.mockRestore();
    expect(screen.queryByText(/^Updated/)).not.toBeInTheDocument();
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Read the FCDO advice/ })).toBeInTheDocument();
  });

  it("never calls the destination safe", async () => {
    const { container } = render(<AdviceCard widget={await sampleOf("advice_card", "filled")} />);
    expect(container.textContent?.toLowerCase()).not.toMatch(/\bsafe/);
  });

  it("error: the link still shows, no date, Try again", async () => {
    render(<AdviceCard widget={await sampleOf("advice_card", "error")} />);
    expect(
      screen.getByText("Layover could not read it just now. The FCDO page is still there."),
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Read the FCDO advice for Portugal/ })).toHaveAttribute(
      "href",
      "https://www.gov.uk/foreign-travel-advice/portugal",
    );
    expect(screen.queryByText(/^Updated/)).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(within(screen.getByRole("alert")).getByText("Unavailable")).toBeInTheDocument();
  });

  it("not_known: the reason and the link to the FCDO index", async () => {
    render(<AdviceCard widget={await sampleOf("advice_card", "not_known")} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(
      screen.getByText("Layover has no FCDO travel advice page for this place"),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("link", { name: /Find a country on the FCDO travel advice index/ }),
    ).toHaveAttribute("href", "https://www.gov.uk/foreign-travel-advice");
    expect(screen.queryByText(/^Updated/)).not.toBeInTheDocument();
  });

  it("loading: a busy status", async () => {
    render(<AdviceCard widget={await sampleOf("advice_card", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Travel advice");
  });
});
