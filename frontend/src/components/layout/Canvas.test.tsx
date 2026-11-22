import { act, render, screen } from "@testing-library/react";

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

  it("marks the first section until another comes into view", () => {
    render(
      <Canvas sections={["brief", "compare"]}>
        <section id="brief">Brief content</section>
        <section id="compare">Compare content</section>
      </Canvas>,
    );
    expect(screen.getByRole("link", { name: "Brief" })).toHaveAttribute("aria-current", "true");
    expect(screen.getByRole("link", { name: "Compare" })).not.toHaveAttribute("aria-current");
  });

  it("marks the last section that crosses the reading line, as the page scrolls", () => {
    type Callback = (entries: Partial<IntersectionObserverEntry>[]) => void;
    let notify: Callback = () => {};
    vi.stubGlobal(
      "IntersectionObserver",
      class {
        constructor(callback: Callback) {
          notify = callback;
        }
        observe() {}
        disconnect() {}
      },
    );
    try {
      render(
        <Canvas sections={["brief", "compare", "days"]}>
          <section id="brief">Brief content</section>
          <section id="compare">Compare content</section>
          <section id="days">Days content</section>
        </Canvas>,
      );
      const target = (id: string) => document.getElementById(id) as Element;
      act(() => notify([{ target: target("compare"), isIntersecting: true }]));
      expect(screen.getByRole("link", { name: "Compare" })).toHaveAttribute("aria-current", "true");
      act(() => notify([{ target: target("days"), isIntersecting: true }]));
      expect(screen.getByRole("link", { name: "Days" })).toHaveAttribute("aria-current", "true");
      expect(
        screen.getAllByRole("link").filter((l) => l.hasAttribute("aria-current")),
      ).toHaveLength(1);
      // Both on the line at once: the later one in the journey wins.
      act(() =>
        notify([
          { target: target("compare"), isIntersecting: true },
          { target: target("days"), isIntersecting: false },
        ]),
      );
      expect(screen.getByRole("link", { name: "Compare" })).toHaveAttribute("aria-current", "true");
    } finally {
      vi.unstubAllGlobals();
    }
  });

  it("an explicit current section wins over the scroll position", () => {
    render(
      <Canvas sections={["brief", "compare"]} current="compare">
        <section id="brief">Brief content</section>
        <section id="compare">Compare content</section>
      </Canvas>,
    );
    expect(screen.getByRole("link", { name: "Compare" })).toHaveAttribute("aria-current", "true");
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
