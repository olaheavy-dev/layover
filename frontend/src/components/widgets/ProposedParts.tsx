import { ArrowUpRight, Circle } from "lucide-react";

import { ActionLink } from "./WidgetParts";

// Small pieces shared by the four proposed widgets.

// An inline "Not known" for one missing value inside a row (decision 0011 rule 4).
export function NotKnownValue() {
  return (
    <span className="text-status-not-known inline-flex items-center gap-1.5 italic">
      <Circle className="size-3" aria-hidden="true" />
      <span>Not known</span>
    </span>
  );
}

// Only http and https addresses become links.
export function httpUrl(value: string | null | undefined): string | null {
  if (!value) return null;
  try {
    const url = new URL(value);
    return url.protocol === "http:" || url.protocol === "https:" ? url.href : null;
  } catch {
    return null;
  }
}

// A link out, or nothing when the address is missing or not http(s).
export function OutLink({ href, children }: { href?: string | null; children: React.ReactNode }) {
  const target = httpUrl(href);
  if (!target) return null;
  return (
    <ActionLink href={target} icon={<ArrowUpRight className="size-4" aria-hidden="true" />}>
      {children}
    </ActionLink>
  );
}

// The footer line for a widget whose source label is missing: no value is shown without a label.
export function missingSourceNote(count: number, loading: boolean): React.ReactNode {
  if (count > 0 || loading) return undefined;
  return <span className="text-text-secondary text-xs">Source: Not known</span>;
}
