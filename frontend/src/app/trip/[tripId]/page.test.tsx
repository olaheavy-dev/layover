import { fireEvent, render, screen, within } from "@testing-library/react";

import TripPage, { generateMetadata, generateStaticParams } from "./page";

async function open(tripId: string) {
  return render(await TripPage({ params: Promise.resolve({ tripId }) }));
}

describe("/trip/{trip_id}", () => {
  it("shows the sample trip with the Sample trip label and one h1", async () => {
    await open("sample-lisbon");
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("Lisbon, May");
    expect(screen.getAllByText("Sample trip").length).toBeGreaterThan(0);
  });

  it("shows the canvas sections in journey order, each in the section index", async () => {
    await open("sample-lisbon");
    const index = screen.getByRole("navigation", { name: "Sections of the trip" });
    expect(
      within(index)
        .getAllByRole("link")
        .map((a) => a.textContent),
    ).toEqual(["Brief", "Compare", "Lisbon", "Stay", "Days", "Booking"]);
    const canvas = screen.getByRole("region", { name: "Your trip" });
    for (const id of ["brief", "compare", "place", "stay", "days", "booking"]) {
      expect(canvas.querySelector(`section#${id}`)).not.toBeNull();
    }
  });

  it("puts the place's facts in the order of the information architecture", async () => {
    await open("sample-lisbon");
    const place = screen.getByRole("region", { name: "Your trip" }).querySelector("section#place");
    const titles = within(place as HTMLElement)
      .getAllByRole("heading", { level: 3 })
      .map((h) => h.textContent);
    // fare_card, cost_estimate, advice_card, climate_chart, money, sea_conditions, daylight, place_intro
    expect(titles.indexOf("Flights")).toBeLessThan(titles.indexOf("Cost estimate"));
    expect(titles.indexOf("Cost estimate")).toBeLessThan(titles.indexOf("Travel advice"));
  });

  it("keeps the working trip's actions, because it is not shared", async () => {
    await open("sample-lisbon");
    expect(screen.getByRole("button", { name: "Share trip" })).toBeInTheDocument();
  });

  it("switches between the Trip and Chat tabs on a phone", async () => {
    await open("sample-lisbon");
    const tab = screen.getByRole("tab", { name: "Chat" });
    expect(tab).toHaveAttribute("aria-selected", "false");
    fireEvent.click(tab);
    expect(tab).toHaveAttribute("aria-selected", "true");
    expect(document.getElementById("panel-trip")).toHaveClass("hidden");
  });

  it("rejects any other id as not found", async () => {
    await expect(TripPage({ params: Promise.resolve({ tripId: "abc" }) })).rejects.toMatchObject({
      digest: "NEXT_HTTP_ERROR_FALLBACK;404",
    });
  });

  it("titles the page from the trip name, with Layover last", async () => {
    expect(
      await generateMetadata({ params: Promise.resolve({ tripId: "sample-lisbon" }) }),
    ).toEqual({
      title: "Lisbon, May",
    });
  });

  it("opens on the Trip tab, because there is a trip to show", async () => {
    await open("sample-lisbon");
    expect(screen.getByRole("tab", { name: "Trip" })).toHaveAttribute("aria-selected", "true");
    expect(document.getElementById("panel-chat")).toHaveClass("hidden");
  });

  it("prerenders the sample id", async () => {
    expect(await generateStaticParams()).toEqual([{ tripId: "sample-lisbon" }]);
  });
});
