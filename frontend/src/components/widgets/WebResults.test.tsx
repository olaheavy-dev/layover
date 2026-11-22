import { render, screen, within } from "@testing-library/react";

import { nth, sampleOf, sampleStates, TEST_NOW } from "./testing";
import { WebResults } from "./WebResults";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

const TAG = "From a web search, not checked by Layover";

// Source: schemas/samples/widgets/web_results, and the "Web results" section of
// docs/design/boards/screens/widgets-journey.html. Working: retrieved_at 2026-11-18T09:00:00Z is
// 18 Nov 2026.
describe("WebResults", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("web_results")).sort()).toEqual(["error", "filled", "loading"]);
  });

  it("filled: the label, each result's link, quote, site and retrieval date, and no Add to trip", async () => {
    const { container } = render(<WebResults widget={await sampleOf("web_results", "filled")} />);
    expect(screen.getByRole("heading", { name: "Web results" })).toBeInTheDocument();
    expect(screen.getByText(TAG)).toBeInTheDocument();
    const rows = screen.getAllByRole("listitem");
    expect(rows).toHaveLength(2);
    expect(
      within(nth(rows, 0)).getByRole("link", { name: "Trams with a pushchair (sample page one)" }),
    ).toHaveAttribute("href", "https://example.org/sample-page-one");
    expect(
      within(nth(rows, 0)).getByText("“Fold the pushchair before you board if the tram is busy.”"),
    ).toBeInTheDocument();
    expect(
      within(nth(rows, 0)).getByText("example.org · Retrieved 18 Nov 2026"),
    ).toBeInTheDocument();
    expect(
      within(nth(rows, 1)).getByRole("link", {
        name: "Getting around with children (sample page two)",
      }),
    ).toHaveAttribute("href", "https://example.org/sample-page-two");
    expect(
      within(nth(rows, 1)).getByText("“Ask the driver where to stand with a pushchair.”"),
    ).toBeInTheDocument();
    expect(screen.queryByRole("button")).toBeNull();
    expect(container.textContent).not.toMatch(/Add to trip/i);
    // The footer is the board's own: the retrieval date, then the source. Never Live or Cached.
    const footer = within(container.querySelector("footer") as HTMLElement);
    expect(footer.getByText("Retrieved 18 Nov 2026")).toBeInTheDocument();
    expect(footer.getByText("Source: Tavily web search")).toBeInTheDocument();
    expect(footer.queryByText(/Live|Cached/)).toBeNull();
  });

  it("a result with an address that is not http or https is left out", async () => {
    const base = await sampleOf("web_results", "filled");
    const widget = {
      ...base,
      results: [{ ...nth(base.results!, 0), url: "javascript:alert(1)" }, nth(base.results!, 1)],
    };
    render(<WebResults widget={widget} />);
    expect(screen.getAllByRole("listitem")).toHaveLength(1);
    expect(screen.queryByText("Trams with a pushchair (sample page one)")).toBeNull();
    expect(screen.getByRole("link", { name: /sample page two/ })).toBeInTheDocument();
  });

  it("error: the footer adds no status", async () => {
    const { container } = render(<WebResults widget={await sampleOf("web_results", "error")} />);
    expect(container.querySelector("footer")).toBeNull();
  });

  it("filled with no retrieval date says Not known, never a made-up date", async () => {
    const widget = { ...(await sampleOf("web_results", "filled")), retrieved_at: null };
    render(<WebResults widget={widget} />);
    expect(screen.queryByText(/Retrieved/)).toBeNull();
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText("when these results were retrieved")).toBeInTheDocument();
  });

  it("filled with no results says Layover cannot help yet, with no label or invented result", async () => {
    const widget = { ...(await sampleOf("web_results", "filled")), results: [] };
    render(<WebResults widget={widget} />);
    expect(
      screen.getByText("I can’t help with that yet. The web search found nothing I can use."),
    ).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });

  it("loading: a busy status", async () => {
    render(<WebResults widget={await sampleOf("web_results", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Web results");
  });

  it("error: Unavailable, the chat line, Try again, no results", async () => {
    render(<WebResults widget={await sampleOf("web_results", "error")} />);
    const alert = screen.getByRole("alert");
    expect(within(alert).getByText("Unavailable")).toBeInTheDocument();
    expect(
      within(alert).getByText(
        "I can’t help with that yet. The web search did not answer just now.",
      ),
    ).toBeInTheDocument();
    expect(within(alert).getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(screen.queryAllByRole("listitem")).toHaveLength(0);
  });
});
