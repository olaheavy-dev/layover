"use client";

import { Circle, Contrast, OctagonAlert, TriangleAlert } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { useTime } from "./TimeContext";

type Label = components["schemas"]["SourceLabel"];

const DAY_MS = 24 * 60 * 60 * 1000;

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(value));
}

// "Cached, 3 days old" (decision 0011 rule 2). The age is whole days between `captured_at` and
// `now`. With no capture time, the release date is shown; with neither, no age is invented.
function cachedText(label: Label, now: Date): string {
  // An unparseable or future time is never turned into an age: fall through to the next value.
  const captured = label.captured_at ? new Date(label.captured_at).getTime() : Number.NaN;
  if (!Number.isNaN(captured) && captured <= now.getTime()) {
    const days = Math.floor((now.getTime() - captured) / DAY_MS);
    if (days === 0) return "Cached, less than a day old";
    return `Cached, ${days} ${days === 1 ? "day" : "days"} old`;
  }
  if (label.data_date && !Number.isNaN(new Date(label.data_date).getTime())) {
    return `Cached, data released ${formatDate(label.data_date)}`;
  }
  return "Cached, age not known";
}

// Live and Cached use normal text colours with different dot shapes. Fallback and Unavailable use
// the warning colour with their own shapes. The words always name the state.
export function SourceLabel({ label, now: given }: { label: Label; now?: Date }) {
  // The `now` prop wins, then the page's TimeProvider, then the clock.
  const time = useTime();
  const now = given ?? time.now ?? new Date();
  let text: string;
  let icon: React.ReactNode;
  let colour: string;
  switch (label.status) {
    case "live":
      text = "Live";
      icon = <Circle className="size-3 shrink-0 fill-current" aria-hidden="true" />;
      colour = "text-status-live";
      break;
    case "cached":
      text = cachedText(label, now);
      icon = <Contrast className="size-3 shrink-0" aria-hidden="true" />;
      colour = "text-status-cached";
      break;
    case "fallback":
      text = "Fallback";
      icon = <TriangleAlert className="size-3 shrink-0" aria-hidden="true" />;
      colour = "text-status-warning";
      break;
    case "unavailable":
      text = "Unavailable";
      icon = <OctagonAlert className="size-3 shrink-0" aria-hidden="true" />;
      colour = "text-status-warning";
      break;
  }
  if (time.asOf && (label.status === "live" || label.status === "cached")) {
    text = `${text}, as of ${formatDate(now.toISOString())}`;
  }
  return (
    <span className="inline-flex flex-wrap items-center gap-x-1.5 gap-y-0.5 text-xs">
      <span className={`inline-flex items-center gap-1 ${colour}`}>
        {icon}
        <span>{text}</span>
      </span>
      <span className="text-text-secondary">{label.source}</span>
    </span>
  );
}
