import { expect, test } from "@playwright/test";

// What a visitor does on each page, against the production build. The accessibility, CSP and
// screenshot checks for every page are in pages.spec.ts.

test.describe("the sample trip", () => {
  test("/trip/sample-lisbon shows the trip, labelled as a sample", async ({ page }) => {
    const response = await page.goto("/trip/sample-lisbon");
    expect(response?.status()).toBe(200);
    await expect(page.getByRole("heading", { level: 1 })).toHaveText("Lisbon, May");
    await expect(page.getByText("Sample trip").first()).toBeVisible();
  });

  test("/trip/sample-lisbon opens the Trip tab on a phone", async ({ page, isMobile }) => {
    test.skip(!isMobile, "the tabs are for phones and tablets");
    await page.goto("/trip/sample-lisbon");
    await expect(page.getByRole("tab", { name: "Trip" })).toHaveAttribute("aria-selected", "true");
    await expect(page.getByRole("region", { name: "Your trip" })).toBeVisible();
    await expect(page.getByRole("heading", { level: 2, name: "Lisbon" })).toBeVisible();
  });

  for (const path of ["/trip/sample-lisbon", "/s/sample-lisbon"]) {
    test(`${path} marks the section in view in the index`, async ({ page }) => {
      await page.goto(path);
      const index = page.getByRole("navigation", { name: "Sections of the trip" });
      const current = index.locator('a[aria-current="true"]');
      await expect(current).toHaveCount(1);
      await expect(current).toHaveText("Brief");
      await page.evaluate(() => document.getElementById("days")?.scrollIntoView());
      await expect(current).toHaveText("Days");
      await expect(index.locator('a[aria-current="true"]')).toHaveCount(1);
    });
  }

  for (const path of ["/trip/sample-lisbon", "/s/sample-lisbon"]) {
    test(`${path} index click marks the last section and keeps the top bar on screen`, async ({
      page,
    }) => {
      await page.goto(path);
      const index = page.getByRole("navigation", { name: "Sections of the trip" });
      if (await page.getByRole("tab", { name: "Trip" }).isVisible()) {
        await page.getByRole("tab", { name: "Trip" }).click();
      }
      const last = index.getByRole("link").last();
      const name = (await last.textContent()) ?? "";
      await last.click();
      await expect(index.locator('a[aria-current="true"]')).toHaveCount(1);
      await expect(index.locator('a[aria-current="true"]')).toHaveText(name);
      const top = await page.getByRole("banner").evaluate((el) => el.getBoundingClientRect().top);
      expect(top).toBe(0);
    });
  }

  for (const path of ["/trip/sample-lisbon", "/s/sample-lisbon"]) {
    test(`${path} index link activated by keyboard moves focus to the section heading`, async ({
      page,
      isMobile,
    }) => {
      test.skip(isMobile, "a keyboard journey: desktop only");
      await page.goto(path);
      const index = page.getByRole("navigation", { name: "Sections of the trip" });
      const link = index.getByRole("link").nth(1);
      const target = ((await link.getAttribute("href")) ?? "").slice(1);
      await link.focus();
      await page.keyboard.press("Enter");
      await expect(page.locator(`#${target}-title`)).toBeFocused();
      await expect(link).toHaveAttribute("aria-current", "true");
      const top = await page.getByRole("banner").evaluate((el) => el.getBoundingClientRect().top);
      expect(top).toBe(0);
    });
  }

  for (const path of ["/trip/sample-lisbon", "/s/sample-lisbon"]) {
    test(`${path} index follows the scroll on a wide, short canvas`, async ({ page, isMobile }) => {
      test.skip(isMobile, "sets its own desktop viewport");
      await page.setViewportSize({ width: 1920, height: 560 });
      await page.goto(path);
      const index = page.getByRole("navigation", { name: "Sections of the trip" });
      // Scroll the "place" section's top to just under the sticky index, as a reader would.
      await page.evaluate(() => {
        const canvas = document.querySelector('section[aria-label="Your trip"]') as HTMLElement;
        const target = document.getElementById("place") as HTMLElement;
        canvas.scrollTop +=
          target.getBoundingClientRect().top - canvas.getBoundingClientRect().top - 50;
      });
      await expect(index.locator('a[aria-current="true"]')).toHaveText(/Lisbon|Place/);
    });
  }

  test("the trip name is not clipped on a phone", async ({ page, isMobile }) => {
    test.skip(!isMobile, "the clipping shows on a phone");
    await page.goto("/trip/sample-lisbon");
    const clipped = await page
      .getByRole("heading", { level: 1 })
      .evaluate((el) => el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight);
    expect(clipped).toBe(false);
  });

  test("/s/sample-lisbon is a read-only copy with the as-of header", async ({ page }) => {
    const response = await page.goto("/s/sample-lisbon");
    expect(response?.status()).toBe(200);
    await expect(page.getByText("Sample trip").first()).toBeVisible();
    await expect(page.getByText("Shared trip, as of 18 Nov 2026")).toBeVisible();
    await expect(page.getByRole("link", { name: "Plan your own trip" }).first()).toHaveAttribute(
      "href",
      "/",
    );
    await expect(
      page.getByRole("button", { name: /edit|choose|add|swap|share trip|new trip/i }),
    ).toHaveCount(0);
    await expect(page.getByText(/budget/i)).toHaveCount(0);
    await expect(page.getByRole("textbox")).toHaveCount(0);
  });
});

test.describe("links that do not work", () => {
  for (const path of ["/trip/abc", "/s/abc"]) {
    test(`${path} answers 404 with the link-not-found page`, async ({ page }) => {
      const response = await page.goto(path);
      expect(response?.status()).toBe(404);
      await expect(page.getByRole("heading", { level: 1 })).toHaveText("This link does not work");
      await expect(page.getByText("Link not found", { exact: true })).toBeVisible();
      await expect(page.getByRole("link", { name: "Plan a new trip" })).toHaveAttribute(
        "href",
        "/",
      );
    });
  }
});

test("/how-it-works shows its six parts and says there are no results yet", async ({ page }) => {
  await page.goto("/how-it-works");
  await expect(page.getByRole("heading", { level: 2 })).toHaveCount(6);
  await expect(page.getByText("No evaluation results yet")).toBeVisible();
});

test("the welcome screen has the chat and the empty canvas", async ({ page, isMobile }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toHaveText("Where to next?");
  await expect(page.getByRole("button", { name: "Three days in Porto" })).toBeVisible();
  if (isMobile) await page.getByRole("tab", { name: "Trip" }).click();
  await expect(
    page.getByText("Every figure shows where it came from and how old it is."),
  ).toBeVisible();
});
