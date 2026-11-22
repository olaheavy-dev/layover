// Which trip and share links work. Layover keeps no trips yet, so only the sample id is a trip; any
// other id is a link that does not work. Not server-only: the proxy reads it too.
export const SAMPLE_TRIP_ID = "sample-lisbon";

const LINK = /^\/(?:trip|s)\/([^/]+)\/?$/;

// True for /trip/{id} and /s/{id} with an id that is not a trip. The proxy answers these with 404
// before the page streams, because a page that finds out later can only say 404 in its text: the
// status is already 200 (Next.js docs, "loading.js", "Status codes").
export function isDeadLink(pathname: string): boolean {
  const id = LINK.exec(pathname)?.[1];
  return id !== undefined && id !== SAMPLE_TRIP_ID;
}
