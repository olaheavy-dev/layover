import { render, screen, within } from "@testing-library/react";

import { getSampleWidgets } from "@/lib/samples";

import WidgetGallery from "./page";

// Rendering every widget in every state (over 100 examples) can take more than vitest's
// default 5 s on a slow CI runner; it took 5.5 s there on 22 Nov 2026.
const GALLERY_RENDER_TIMEOUT = 30_000;

vi.mock("next/server", async (original) => ({
  ...(await original<object>()),
  connection: async () => {},
}));

async function open() {
  return render(await WidgetGallery());
}

describe("/dev/widgets", () => {
  afterEach(() => vi.unstubAllEnvs());

  it("answers not found when the setting is unset", async () => {
    vi.stubEnv("ENABLE_WIDGET_GALLERY", "");
    await expect(WidgetGallery()).rejects.toThrow("NEXT_HTTP_ERROR_FALLBACK;404");
  });

  it(
    "shows one section per kind, 20 in all, under one h1",
    async () => {
      vi.stubEnv("ENABLE_WIDGET_GALLERY", "1");
      await open();
      expect(screen.getAllByRole("heading", { level: 1 })).toHaveLength(1);
      const kinds = new Set((await getSampleWidgets()).map((s) => s.kind));
      expect(kinds.size).toBe(20);
      // One h2 per kind, then one for the notices.
      const h2s = screen.getAllByRole("heading", { level: 2 }).map((h) => h.textContent);
      expect(h2s).toEqual([...kinds, "notices"]);
      for (const kind of kinds) {
        expect(screen.getByRole("heading", { level: 2, name: kind })).toBeInTheDocument();
      }
    },
    GALLERY_RENDER_TIMEOUT,
  );

  it(
    "labels each sample state '<kind> · <state>' with a paragraph, not a heading, and shows the limit notice",
    async () => {
      vi.stubEnv("ENABLE_WIDGET_GALLERY", "1");
      await open();
      const samples = await getSampleWidgets();
      for (const { kind, state } of samples) {
        expect(screen.getByText(`${kind} · ${state}`).tagName).toBe("P");
      }
      // The widgets' own titles are the h3s: a label never sits beside them in the outline.
      expect(
        screen.getAllByRole("heading", { level: 3 }).filter((h) => h.textContent?.includes(" · ")),
      ).toEqual([]);
      expect(screen.getByText("limit_reached · shown").tagName).toBe("P");
      const notices = screen.getByRole("region", { name: "notices" });
      expect(within(notices).getByRole("status")).toHaveTextContent("You have reached the limit");
    },
    GALLERY_RENDER_TIMEOUT,
  );
});
