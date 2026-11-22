import { render, screen } from "@testing-library/react";

import { BriefSummary } from "./BriefSummary";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

const CHIPS = [
  "From Manchester (MAN)",
  "May 2027 · 5 nights",
  "2 adults",
  "£800 in total",
  "Warm, relaxed, good food",
];

describe("BriefSummary", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("brief_summary")).sort()).toEqual([
      "confirmed",
      "editing",
      "filled",
      "loading",
      "waiting",
    ]);
  });

  it("loading: shows a busy status and no chips", async () => {
    render(<BriefSummary widget={await sampleOf("brief_summary", "loading")} />);
    expect(screen.getByRole("heading", { name: "Your brief" })).toBeInTheDocument();
    expect(screen.getByRole("status")).toHaveTextContent("Loading Your brief");
    expect(screen.queryByText("2 adults")).not.toBeInTheDocument();
  });

  it.each(["filled", "waiting"])(
    "%s: every field as a chip, with Confirm and Edit",
    async (state) => {
      render(<BriefSummary widget={await sampleOf("brief_summary", state)} />);
      for (const chip of CHIPS)
        expect(screen.getByRole("button", { name: `${chip} (edit)` })).toBeInTheDocument();
      expect(screen.getByText("Waiting for your OK")).toBeInTheDocument();
      expect(screen.getByText(/Nothing is searched until you confirm/)).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Confirm brief" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Edit brief" })).toBeInTheDocument();
    },
  );

  it("editing: the budget chip becomes a field with Save and Cancel", async () => {
    render(<BriefSummary widget={await sampleOf("brief_summary", "editing")} />);
    expect(screen.getByLabelText("Budget")).toHaveValue("£800");
    expect(screen.getByRole("button", { name: "Save" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Cancel" })).toBeInTheDocument();
    expect(screen.getByText(/Press Enter to save/)).toBeInTheDocument();
    expect(screen.queryByText("£800 in total")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /From Manchester/ })).toBeInTheDocument();
  });

  it("confirmed: plain chips, 'Confirmed by you' and an Edit button", async () => {
    render(<BriefSummary widget={await sampleOf("brief_summary", "confirmed")} />);
    for (const chip of CHIPS) expect(screen.getByText(chip)).toBeInTheDocument();
    expect(screen.getByText("Confirmed by you")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Edit" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Confirm brief" })).not.toBeInTheDocument();
  });

  it("leaves out a chip for a field that is missing, and never guesses one", async () => {
    const widget = {
      ...(await sampleOf("brief_summary", "confirmed")),
      budget: null,
      adults: null,
    };
    render(<BriefSummary widget={widget} />);
    expect(screen.queryByText(/in total/)).not.toBeInTheDocument();
    expect(screen.queryByText(/adult/)).not.toBeInTheDocument();
    expect(screen.getByText("From Manchester (MAN)")).toBeInTheDocument();
  });

  it("says 1 adult and 1 night in the singular", async () => {
    const widget = { ...(await sampleOf("brief_summary", "confirmed")), adults: 1, nights: 1 };
    render(<BriefSummary widget={widget} />);
    expect(screen.getByText("1 adult")).toBeInTheDocument();
    expect(screen.getByText("May 2027 · 1 night")).toBeInTheDocument();
  });
});
