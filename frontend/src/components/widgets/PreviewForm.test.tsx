import { fireEvent, render, screen } from "@testing-library/react";

import { PreviewForm } from "./PreviewForm";

describe("PreviewForm", () => {
  it("shows its children and passes the class name on", () => {
    render(
      <PreviewForm className="budget-form">
        <label>
          Budget
          <input defaultValue="500" />
        </label>
      </PreviewForm>,
    );
    expect(screen.getByLabelText("Budget")).toHaveValue("500");
    expect(screen.getByLabelText("Budget").closest("form")).toHaveClass("budget-form");
  });

  it("does nothing when submitted: the page does not navigate and the field keeps its value", () => {
    render(
      <PreviewForm>
        <input aria-label="Budget" defaultValue="500" />
        <button type="submit">Save</button>
      </PreviewForm>,
    );
    const form = screen.getByLabelText("Budget").closest("form")!;
    // fireEvent returns false when a handler called preventDefault(). A real submit with the
    // default left in place would reload the page.
    const notPrevented = fireEvent.submit(form);
    expect(notPrevented).toBe(false);
    expect(screen.getByLabelText("Budget")).toHaveValue("500");
  });
});
