import { render, screen } from "@testing-library/react";

import { getSampleTrip, SAMPLE_TODAY, type Trip } from "@/lib/samples";

import { SharedTrip } from "./SharedTrip";

// A trip that is not the sample, with no date on its share settings.
async function ownTrip(): Promise<Trip> {
  const trip = await getSampleTrip();
  return { ...trip, is_sample: false, share: { include_budget_and_travellers: false } };
}

describe("SharedTrip", () => {
  it("adds the budget and traveller chips only when the trip was shared with them", async () => {
    const trip = await getSampleTrip();
    const shared = { ...trip, share: { ...trip.share, include_budget_and_travellers: true } };
    render(<SharedTrip trip={shared} asOf={SAMPLE_TODAY} />);
    expect(screen.getByText("2 adults")).toBeInTheDocument();
    expect(screen.getByText("£800 in total")).toBeInTheDocument();
  });

  it("leaves them out by default", async () => {
    render(<SharedTrip trip={await getSampleTrip()} asOf={SAMPLE_TODAY} />);
    expect(screen.queryByText("2 adults")).not.toBeInTheDocument();
    expect(screen.queryByText("£800 in total")).not.toBeInTheDocument();
  });

  it("shows the date it is given in the header and on the labels", async () => {
    render(<SharedTrip trip={await getSampleTrip()} asOf={SAMPLE_TODAY} />);
    expect(screen.getByText("Shared trip, as of 18 Nov 2026")).toBeInTheDocument();
    expect(screen.getAllByText(/, as of 18 Nov 2026/).length).toBeGreaterThan(1);
  });

  it.each([
    ["no date", undefined],
    ["a null date", null],
    ["a date that cannot be read", "not a date"],
    ["an empty date", ""],
  ])("with %s, says Shared trip with no date and invents none", async (_name, asOf) => {
    const { container } = render(<SharedTrip trip={await ownTrip()} asOf={asOf} />);
    expect(screen.getByText("Shared trip")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/as of|frozen on/);
    expect(
      screen.getByText(
        "This is a copy of a trip. Fares and advice can change, so check each source before you plan around it.",
      ),
    ).toBeInTheDocument();
  });

  it("reads a date given as text from the share settings", async () => {
    render(<SharedTrip trip={await ownTrip()} asOf="2026-12-01T10:00:00Z" />);
    expect(screen.getByText("Shared trip, as of 1 Dec 2026")).toBeInTheDocument();
  });

  it("names a chosen hotel even when no listed hotel matches it, and never says skipped", async () => {
    const trip = await ownTrip();
    const stay = { ...trip.stay!, selection: "chosen" as const, chosen_hotel: "Hotel Nowhere" };
    render(<SharedTrip trip={{ ...trip, stay }} asOf={SAMPLE_TODAY} />);
    expect(screen.getByText(/Hotel Nowhere/)).toBeInTheDocument();
    expect(screen.queryByText(/skipped/)).not.toBeInTheDocument();
  });

  it("names a changed hotel with its area when a row matches", async () => {
    const trip = await ownTrip();
    const stay = {
      ...trip.stay!,
      selection: "changed" as const,
      chosen_hotel: "Sample Guesthouse Baixa",
    };
    render(<SharedTrip trip={{ ...trip, stay }} asOf={SAMPLE_TODAY} />);
    expect(screen.getByText(/Sample Guesthouse Baixa, Baixa\./)).toBeInTheDocument();
  });

  it("with a chosen hotel and no name, says its name is not known, not that it was skipped", async () => {
    const trip = await ownTrip();
    const stay = { ...trip.stay!, selection: "chosen" as const, chosen_hotel: null };
    render(<SharedTrip trip={{ ...trip, stay }} asOf={SAMPLE_TODAY} />);
    expect(screen.queryByText(/skipped/)).not.toBeInTheDocument();
    expect(screen.getByText("A hotel was chosen. Its name is not known.")).toBeInTheDocument();
  });

  it("says skipped only when the hotel was skipped", async () => {
    const trip = await ownTrip();
    const stay = { ...trip.stay!, selection: "skipped" as const, chosen_hotel: null };
    render(<SharedTrip trip={{ ...trip, stay }} asOf={SAMPLE_TODAY} />);
    expect(
      screen.getByText("You skipped the hotel. Days start from the centre of Lisbon."),
    ).toBeInTheDocument();
  });

  it("says Compared 1 place, not 1 places", async () => {
    const trip = await ownTrip();
    const cards = trip.comparison!.cards!.slice(0, 1);
    const comparison = { ...trip.comparison!, cards, chosen_place: null };
    render(<SharedTrip trip={{ ...trip, comparison }} asOf={SAMPLE_TODAY} />);
    expect(screen.getByText("Compared 1 place")).toBeInTheDocument();
  });
});
