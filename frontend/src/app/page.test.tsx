import { render, screen } from "@testing-library/react";
import Home from "./page";

describe("Home", () => {
  it("has one main heading, the welcome question", () => {
    render(<Home />);
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Where to next?");
  });

  it("shows the chat, the empty canvas with the honesty line, and no sample label", () => {
    render(<Home />);
    expect(screen.getByRole("region", { name: "Chat" })).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Your trip" })).toBeInTheDocument();
    expect(
      screen.getByText("Every figure shows where it came from and how old it is."),
    ).toBeInTheDocument();
    expect(screen.queryByText("Sample trip")).not.toBeInTheDocument();
  });

  it("opens on the Chat tab, because there is no trip yet", () => {
    render(<Home />);
    expect(screen.getByRole("tab", { name: "Chat" })).toHaveAttribute("aria-selected", "true");
    expect(document.getElementById("panel-trip")).toHaveClass("hidden");
  });

  it("has no Share trip or trip name on the welcome screen", () => {
    render(<Home />);
    expect(screen.queryByRole("button", { name: "Share trip" })).not.toBeInTheDocument();
  });
});
