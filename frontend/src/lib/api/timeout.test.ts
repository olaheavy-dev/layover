import { fetchWithTimeout, SERVER_API_TIMEOUT_MS } from "./timeout";

describe("fetchWithTimeout", () => {
  afterEach(() => vi.useRealTimers());

  it("waits 10 seconds, the owner's choice of 22 Nov 2026", () => {
    expect(SERVER_API_TIMEOUT_MS).toBe(10_000);
  });

  it("rejects a call that never answers once the time is up", async () => {
    vi.useFakeTimers();
    // A backend that accepts the call and never answers: it settles only when the signal aborts.
    const hung = (request: Request) =>
      new Promise<Response>((_, reject) => {
        request.signal.addEventListener("abort", () => reject(request.signal.reason));
      });
    const call = fetchWithTimeout(hung, 50)(new Request("http://api.test/v1/x"));
    const outcome = expect(call).rejects.toThrow();
    await vi.advanceTimersByTimeAsync(51);
    await outcome;
  });

  it("passes an answer that arrives in time", async () => {
    const quick = async () => new Response("ok");
    const response = await fetchWithTimeout(quick, 50)(new Request("http://api.test/v1/x"));
    expect(await response.text()).toBe("ok");
  });
});
