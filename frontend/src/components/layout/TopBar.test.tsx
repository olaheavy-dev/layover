import { render, screen } from "@testing-library/react";

import { TopBar } from "./TopBar";

describe("TopBar", () => {
  it("links the logo home and shows the trip name, Share trip, How it works and New trip", () => {
    render(<TopBar tripName="Warm break, May" />);
    expect(screen.getByRole("link", { name: "Layover, home" })).toHaveAttribute("href", "/");
    expect(screen.getByText("Warm break, May")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Share trip" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "How it works" })).toHaveAttribute(
      "href",
      "/how-it-works",
    );
    expect(screen.getByRole("button", { name: "New trip" })).toBeInTheDocument();
  });

  it("has no Share trip on a shared trip", () => {
    render(<TopBar tripName="Warm break, May" shared />);
    expect(screen.queryByRole("button", { name: "Share trip" })).not.toBeInTheDocument();
    expect(screen.getByText("Warm break, May")).toBeInTheDocument();
  });

  it("has no Share trip when there is no trip yet", () => {
    render(<TopBar />);
    expect(screen.queryByRole("button", { name: "Share trip" })).not.toBeInTheDocument();
  });

  it("holds no heading, because the page owns the h1", () => {
    render(<TopBar tripName="Warm break, May" />);
    expect(screen.queryByRole("heading")).not.toBeInTheDocument();
  });

  it("shows the Layover logo as an SVG inside the home link, hidden from screen readers", () => {
    render(<TopBar tripName="Warm break, May" />);
    const home = screen.getByRole("link", { name: "Layover, home" });
    const svgs = home.querySelectorAll("svg");
    expect(svgs.length).toBe(2);
    svgs.forEach((svg) => expect(svg).toHaveAttribute("aria-hidden", "true"));
    expect(home.innerHTML).toContain("var(--logo-ink)");
    expect(home.innerHTML).not.toMatch(/#[0-9a-fA-F]{6}/);
  });
});
