"use client";

import { createContext, useContext } from "react";

type Time = { now: Date | null; asOf: boolean };

const TimeContext = createContext<Time>({ now: null, asOf: false });

// The date a page measures ages from. A page with no provider uses the clock. A sample page uses
// the sample's own "today", so "Cached, 3 days old" never drifts. `asOf` is for a shared trip: its
// Live and Cached labels add ", as of" and that date (docs/design/boards/sample-data.md).
// It is a client component so the label reads it the same way on the server and in the browser.
export function TimeProvider({
  now,
  asOf = false,
  children,
}: {
  now: Date;
  asOf?: boolean;
  children: React.ReactNode;
}) {
  return <TimeContext value={{ now, asOf }}>{children}</TimeContext>;
}

export function useTime(): Time {
  return useContext(TimeContext);
}
