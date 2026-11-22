import { render, screen } from "@testing-library/react";

import HowItWorks from "./page";

describe("/how-it-works", () => {
  it("has one h1 and the six parts in order", () => {
    render(<HowItWorks />);
    expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
    expect(screen.getByRole("heading", { level: 1 })).toHaveTextContent("How Layover works");
    expect(screen.getAllByRole("heading", { level: 2 }).map((h) => h.textContent)).toEqual([
      "1. What Layover does",
      "2. The agent team",
      "3. The rules Layover keeps",
      "4. Where the data comes from",
      "5. How well it works",
      "6. Read the code",
    ]);
  });

  it("says there are no evaluation results yet and invents none", () => {
    render(<HowItWorks />);
    expect(screen.getByText("No evaluation results yet")).toBeInTheDocument();
    expect(screen.queryByText(/\d+(\.\d+)?\s*%/)).not.toBeInTheDocument();
  });

  it("lists the agent team, the six rules and each data source with its terms", () => {
    render(<HowItWorks />);
    expect(screen.getByRole("heading", { name: "Brief agent" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Booking" })).toBeInTheDocument();
    expect(screen.getAllByRole("heading", { level: 3 }).length).toBe(4 + 6 + 17);
    expect(screen.getByRole("link", { name: /Travelpayouts: Aviasales Data API/ })).toHaveAttribute(
      "href",
      "https://support.travelpayouts.com/hc/en-us/articles/203956163",
    );
  });

  it("links to the code on GitHub and to the section index anchors", () => {
    render(<HowItWorks />);
    expect(screen.getByRole("link", { name: /Layover on GitHub/ })).toHaveAttribute(
      "href",
      "https://github.com/olaheavy-dev/layover",
    );
    expect(screen.getByRole("link", { name: "Evaluation" })).toHaveAttribute("href", "#evaluation");
  });

  it("holds no Sample trip label, because it shows no sample trip", () => {
    render(<HowItWorks />);
    expect(screen.queryByText("Sample trip")).not.toBeInTheDocument();
  });
});
