import { render, screen } from "@testing-library/react";

import { getSampleTrip } from "@/lib/samples";

import { SharedTrip } from "./SharedTrip";

describe("SharedTrip", () => {
  it("adds the budget and traveller chips only when the trip was shared with them", async () => {
    const trip = await getSampleTrip();
    const shared = { ...trip, share: { ...trip.share, include_budget_and_travellers: true } };
    render(<SharedTrip trip={shared} />);
    expect(screen.getByText("2 adults")).toBeInTheDocument();
    expect(screen.getByText("£800 in total")).toBeInTheDocument();
  });

  it("leaves them out by default", async () => {
    render(<SharedTrip trip={await getSampleTrip()} />);
    expect(screen.queryByText("2 adults")).not.toBeInTheDocument();
    expect(screen.queryByText("£800 in total")).not.toBeInTheDocument();
  });
});
