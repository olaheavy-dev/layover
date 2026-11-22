import { render, screen } from "@testing-library/react";

import { WidgetFrame } from "./WidgetFrame";

const NOW = new Date("2026-11-18T09:00:00Z");
const live = { status: "live" as const, source: "Frankfurter" };

describe("WidgetFrame", () => {
  it("shows the title, the body and the source footer when filled", () => {
    render(
      <WidgetFrame title="Money" state="filled" sources={[live]} now={NOW}>
        <p>Body text</p>
      </WidgetFrame>,
    );
    expect(screen.getByRole("heading", { name: "Money" })).toBeInTheDocument();
    expect(screen.getByText("Body text")).toBeInTheDocument();
    expect(screen.getByText("Live")).toBeInTheDocument();
    expect(screen.getByText("Frankfurter")).toBeInTheDocument();
    expect(screen.getByRole("contentinfo")).toBeInTheDocument();
  });

  it("shows no footer when there are no sources", () => {
    render(<WidgetFrame title="Money" state="filled" sources={[]} />);
    expect(screen.queryByRole("contentinfo")).not.toBeInTheDocument();
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
