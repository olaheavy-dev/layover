import { render, screen } from "@testing-library/react";

import type { SampleWidget } from "@/lib/samples";

import { Widget } from "./Widget";

describe("Widget", () => {
  it("shows Not known for a kind it does not know, and does not throw", () => {
    const unknown = {
      kind: "teleporter",
      state: "filled",
      sources: [],
    } as unknown as SampleWidget["widget"];
    expect(() => render(<Widget widget={unknown} />)).not.toThrow();
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText("This part of the trip can't be shown")).toBeInTheDocument();
  });
});
