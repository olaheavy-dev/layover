import { render, screen } from "@testing-library/react";

import { Canvas } from "./Canvas";

describe("Canvas", () => {
  it("shows its sections and the section index", () => {
    render(
      <Canvas sections={["brief", "compare"]} current="brief">
        <section id="brief">Brief content</section>
      </Canvas>,
    );
    expect(screen.getByRole("region", { name: "Your trip" })).toBeInTheDocument();
    expect(screen.getByText("Brief content")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "Compare" })).toBeInTheDocument();
  });

  it("shows the empty state with the honesty line and a link to How Layover works", () => {
    render(<Canvas />);
    expect(screen.getByRole("heading", { name: "Your trip" })).toBeInTheDocument();
    expect(
      screen.getByText("Your plan, prices and place facts appear here as we talk."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Every figure shows where it came from and how old it is."),
    ).toBeInTheDocument();
    expect(screen.getByRole("link", { name: "How Layover works" })).toHaveAttribute(
      "href",
      "/how-it-works",
    );
    expect(screen.queryByRole("navigation")).not.toBeInTheDocument();
  });
});
