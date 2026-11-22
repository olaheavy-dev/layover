import { fireEvent, render, screen } from "@testing-library/react";

import { PhoneTabs } from "./PhoneTabs";

describe("PhoneTabs", () => {
  it("shows Chat and Trip tabs and selects the current one", () => {
    render(<PhoneTabs view="chat" onViewChange={() => {}} />);
    const chat = screen.getByRole("tab", { name: "Chat" });
    expect(chat).toHaveAttribute("aria-selected", "true");
    expect(screen.getByRole("tab", { name: "Trip" })).toHaveAttribute("aria-selected", "false");
  });

  it("shows the badge text and reads it out as part of the Trip tab name", () => {
    render(<PhoneTabs view="chat" onViewChange={() => {}} newCount={3} />);
    expect(screen.getByText("3 new")).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: "Trip 3 new" })).toBeInTheDocument();
  });

  it("shows no badge when nothing is new", () => {
    render(<PhoneTabs view="chat" onViewChange={() => {}} newCount={0} />);
    expect(screen.queryByText(/new$/)).not.toBeInTheDocument();
  });

  it("calls onViewChange when a tab is pressed", () => {
    const onViewChange = vi.fn();
    render(<PhoneTabs view="chat" onViewChange={onViewChange} />);
    fireEvent.click(screen.getByRole("tab", { name: "Trip" }));
    expect(onViewChange).toHaveBeenCalledWith("trip");
  });

  it("moves between tabs with the arrow keys", () => {
    const onViewChange = vi.fn();
    render(<PhoneTabs view="chat" onViewChange={onViewChange} />);
    fireEvent.keyDown(screen.getByRole("tab", { name: "Chat" }), { key: "ArrowRight" });
    expect(onViewChange).toHaveBeenCalledWith("trip");
  });

  it("only the selected tab is in the tab order", () => {
    render(<PhoneTabs view="trip" onViewChange={() => {}} />);
    expect(screen.getByRole("tab", { name: "Trip" })).toHaveAttribute("tabindex", "0");
    expect(screen.getByRole("tab", { name: "Chat" })).toHaveAttribute("tabindex", "-1");
  });
});
