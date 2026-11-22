import { render, screen } from "@testing-library/react";

import { LimitReached } from "./LimitReached";

describe("LimitReached", () => {
  it("shows the board's notice as a status", () => {
    render(<LimitReached />);
    const notice = screen.getByRole("status");
    expect(notice).toHaveTextContent("You have reached the limit for planning");
    expect(notice).toHaveTextContent(
      "Layover limits how much each visitor can plan. You can plan again when the limit resets, later on.",
    );
    expect(notice).toHaveTextContent("Your trip is still here. You can read it and share it.");
  });

  it("has a heading that names the notice", () => {
    render(<LimitReached />);
    expect(screen.getByRole("heading", { name: "You have reached the limit for planning" }));
    expect(screen.getByRole("status")).toHaveAccessibleName(
      "You have reached the limit for planning",
    );
  });
});
