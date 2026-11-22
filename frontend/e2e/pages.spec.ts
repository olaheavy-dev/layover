import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

// Every page of the product, so each is checked for accessibility, CSP violations and errors in
// light, dark and mobile, and compared with its screenshot. Add each new page here (with real ids
// for dynamic routes), then make its screenshots with `make screenshots-frontend`.
const PAGES = [
  "/",
  "/trip/sample-lisbon",
  "/s/sample-lisbon",
  "/how-it-works",
  "/trip/abc",
  "/dev/widgets",
];

// WCAG 2.2 A and AA, as axe tags them.
const WCAG = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"];

declare global {
  interface Window {
    cspViolations: string[];
  }
}

test.beforeEach(async ({ page }) => {
  // Injected by the browser's debugger, so the page's own policy doesn't block it.
  await page.addInitScript(() => {
    window.cspViolations = [];
    document.addEventListener("securitypolicyviolation", (event) => {
      window.cspViolations.push(`${event.violatedDirective} ${event.blockedURI}`);
    });
  });
});

function screenshotName(path: string) {
  return path === "/" ? "home" : path.slice(1).replaceAll("/", "-");
}

for (const path of PAGES) {
  test(`${path} is accessible and runs within its CSP`, async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (error) => errors.push(error.message));

    await page.goto(path);
    await page.waitForLoadState("networkidle");

    const { violations } = await new AxeBuilder({ page }).withTags(WCAG).analyze();
    expect(violations.map(({ id, help, nodes }) => ({ id, help, nodes: nodes.length }))).toEqual(
      [],
    );
    expect(await page.evaluate(() => window.cspViolations)).toEqual([]);
    expect(errors).toEqual([]);
    await expect(page.getByRole("heading", { level: 1 })).toHaveCount(1);
    // The development gallery is a very tall page of every widget state: one image of it would pass
    // the repository's 1 MB file limit, so it is shot one section at a time (below).
    if (path === "/dev/widgets") return;
    // Compared only in Playwright's Linux image (see playwright.config.ts).
    await expect(page).toHaveScreenshot(`${screenshotName(path)}.png`, { fullPage: true });
  });
}

// The gallery, one image for each kind of widget and one for the limit-reached notice, in light,
// dark and phone width (issue #54). Each image stays well under 1 MB.
test("/dev/widgets: each section matches its screenshot", async ({ page }) => {
  await page.goto("/dev/widgets");
  await page.waitForLoadState("networkidle");
  const sections = page.locator('section[aria-labelledby^="kind-"]');
  const count = await sections.count();
  expect(count).toBeGreaterThan(10);
  for (let index = 0; index < count; index++) {
    const section = sections.nth(index);
    const kind = (await section.getAttribute("aria-labelledby"))!.replace("kind-", "");
    await expect(section).toHaveScreenshot(`dev-widgets-${kind}.png`);
  }
});

// Every page fits the screen: the page never scrolls sideways, and no text or box inside the page
// is cut off or sticks out of its container, unless it is meant to scroll or to end in "...".
for (const path of PAGES) {
  test(`${path} fits the screen width`, async ({ page }) => {
    await page.goto(path);
    await page.waitForLoadState("networkidle");
    const { scroll, inner } = await page.evaluate(() => ({
      scroll: document.documentElement.scrollWidth,
      inner: window.innerWidth,
    }));
    expect(scroll).toBeLessThanOrEqual(inner);
    const wide = await page.evaluate(() =>
      [...document.querySelectorAll("main *:not(svg *)")]
        .filter((element) => {
          const style = getComputedStyle(element);
          const scrolls = style.overflowX === "auto" || style.overflowX === "scroll";
          return (
            element.clientWidth > 1 &&
            element.scrollWidth > element.clientWidth &&
            !scrolls &&
            style.textOverflow !== "ellipsis"
          );
        })
        .map(
          (element) =>
            `${element.tagName.toLowerCase()} (${element.scrollWidth} > ${element.clientWidth}): ${element.textContent?.slice(0, 60)}`,
        ),
    );
    expect(wide).toEqual([]);
  });
}

// Each page says what it is in its tab (WCAG 2.4.2), with Layover's name last, as the boards do.
const TITLES: Record<string, string> = {
  "/": "Where to next? A new trip · Layover",
  "/trip/sample-lisbon": "Lisbon, May · Layover",
  "/s/sample-lisbon": "Shared trip: Lisbon, May · Layover",
  "/how-it-works": "How Layover works · Layover",
  "/trip/abc": "Link not found · Layover",
  "/dev/widgets": "Widget gallery · Layover",
};
for (const [path, title] of Object.entries(TITLES)) {
  test(`${path} is titled "${title}"`, async ({ page }) => {
    await page.goto(path);
    await expect(page).toHaveTitle(title);
  });
}

// The two typefaces are served from this repository. A family name that is not valid CSS makes the
// browser drop the @font-face rule without an error, so check that each face really loads.
test("the Source Serif 4 and Source Sans 3 fonts load", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  const loaded = async () =>
    page.evaluate(async () => {
      await document.fonts.ready;
      return [...document.fonts]
        .filter((face) => face.status === "loaded")
        .map((face) => face.family.replaceAll('"', ""));
    });
  await expect.poll(loaded).toEqual(expect.arrayContaining(["Source Serif 4", "Source Sans 3"]));
});
