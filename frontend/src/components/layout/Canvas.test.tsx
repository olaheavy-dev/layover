import { act, fireEvent, render, screen } from "@testing-library/react";

import { Canvas, readingBand } from "./Canvas";

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

describe("readingBand", () => {
  // Working: the band runs from 48 px (under the sticky index) to 10% of the canvas height, but is
  // never thinner than 16 px. The bottom margin is what is left under the band's end.
  // Source: the IntersectionObserver spec (w3c.github.io/IntersectionObserver, rootMargin): a
  // percentage is of the root's width, so the height is turned into pixels here instead.
  it.each([
    // height 650: 10% = 65 (more than 48 + 16 = 64), bottom = 650 - 65 = 585
    [650, "-48px 0px -585px 0px"],
    // height 1000: 10% = 100, bottom = 900
    [1000, "-48px 0px -900px 0px"],
    // height 400: 10% = 40, below 64, so the band ends at 64; bottom = 400 - 64 = 336
    [400, "-48px 0px -336px 0px"],
    // height 60: shorter than the band's end; bottom 0
    [60, "-48px 0px 0px 0px"],
  ])("for a canvas %i px high is %s", (height, margin) => {
    expect(readingBand(height)).toBe(margin);
  });
});
