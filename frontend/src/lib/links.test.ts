import { isDeadLink } from "./links";

describe("isDeadLink", () => {
  it.each(["/trip/abc", "/s/abc", "/trip/abc/", "/s/Sample-Lisbon", "/trip/sample-lisbon-2"])(
    "treats %s as a link that does not work",
    (path) => expect(isDeadLink(path)).toBe(true),
  );

  it.each([
    "/trip/sample-lisbon",
    "/s/sample-lisbon",
    "/trip/sample-lisbon/",
    "/",
    "/how-it-works",
  ])("leaves %s alone", (path) => expect(isDeadLink(path)).toBe(false));

  it.each(["/trip", "/s", "/trip/abc/extra", "/other/abc"])(
    "leaves %s to the router, which has no such page",
    (path) => expect(isDeadLink(path)).toBe(false),
  );
});
