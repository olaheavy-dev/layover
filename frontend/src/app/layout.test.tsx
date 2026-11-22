import { metadata } from "./layout";

// The fonts are Next.js build-time loaders, which a unit test cannot run.
vi.mock("./fonts", () => ({ sourceSans: { variable: "" }, sourceSerif: { variable: "" } }));

// WCAG 2.4.2 (Page Titled): every page has its own title, with Layover's name last, as the boards do.
describe("the page titles", () => {
  it("gives a page with no title of its own the welcome board's, and ends the others with Layover", () => {
    expect(metadata.title).toEqual({
      default: "Where to next? A new trip · Layover",
      template: "%s · Layover",
    });
  });

  it("describes Layover in one plain line, not the template's placeholder", () => {
    expect(metadata.description).toBe("An AI travel planner for people in the UK.");
  });
});
