import { fireEvent, render, screen } from "@testing-library/react";

import { TripStrip } from "./TripStrip";

describe("TripStrip", () => {
  it("shows the trip name, what is ready and View trip", () => {
    render(<TripStrip name="Lisbon, May" factsReady={5} onViewTrip={() => {}} />);
    expect(screen.getByRole("group", { name: "Your trip so far" })).toBeInTheDocument();
    expect(screen.getByText("Lisbon, May")).toBeInTheDocument();
    expect(screen.getByText("5 facts ready")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "View trip" })).toBeInTheDocument();
  });

  it("uses the singular for one fact", () => {
    render(<TripStrip name="Lisbon, May" factsReady={1} onViewTrip={() => {}} />);
    expect(screen.getByText("1 fact ready")).toBeInTheDocument();
  });

  it("shows no count when none is given", () => {
    render(<TripStrip name="Lisbon, May" onViewTrip={() => {}} />);
    expect(screen.queryByText(/ready/)).not.toBeInTheDocument();
  });

  it("calls onViewTrip", () => {
    const onViewTrip = vi.fn();
    render(<TripStrip name="Lisbon, May" onViewTrip={onViewTrip} />);
    fireEvent.click(screen.getByRole("button", { name: "View trip" }));
    expect(onViewTrip).toHaveBeenCalledOnce();
  });

  it("shows the place photo when one is given", () => {
    render(
      <TripStrip
        name="Lisbon, May"
        photoSrc="/lisbon.jpg"
        photoAlt="Red roofs in Lisbon"
        onViewTrip={() => {}}
      />,
    );
    expect(screen.getByRole("img", { name: "Red roofs in Lisbon" })).toHaveAttribute(
      "src",
      expect.stringContaining("lisbon.jpg"),
    );
  });

  it("falls back to the icon when there is no photo", () => {
    const { container } = render(<TripStrip name="Lisbon, May" onViewTrip={() => {}} />);
    expect(screen.queryByRole("img")).not.toBeInTheDocument();
    expect(container.querySelector("svg")).toHaveAttribute("aria-hidden", "true");
  });
});
