import { render, screen } from "@testing-library/react";

import { NotKnownWidget } from "./NotKnownWidget";
import { sampleOf, sampleStates } from "./testing";

// Source: schemas/samples/widgets/not_known, and the "Not known" section of
// docs/design/boards/screens/widgets-journey.html.
describe("NotKnownWidget", () => {
  it("is tested against every sample state", async () => {
    expect(await sampleStates("not_known")).toEqual(["not_known"]);
  });

  it("not_known: the label, what is missing, why, and what Layover can do", async () => {
    const { container } = render(
      <NotKnownWidget widget={await sampleOf("not_known", "not_known")} />,
    );
    expect(screen.getByRole("heading", { name: "Local bus fares in Lisbon" })).toBeInTheDocument();
    expect(screen.getByText("Not known")).toBeInTheDocument();
    expect(screen.getByText("What is missing")).toBeInTheDocument();
    expect(screen.getByText("Why")).toBeInTheDocument();
    expect(screen.getByText("What Layover can do")).toBeInTheDocument();
    expect(screen.getByText("None of the sources Layover uses has them")).toBeInTheDocument();
    expect(
      screen.getByText(
        "Show the cost estimate without them, with local transport marked Not known",
      ),
    ).toBeInTheDocument();
    expect(container.querySelector("footer")).toBeNull();
  });

  it("leaves out a row the contract does not give, and invents no reason", async () => {
    const widget = {
      ...(await sampleOf("not_known", "not_known")),
      reason: null,
      instead: null,
    };
    render(<NotKnownWidget widget={widget} />);
    expect(screen.queryByText("Why")).toBeNull();
    expect(screen.queryByText("What Layover can do")).toBeNull();
    expect(screen.getByText("What is missing")).toBeInTheDocument();
  });

  it("with no missing text, the title is just Not known", async () => {
    const widget = { ...(await sampleOf("not_known", "not_known")), missing: null };
    render(<NotKnownWidget widget={widget} />);
    expect(screen.getByRole("heading", { name: "Not known" })).toBeInTheDocument();
  });
});
