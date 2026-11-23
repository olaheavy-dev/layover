import { render, screen } from "@testing-library/react";

import { WidgetFrame } from "./WidgetFrame";

const NOW = new Date("2026-11-18T09:00:00Z");
const live = { status: "live" as const, source: "Frankfurter" };

describe("WidgetFrame", () => {
  it("shows the title, the body and the source footer when filled", () => {
    const { container } = render(
      <WidgetFrame title="Money" state="filled" sources={[live]} now={NOW}>
        <p>Body text</p>
      </WidgetFrame>,
    );
    expect(screen.getByRole("heading", { name: "Money" })).toBeInTheDocument();
    expect(screen.getByText("Body text")).toBeInTheDocument();
    expect(screen.getByText("Live")).toBeInTheDocument();
    expect(screen.getByText("Frankfurter")).toBeInTheDocument();
    // A <footer> inside a <section> has no contentinfo role in browsers, so find it by tag.
    expect(container.querySelector("footer")).toBeInTheDocument();
  });

  it("shows no footer when there are no sources", () => {
    const { container } = render(<WidgetFrame title="Money" state="filled" sources={[]} />);
    expect(container.querySelector("footer")).toBeNull();
  });

  it("shows a loading status and marks the card busy", () => {
    const { container } = render(<WidgetFrame title="Money" state="loading" sources={[]} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Money");
    expect(container.querySelector("section")).toHaveAttribute("aria-busy", "true");
  });

  it("shows the empty text", () => {
    render(<WidgetFrame title="Money" state="empty" sources={[]} emptyText="No fares yet" />);
    expect(screen.getByText("No fares yet")).toBeInTheDocument();
  });

  it("shows an error as an alert", () => {
    render(<WidgetFrame title="Money" state="error" sources={[]} />);
    expect(screen.getByRole("alert")).toHaveTextContent("This part of the trip couldn't load");
  });

  it("shows Not known with the missing text", () => {
    render(<WidgetFrame title="Money" state="not_known" sources={[]} missing="The rate" />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText("The rate")).toBeInTheDocument();
  });
});

describe("WidgetFrame notice", () => {
  it("shows a notice above the body in every state, including loading", () => {
    render(
      <WidgetFrame
        title="Try booking"
        state="loading"
        sources={[]}
        notice={<p>A standing notice</p>}
      />,
    );
    expect(screen.getByText("A standing notice")).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent("Loading Try booking");
  });
});
