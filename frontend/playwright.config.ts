import { defineConfig, devices } from "@playwright/test";

const CI = Boolean(process.env.CI);
const PORT = 3100;
// The backend the sample pages read their samples from (GET /v1/sample/*).
const API_PORT = 8100;
// Set by scripts/e2e-docker.sh (CI, make screenshots-frontend): Chromium in Playwright's Linux
// image, the one place screenshots are compared, because fonts and rendering differ by machine.
const BROWSER_SERVER = process.env.PLAYWRIGHT_BROWSER_SERVER;

// End-to-end tests against the production build, served as the container serves it: the
// standalone server. `make check` builds first; run them alone with `make e2e-frontend`, or with
// the screenshots via `make e2e-frontend E2E_DOCKER=1`.
export default defineConfig({
  testDir: "./e2e",
  forbidOnly: CI,
  retries: CI ? 1 : 0,
  reporter: CI ? [["github"], ["list"]] : "list",
  ignoreSnapshots: !BROWSER_SERVER,
  // CI never writes a screenshot: a page without one fails until it is made and committed.
  updateSnapshots: CI ? "none" : "missing",
  snapshotPathTemplate: "{testDir}/screenshots/{testFilePath}/{arg}-{projectName}{ext}",
  use: {
    baseURL: `http://127.0.0.1:${PORT}`,
    trace: "retain-on-failure",
    // The browser in the container reaches this machine's 127.0.0.1 (the server) through the connection.
    connectOptions: BROWSER_SERVER
      ? { wsEndpoint: BROWSER_SERVER, exposeNetwork: "<loopback>" }
      : undefined,
  },
  // Each page is checked in light and dark, and at a phone's width.
  projects: [
    { name: "light", use: { ...devices["Desktop Chrome"], colorScheme: "light" } },
    { name: "dark", use: { ...devices["Desktop Chrome"], colorScheme: "dark" } },
    // 390 px is the narrowest width the product supports (WCAG 1.4.10 reflow starts at 320 CSS px).
    { name: "mobile", use: { ...devices["Pixel 7"], viewport: { width: 390, height: 844 } } },
  ],
  webServer: [
    {
      // The backend, from source, as `make dev` runs it (uv is installed in CI). The sample routes
      // need no database: it connects lazily, so only /health/ready would fail without one.
      // An empty ENV_FILE keeps a developer's own backend settings file (and its keys) out.
      command: `uv --directory ../backend run --locked --extra db uvicorn app.main:app --host 127.0.0.1 --port ${API_PORT} --no-access-log`,
      url: `http://127.0.0.1:${API_PORT}/health/live`,
      env: { APP_ENV: "local", ENV_FILE: "" },
      reuseExistingServer: !CI,
      timeout: 60_000,
    },
    {
      // The standalone server serves .next/static only once it is copied in (the image does the same).
      command: "cp -R .next/static .next/standalone/.next/ && node .next/standalone/server.js",
      url: `http://127.0.0.1:${PORT}`,
      env: {
        PORT: String(PORT),
        HOSTNAME: "127.0.0.1",
        NEXT_TELEMETRY_DISABLED: "1",
        ENABLE_WIDGET_GALLERY: "1",
        // The sample pages read the samples through the API, on every request.
        API_BASE_URL: `http://127.0.0.1:${API_PORT}`,
      },
      reuseExistingServer: !CI,
      timeout: 30_000,
    },
  ],
});
