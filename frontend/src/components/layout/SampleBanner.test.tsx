import { render, screen } from "@testing-library/react";

import { SampleBanner } from "./SampleBanner";

describe("SampleBanner", () => {
  it("shows the label Sample trip", () => {
    render(<SampleBanner />);
    expect(screen.getByText("Sample trip")).toBeInTheDocument();
  });
});
