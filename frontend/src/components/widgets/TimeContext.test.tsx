import { render, screen } from "@testing-library/react";

import { SourceLabel } from "./SourceLabel";
import { TimeProvider } from "./TimeContext";

// The sample's own "today" (schemas/samples/README.md: 18 Nov 2026, 09:00 UTC).
const SAMPLE_TODAY = new Date("2026-11-18T09:00:00Z");

describe("TimeProvider", () => {
  it("measures a cached age against the page's own date, not the clock", () => {
    // Working: 18 Nov 2026 09:00 minus 15 Nov 2026 09:00 = 3 whole days, whatever today is.
    // Source: schemas/samples/README.md ("3 days old" is a captured_at of 15 Nov 2026 at 09:00 UTC).
    render(
      <TimeProvider now={SAMPLE_TODAY}>
        <SourceLabel
          label={{ status: "cached", source: "Travelpayouts", captured_at: "2026-11-15T09:00:00Z" }}
        />
      </TimeProvider>,
    );
    expect(screen.getByText("Cached, 3 days old")).toBeInTheDocument();
  });

  it("adds ', as of' and the date to a Live or Cached label on a shared trip", () => {
    // Source: docs/design/boards/sample-data.md ("Shared trip, as of rule").
    render(
      <TimeProvider now={SAMPLE_TODAY} asOf>
        <SourceLabel
          label={{ status: "cached", source: "Travelpayouts", captured_at: "2026-11-15T09:00:00Z" }}
        />
        <SourceLabel label={{ status: "live", source: "Frankfurter" }} />
      </TimeProvider>,
    );
    expect(screen.getByText("Cached, 3 days old, as of 18 Nov 2026")).toBeInTheDocument();
    expect(screen.getByText("Live, as of 18 Nov 2026")).toBeInTheDocument();
  });

  it("leaves Fallback and Unavailable labels as they are on a shared trip", () => {
    render(
      <TimeProvider now={SAMPLE_TODAY} asOf>
        <SourceLabel label={{ status: "unavailable", source: "Duffel" }} />
        <SourceLabel label={{ status: "fallback", source: "Wikivoyage" }} />
      </TimeProvider>,
    );
    expect(screen.getByText("Unavailable")).toBeInTheDocument();
    expect(screen.getByText("Fallback")).toBeInTheDocument();
  });
});
