import { render, screen } from "@testing-library/react";

import { getSampleTrip } from "@/lib/samples";

import SharedPage, { generateMetadata } from "./page";

vi.mock("@/lib/samples", async (original) => ({
  ...(await original<object>()),
  getSampleTrip: vi.fn((await original<typeof import("@/lib/samples")>()).getSampleTrip),
}));

async function open(shareId: string) {
  return render(await SharedPage({ params: Promise.resolve({ shareId }) }));
}

describe("/s/{share_id}", () => {
  it("shows the sample trip with the Sample trip label, the as-of header and one h1", async () => {
    await open("sample-lisbon");
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Lisbon, May");
    expect(screen.getAllByText("Sample trip").length).toBeGreaterThan(0);
    expect(screen.getByText("Shared trip, as of 18 Nov 2026")).toBeInTheDocument();
    expect(
      screen.getByText(
        "This is a copy of a trip, frozen on 18 Nov 2026. Fares and advice can change after that date, so check each source before you plan around it.",
      ),
    ).toBeInTheDocument();
  });

  it("links to Plan your own trip", async () => {
    await open("sample-lisbon");
    for (const link of screen.getAllByRole("link", { name: "Plan your own trip" })) {
      expect(link).toHaveAttribute("href", "/");
    }
  });

  it("has no Edit, Choose, Add, Swap, Share or New trip buttons and no chat", async () => {
    await open("sample-lisbon");
    const names = screen.queryAllByRole("button").map((b) => b.textContent ?? "");
    expect(
      names.filter((n) => /edit|choose|add|swap|share|new trip|stay here|approve/i.test(n)),
    ).toEqual([]);
    expect(screen.queryByRole("button", { name: /wider area|try again/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(screen.queryByRole("tab")).not.toBeInTheDocument();
  });

  it("shows no budget or traveller chips and no under or over budget line", async () => {
    // include_budget_and_travellers is false in the sample (schemas/samples/trip/sample-lisbon.json).
    await open("sample-lisbon");
    expect(screen.queryByText(/budget/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/adults/i)).not.toBeInTheDocument();
    expect(screen.queryByText("£800 in total")).not.toBeInTheDocument();
    expect(screen.getByText("From Manchester (MAN)")).toBeInTheDocument();
  });

  it("shows each age as of the share date", async () => {
    await open("sample-lisbon");
    expect(screen.getAllByText("Cached, 3 days old, as of 18 Nov 2026").length).toBeGreaterThan(0);
  });

  it("shows the sections but not Booking, and no Compare choice", async () => {
    await open("sample-lisbon");
    const index = screen.getByRole("navigation", { name: "Sections of the trip" });
    expect(index).not.toHaveTextContent("Booking");
    expect(screen.getByText("Compared 3 places: you chose Lisbon")).toBeInTheDocument();
  });

  it("rejects any other id as not found", async () => {
    await expect(SharedPage({ params: Promise.resolve({ shareId: "abc" }) })).rejects.toMatchObject(
      {
        digest: "NEXT_HTTP_ERROR_FALLBACK;404",
      },
    );
  });

  it("titles the page from the trip name, with Layover last", async () => {
    expect(
      await generateMetadata({ params: Promise.resolve({ shareId: "sample-lisbon" }) }),
    ).toEqual({ title: "Shared trip: Lisbon, May" });
  });

  it("fails when the API cannot give the sample trip, so the error page shows", async () => {
    vi.mocked(getSampleTrip).mockRejectedValueOnce(new Error("The sample trip could not be read."));
    await expect(open("sample-lisbon")).rejects.toThrow("could not be read");
  });
});
