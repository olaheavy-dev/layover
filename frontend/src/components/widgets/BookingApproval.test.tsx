import { render, screen } from "@testing-library/react";

import { BookingApproval } from "./BookingApproval";
import { sampleOf, sampleStates, TEST_NOW } from "./testing";

beforeAll(() => {
  vi.useFakeTimers({ toFake: ["Date"] });
  vi.setSystemTime(TEST_NOW);
});
afterAll(() => vi.useRealTimers());

const SANDBOX = "Sandbox: no real booking or payment";
const STATES = [
  "approved",
  "declined",
  "empty",
  "error",
  "filled",
  "flights_only",
  "loading",
  "price_changed",
  "waiting",
];

describe("BookingApproval", () => {
  it("is tested against every sample state", async () => {
    expect((await sampleStates("booking_approval")).sort()).toEqual(STATES);
  });

  it.each(STATES)("%s: always shows the sandbox notice", async (state) => {
    render(<BookingApproval widget={await sampleOf("booking_approval", state)} />);
    expect(screen.getByRole("heading", { name: "Try booking" })).toBeInTheDocument();
    expect(screen.getByText(SANDBOX)).toBeInTheDocument();
  });

  it("loading: a busy status and no buttons, so nothing can be approved", async () => {
    render(<BookingApproval widget={await sampleOf("booking_approval", "loading")} />);
    expect(screen.getByRole("status")).toHaveTextContent("Loading Try booking");
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it.each(["filled", "waiting"])(
    "%s: the summary, the sandbox price and equal Approve and Decline",
    async (state) => {
      render(<BookingApproval widget={await sampleOf("booking_approval", state)} />);
      expect(screen.getByText("Waiting for your approval")).toBeInTheDocument();
      expect(screen.getByText("MAN to LIS")).toBeInTheDocument();
      expect(screen.getByText("14 May 2027")).toBeInTheDocument();
      expect(screen.getByText("19 May 2027")).toBeInTheDocument();
      expect(screen.getByText("2 adults")).toBeInTheDocument();
      expect(screen.getByText("£192 for 2")).toBeInTheDocument();
      expect(screen.getByText(/Sandbox price, not the fare above/)).toBeInTheDocument();
      expect(screen.getByText("Nothing is ordered until you press Approve.")).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Approve" })).toBeInTheDocument();
      expect(screen.getByRole("button", { name: "Decline" })).toBeInTheDocument();
      expect(screen.getByText("Live")).toBeInTheDocument();
      expect(screen.getByText("Duffel sandbox")).toBeInTheDocument();
    },
  );

  it("approved: the sandbox order and a plain 'no real booking' line, with no buttons", async () => {
    render(<BookingApproval widget={await sampleOf("booking_approval", "approved")} />);
    expect(screen.getByText("Approved. Sandbox order SANDBOX-0001.")).toBeInTheDocument();
    expect(
      screen.getByText("No real booking was made and no payment was taken."),
    ).toBeInTheDocument();
    expect(screen.getByText("£192 for 2")).toBeInTheDocument();
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("declined: nothing was ordered, with Search again", async () => {
    render(<BookingApproval widget={await sampleOf("booking_approval", "declined")} />);
    expect(screen.getByText("Declined. Nothing was ordered.")).toBeInTheDocument();
    expect(screen.getByText("MAN to LIS, 14 to 19 May 2027, 2 adults.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Search again" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Approve" })).not.toBeInTheDocument();
  });

  it("price_changed: both prices in words, a new Approve button at the new price", async () => {
    render(<BookingApproval widget={await sampleOf("booking_approval", "price_changed")} />);
    expect(screen.getByText("The price changed")).toBeInTheDocument();
    expect(
      screen.getByText("The price changed at the price check. Layover asks again."),
    ).toBeInTheDocument();
    expect(screen.getByText("Price you saw")).toBeInTheDocument();
    expect(screen.getByText("£192 for 2")).toBeInTheDocument();
    expect(screen.getByText("Price now")).toBeInTheDocument();
    expect(screen.getByText("£204 for 2")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Nothing is ordered. Approve only if £204 for 2 is fine for you. These are sandbox prices, not the fare above.",
      ),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Approve at £204" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Decline" })).toBeInTheDocument();
  });

  it("price_changed with no new price: no Approve button and the new price says Not known", async () => {
    const widget = { ...(await sampleOf("booking_approval", "price_changed")), new_price: null };
    render(<BookingApproval widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /Approve/ })).not.toBeInTheDocument();
  });

  it("flights_only: says a hotel cannot be added yet", async () => {
    render(<BookingApproval widget={await sampleOf("booking_approval", "flights_only")} />);
    expect(
      screen.getByText("Flights only. Layover cannot add a hotel to the sandbox booking yet."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Approve" })).toBeInTheDocument();
  });

  it("empty: says the sandbox has no offer, with Edit brief and an Aviasales link", async () => {
    render(<BookingApproval widget={await sampleOf("booking_approval", "empty")} />);
    expect(
      screen.getByText("The sandbox has no offer for MAN to LIS on 14 May 2027."),
    ).toBeInTheDocument();
    expect(screen.getByText(/Nothing was ordered/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Edit brief" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Look on Aviasales/ })).toHaveAttribute(
      "href",
      "https://www.aviasales.com/",
    );
  });

  it("error: Unavailable, what failed, Try again and no price", async () => {
    const { container } = render(
      <BookingApproval widget={await sampleOf("booking_approval", "error")} />,
    );
    expect(screen.getAllByText("Unavailable").length).toBeGreaterThan(0);
    expect(
      screen.getByText("Layover could not reach the Duffel sandbox just now. Nothing was ordered."),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Try again" })).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/£/);
  });

  it("shows Not known for a price that is missing, never zero, and offers no Approve", async () => {
    const widget = { ...(await sampleOf("booking_approval", "waiting")), sandbox_price: null };
    const { container } = render(<BookingApproval widget={widget} />);
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/£/);
    expect(screen.queryByRole("button", { name: /Approve/ })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Decline" })).toBeInTheDocument();
  });
});
