import { render, screen } from "@testing-library/react";

import { NotKnown } from "./NotKnown";

describe("NotKnown", () => {
  it("shows Not known and the missing text", () => {
    render(<NotKnown missing="Local bus fares in Lisbon" />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText("Local bus fares in Lisbon")).toBeInTheDocument();
  });

  it("shows the reason and what happens instead when given", () => {
    render(<NotKnown missing="Fares" reason="No source has them" instead="Shown without fares" />);
    expect(screen.getByText("No source has them")).toBeInTheDocument();
    expect(screen.getByText("Shown without fares")).toBeInTheDocument();
  });

  it("never shows a stand-in for the missing value", () => {
    const { container } = render(<NotKnown missing="Fares" />);
    const text = container.textContent ?? "";
    // A bare "0" would also match any digit-bearing copy, so look for a zero as a figure.
    expect(text).not.toMatch(/(?<![\d.])0(?![\d])/);
    for (const banned of ["£0", "N/A", "—"]) {
      expect(text).not.toContain(banned);
    }
  });
});
