import { render, screen } from "@testing-library/react";

import type { components } from "@/lib/api/schema";

import { SourceLabel } from "./SourceLabel";

type Label = components["schemas"]["SourceLabel"];

// A fixed "now" passed as a prop, so no test depends on the clock.
const NOW = new Date("2026-11-18T09:00:00Z");

describe("SourceLabel", () => {
  it("shows the age of a cached label", () => {
    // Working: 18 Nov 2026 09:00 minus 15 Nov 2026 09:00 = 3 whole days.
    // Source: schemas/samples/README.md ("3 days old" is a captured_at of 15 Nov 2026 at 09:00 UTC).
    const label: Label = {
      status: "cached",
      source: "Travelpayouts",
      captured_at: "2026-11-15T09:00:00Z",
    };
    render(<SourceLabel label={label} now={NOW} />);
    expect(screen.getByText("Cached, 3 days old")).toBeInTheDocument();
  });

  it("lets the source name wrap under the status and keeps the icon its size", () => {
    const label: Label = {
      status: "cached",
      source: "Travelpayouts",
      captured_at: "2026-11-15T09:00:00Z",
    };
    const { container } = render(<SourceLabel label={label} now={NOW} />);
    expect(container.firstElementChild).toHaveClass("flex-wrap");
    expect(container.querySelector("svg")).toHaveClass("shrink-0");
  });

  it("says 1 day old, not 1 days old", () => {
    const label: Label = { status: "cached", source: "S", captured_at: "2026-11-17T09:00:00Z" };
    render(<SourceLabel label={label} now={NOW} />);
    expect(screen.getByText("Cached, 1 day old")).toBeInTheDocument();
  });

  it("shows the release date when a cached label has only a data date", () => {
    const label: Label = { status: "cached", source: "Foursquare", data_date: "2026-11-04" };
    render(<SourceLabel label={label} now={NOW} />);
    expect(screen.getByText("Cached, data released 4 Nov 2026")).toBeInTheDocument();
  });

  it("never invents an age when a cached label has neither", () => {
    render(<SourceLabel label={{ status: "cached", source: "S" }} now={NOW} />);
    expect(screen.getByText("Cached, age not known")).toBeInTheDocument();
  });

  it.each([
    ["live", "Live"],
    ["fallback", "Fallback"],
    ["unavailable", "Unavailable"],
  ] as const)("shows %s as the word %s", (status, word) => {
    render(<SourceLabel label={{ status, source: "Frankfurter" }} now={NOW} />);
    expect(screen.getByText(word)).toBeInTheDocument();
    expect(screen.getByText("Frankfurter")).toBeInTheDocument();
  });

  it("never prints NaN or throws for an unparseable captured_at or data_date", () => {
    const bad: Label = { status: "cached", source: "S", captured_at: "bad", data_date: "bad" };
    expect(() => render(<SourceLabel label={bad} now={NOW} />)).not.toThrow();
    expect(screen.getByText("Cached, age not known")).toBeInTheDocument();
  });

  it("falls back to a valid data_date when captured_at is unparseable", () => {
    const label: Label = {
      status: "cached",
      source: "S",
      captured_at: "bad",
      data_date: "2026-11-04",
    };
    render(<SourceLabel label={label} now={NOW} />);
    expect(screen.getByText("Cached, data released 4 Nov 2026")).toBeInTheDocument();
  });

  it("does not claim freshness for a captured_at in the future", () => {
    const label: Label = { status: "cached", source: "S", captured_at: "2026-11-19T09:00:00Z" };
    render(<SourceLabel label={label} now={NOW} />);
    expect(screen.getByText("Cached, age not known")).toBeInTheDocument();
  });
});
