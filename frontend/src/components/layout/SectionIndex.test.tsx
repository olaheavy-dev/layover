import { render, screen, within } from "@testing-library/react";

import { SectionIndex } from "./SectionIndex";

describe("SectionIndex", () => {
  it("lists only the sections with content, in journey order", () => {
    render(<SectionIndex sections={["days", "brief", "place", "compare"]} place="Lisbon" />);
    const links = within(
      screen.getByRole("navigation", { name: "Sections of the trip" }),
    ).getAllByRole("link");
    expect(links.map((link) => link.textContent)).toEqual(["Brief", "Compare", "Lisbon", "Days"]);
    expect(screen.queryByRole("link", { name: "Stay" })).not.toBeInTheDocument();
    expect(screen.queryByRole("link", { name: "Booking" })).not.toBeInTheDocument();
  });

  it("links each section to its anchor", () => {
    render(<SectionIndex sections={["brief", "place", "booking"]} place="Lisbon" />);
    expect(screen.getByRole("link", { name: "Brief" })).toHaveAttribute("href", "#brief");
    expect(screen.getByRole("link", { name: "Lisbon" })).toHaveAttribute("href", "#place");
    expect(screen.getByRole("link", { name: "Booking" })).toHaveAttribute("href", "#booking");
  });

  it("marks the current section with aria-current, bold and underlined", () => {
    render(<SectionIndex sections={["brief", "compare"]} current="compare" />);
    const current = screen.getByRole("link", { name: "Compare" });
    expect(current).toHaveAttribute("aria-current", "true");
    expect(current).toHaveClass("font-bold", "underline");
    const other = screen.getByRole("link", { name: "Brief" });
    expect(other).not.toHaveAttribute("aria-current");
    expect(other).not.toHaveClass("font-bold");
  });

  it("falls back to a plain label when the place has no name yet", () => {
    render(<SectionIndex sections={["place"]} />);
    expect(screen.getByRole("link", { name: "Place" })).toBeInTheDocument();
  });

  it("renders nothing when no section has content", () => {
    const { container } = render(<SectionIndex sections={[]} />);
    expect(container).toBeEmptyDOMElement();
  });
});
