import { fireEvent, render, screen } from "@testing-library/react";

import { ChatColumn } from "./ChatColumn";

describe("ChatColumn", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("shows the four example prompts and the message box", () => {
    render(<ChatColumn />);
    const group = screen.getByRole("group", { name: "Or try one of these" });
    expect(group.querySelectorAll("button")).toHaveLength(4);
    expect(
      screen.getByRole("button", { name: "Somewhere warm in May, not sure where" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Do I need a visa for Turkey?" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Three days in Porto" })).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Cheapest flights from Bristol in March" }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText("Message to Layover")).toBeInTheDocument();
  });

  it("says the chat isn't connected yet when a message is sent, and makes no network call", () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    render(<ChatColumn />);
    fireEvent.change(screen.getByLabelText("Message to Layover"), { target: { value: "Hello" } });
    fireEvent.click(screen.getByRole("button", { name: "Send" }));
    expect(screen.getByText("The chat isn't connected yet")).toBeInTheDocument();
    expect(screen.getByText("Hello")).toBeInTheDocument();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("gives the same answer for an example prompt, with no network call", () => {
    const fetchSpy = vi.spyOn(globalThis, "fetch");
    render(<ChatColumn />);
    fireEvent.click(screen.getByRole("button", { name: "Three days in Porto" }));
    expect(screen.getByText("The chat isn't connected yet")).toBeInTheDocument();
    expect(fetchSpy).not.toHaveBeenCalled();
  });

  it("ignores an empty message", () => {
    render(<ChatColumn />);
    fireEvent.click(screen.getByRole("button", { name: "Send" }));
    expect(screen.queryByText("The chat isn't connected yet")).not.toBeInTheDocument();
  });

  it("clears the box after sending", () => {
    render(<ChatColumn />);
    const input = screen.getByLabelText("Message to Layover");
    fireEvent.change(input, { target: { value: "Hello" } });
    fireEvent.click(screen.getByRole("button", { name: "Send" }));
    expect(input).toHaveValue("");
  });

  it("shows the trip strip above the message box when one is given", () => {
    render(<ChatColumn strip={<p>strip here</p>} />);
    expect(screen.getByText("strip here")).toBeInTheDocument();
  });

  it("keeps the welcome outside the live log, so it is not announced on mount", () => {
    render(<ChatColumn />);
    const log = screen.getByRole("log", { name: "Conversation with Layover" });
    expect(log).not.toContainElement(screen.getByRole("heading", { name: "Where to next?" }));
    expect(log).not.toContainElement(screen.getByRole("group", { name: "Or try one of these" }));
  });

  it("puts messages inside the log", () => {
    render(<ChatColumn />);
    fireEvent.change(screen.getByLabelText("Message to Layover"), { target: { value: "Hello" } });
    fireEvent.click(screen.getByRole("button", { name: "Send" }));
    const log = screen.getByRole("log", { name: "Conversation with Layover" });
    expect(log).toContainElement(screen.getByText("Hello"));
    expect(log).toContainElement(screen.getByText("The chat isn't connected yet"));
  });

  it("cancels the column's gap while the log is empty, and not once there are messages", () => {
    render(<ChatColumn />);
    const log = screen.getByRole("log", { name: "Conversation with Layover" });
    expect(log).toHaveClass("-mt-3");
    fireEvent.change(screen.getByLabelText("Message to Layover"), { target: { value: "Hello" } });
    fireEvent.click(screen.getByRole("button", { name: "Send" }));
    expect(log).not.toHaveClass("-mt-3");
  });

  it("makes the scrolling chat a focusable region, so the keyboard can scroll it", () => {
    render(<ChatColumn />);
    const region = screen.getByRole("region", { name: "Chat messages and examples" });
    expect(region).toHaveAttribute("tabindex", "0");
    expect(region).toContainElement(screen.getByRole("group", { name: "Or try one of these" }));
    expect(region).toContainElement(screen.getByRole("log"));
    // The message box stays outside it, always visible.
    expect(region).not.toContainElement(screen.getByLabelText("Message to Layover"));
    region.focus();
    expect(region).toHaveFocus();
  });
});
