// @vitest-environment node
import { unstable_doesMiddlewareMatch } from "next/experimental/testing/server";
import { NextRequest } from "next/server";

import * as csp from "@/lib/csp";

import { config, proxy } from "./proxy";

vi.mock("@/lib/csp", async (original) => {
  const actual = await original<typeof csp>();
  return {
    ...actual,
    usesNonce: (pathname: string) => actual.usesNonce(pathname, ["/account"]),
  };
});

function policyOf(response: Response) {
  return response.headers.get("content-security-policy") ?? "";
}

describe("the proxy", () => {
  afterEach(() => vi.unstubAllEnvs());

  it("sets the static policy on an ordinary page", () => {
    const response = proxy(new NextRequest("http://app.test/"));
    expect(policyOf(response)).toContain("script-src 'self' 'unsafe-inline'");
    expect(policyOf(response)).not.toContain("nonce-");
  });

  it("gives a nonce page a fresh nonce, in the response and in the request Next.js renders", () => {
    const first = proxy(new NextRequest("http://app.test/account/billing"));
    const second = proxy(new NextRequest("http://app.test/account"));
    const nonce = policyOf(first).match(/'nonce-([^']+)'/)?.[1];
    expect(nonce).toBeTruthy();
    expect(policyOf(second)).not.toContain(nonce);
    // NextResponse.next({ request }) passes overridden request headers on this way.
    expect(first.headers.get("x-middleware-request-content-security-policy")).toBe(policyOf(first));
  });

  it.each(["/trip/abc", "/s/abc"])("answers %s with the not-found page and status 404", (path) => {
    const response = proxy(new NextRequest(`http://app.test${path}`));
    expect(response.status).toBe(404);
    expect(response.headers.get("x-middleware-rewrite")).toBe("http://app.test/link-not-found");
    expect(policyOf(response)).toContain("frame-ancestors 'none'");
  });

  it.each(["/trip/sample-lisbon", "/s/sample-lisbon"])(
    "lets the sample link %s through",
    (path) => {
      const response = proxy(new NextRequest(`http://app.test${path}`));
      expect(response.status).toBe(200);
      expect(response.headers.get("x-middleware-rewrite")).toBeNull();
    },
  );

  it("answers /dev/widgets with 404 and the policy when the gallery setting is unset", () => {
    for (const path of ["/dev/widgets", "/dev/widgets/"]) {
      const response = proxy(new NextRequest(`http://app.test${path}`));
      expect(response.status).toBe(404);
      expect(response.headers.get("x-middleware-rewrite")).toBe("http://app.test/link-not-found");
      expect(policyOf(response)).toContain("frame-ancestors 'none'");
    }
  });

  it("lets /dev/widgets through when the gallery setting is on, and only that path is guarded", () => {
    vi.stubEnv("ENABLE_WIDGET_GALLERY", "1");
    expect(proxy(new NextRequest("http://app.test/dev/widgets")).status).toBe(200);
    vi.stubEnv("ENABLE_WIDGET_GALLERY", "");
    expect(proxy(new NextRequest("http://app.test/dev/other")).status).toBe(200);
  });

  it("adds CSP_CONNECT_SRC's origins, read per request", () => {
    vi.stubEnv("CSP_CONNECT_SRC", "https://files.example.com");
    expect(policyOf(proxy(new NextRequest("http://app.test/")))).toContain(
      "connect-src 'self' https://files.example.com",
    );
  });

  it.each(["/", "/courses/42", "/apiary", "/account"])("runs for the page %s", (url) => {
    expect(unstable_doesMiddlewareMatch({ config, url })).toBe(true);
  });

  it.each(["/api", "/api/v1/me", "/_next/static/chunks/a.js", "/_next/image", "/favicon.ico"])(
    "skips %s, which isn't a page",
    (url) => {
      expect(unstable_doesMiddlewareMatch({ config, url })).toBe(false);
    },
  );

  it("skips prefetches", () => {
    const headers = { "next-router-prefetch": "1" };
    expect(unstable_doesMiddlewareMatch({ config, url: "/", headers })).toBe(false);
  });
});
