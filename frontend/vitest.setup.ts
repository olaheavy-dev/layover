import "@testing-library/jest-dom/vitest";

// `server-only` throws when imported outside a React Server environment; the tests import server
// modules directly.
vi.mock("server-only", () => ({}));

// The pages read the shared samples through the API (GET /v1/sample/trip and /v1/sample/widgets).
// The unit tests have no backend, so this stands in for it by reading the same files the backend
// serves (schemas/samples), in the same order. A test that checks the API call itself
// (samples.test.ts) replaces this mock with its own.
vi.mock("@/lib/api/server", async () => {
  const { readdir, readFile } = await import("node:fs/promises");
  const path = await import("node:path");
  const root = path.resolve(process.cwd(), "..", "schemas", "samples");
  const read = async (...parts: string[]) =>
    JSON.parse(await readFile(path.join(root, ...parts), "utf8"));
  async function widgets() {
    const kinds = (await readdir(path.join(root, "widgets"), { withFileTypes: true }))
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .sort();
    const samples = [];
    for (const kind of kinds) {
      const files = (await readdir(path.join(root, "widgets", kind)))
        .filter((f) => f.endsWith(".json"))
        .sort();
      for (const file of files) {
        samples.push({
          is_sample: true,
          kind,
          state: file.slice(0, -".json".length),
          widget: await read("widgets", kind, file),
        });
      }
    }
    return samples;
  }
  return {
    serverApi: async () => ({
      GET: async (url: string) => {
        if (url === "/v1/sample/trip") return { data: await read("trip", "sample-lisbon.json") };
        if (url === "/v1/sample/widgets") return { data: await widgets() };
        throw new Error(`vitest.setup: no stand-in for ${url}`);
      },
    }),
  };
});
