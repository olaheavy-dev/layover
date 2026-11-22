/**
 * How long a server-side API call may take before it fails and the error page shows. Owner's
 * choice, 22 Nov 2026: "10 seconds (Recommended)". Today's sample calls take about 5 ms; raise it
 * here when a later step adds slower calls. Without a limit, a backend that accepts a call and
 * never answers leaves the page loading for minutes.
 */
export const SERVER_API_TIMEOUT_MS = 10_000;

type Fetch = (input: Request) => Promise<Response>;

/** Wraps a fetch so each call is cancelled, and rejects, after `ms`. */
export function fetchWithTimeout(
  inner: Fetch = (request) => fetch(request),
  ms: number = SERVER_API_TIMEOUT_MS,
): Fetch {
  return (request) =>
    inner(
      new Request(request, { signal: AbortSignal.any([request.signal, AbortSignal.timeout(ms)]) }),
    );
}
