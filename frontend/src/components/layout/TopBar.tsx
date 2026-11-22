import { CircleHelp, Plus, Share2 } from "lucide-react";
import Link from "next/link";

import { ActionButton } from "../widgets/WidgetParts";
import { Logo } from "./Logo";

// The bar on every screen. The trip name is plain text, not a heading: the page owns the one h1.
// A shared trip has no "Share trip", and neither does a screen with no trip yet.
export function TopBar({
  tripName,
  nameAs: Name = "p",
  shared = false,
  action = "new-trip",
  onShare,
  onNewTrip,
  children,
}: {
  tripName?: string;
  // The page decides which element holds the one h1: the trip name on a trip, or nothing here.
  nameAs?: "p" | "h1";
  shared?: boolean;
  // The button at the end: "New trip" (the default), a link to start a trip (shared trip, How it
  // works), or nothing (the welcome screen, which is already a new trip).
  action?: "new-trip" | "plan-your-own-trip" | "plan-a-trip" | "none";
  onShare?: () => void;
  onNewTrip?: () => void;
  // Room for the sample label.
  children?: React.ReactNode;
}) {
  return (
    <header className="bg-bg-secondary border-border-primary flex flex-wrap items-center gap-x-4 gap-y-2 border-b px-4 py-2">
      <Link href="/" aria-label="Layover, home" className="inline-flex min-h-11 items-center">
        <Logo />
      </Link>
      {tripName ? (
        <Name className="min-w-0 flex-1 truncate text-sm font-medium">{tripName}</Name>
      ) : (
        <span className="flex-1" />
      )}
      {children}
      <nav aria-label="Layover" className="flex items-center gap-2">
        <Link
          href="/how-it-works"
          className="text-text-link inline-flex min-h-11 items-center gap-1.5 px-1 text-sm underline"
        >
          <CircleHelp className="size-4" aria-hidden="true" />
          How it works
        </Link>
        {tripName && !shared ? (
          <ActionButton
            variant="secondary"
            onClick={onShare}
            icon={<Share2 className="size-4" aria-hidden="true" />}
          >
            Share trip
          </ActionButton>
        ) : null}
        {action === "new-trip" ? (
          <ActionButton
            variant="secondary"
            onClick={onNewTrip}
            icon={<Plus className="size-4" aria-hidden="true" />}
          >
            New trip
          </ActionButton>
        ) : null}
        {action === "plan-your-own-trip" || action === "plan-a-trip" ? (
          <Link
            href="/"
            className="border-border-control text-text-primary inline-flex min-h-11 items-center justify-center gap-1.5 rounded-md border px-4 text-sm font-medium"
          >
            <Plus className="size-4" aria-hidden="true" />
            {action === "plan-a-trip" ? "Plan a trip" : "Plan your own trip"}
          </Link>
        ) : null}
      </nav>
    </header>
  );
}
