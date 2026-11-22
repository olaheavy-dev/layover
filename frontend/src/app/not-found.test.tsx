import { render, screen } from "@testing-library/react";

import NotFound from "./not-found";

describe("Link not found", () => {
  it("shows the board's wording under one h1, without saying whether a trip existed", () => {
    render(<NotFound />);
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("This link does not work");
    expect(screen.getByText("Link not found")).toBeInTheDocument();
    expect(
      screen.getByText(
        "The address may be wrong, or the link may no longer work. Check that you copied all of it.",
      ),
    ).toBeInTheDocument();
  });

  it("offers Plan a new trip and How Layover works", () => {
    render(<NotFound />);
    expect(screen.getByRole("link", { name: "Plan a new trip" })).toHaveAttribute("href", "/");
    expect(screen.getByRole("link", { name: "How Layover works" })).toHaveAttribute(
      "href",
      "/how-it-works",
    );
  });
});
