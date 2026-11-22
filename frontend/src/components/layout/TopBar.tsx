import { CircleHelp, Plus, Share2 } from "lucide-react";
import Link from "next/link";

import { ActionButton } from "../widgets/WidgetParts";
import { Logo } from "./Logo";

// The bar on every screen. The trip name is plain text, not a heading: the page owns the one h1.
// A shared trip has no "Share trip", and neither does a screen with no trip yet.
export function TopBar({
  tripName,
  shared = false,
  onShare,
  onNewTrip,
  children,
}: {
  tripName?: string;
  shared?: boolean;
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
        <p className="min-w-0 flex-1 truncate text-sm font-medium">{tripName}</p>
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
        <ActionButton
          variant="secondary"
          onClick={onNewTrip}
          icon={<Plus className="size-4" aria-hidden="true" />}
        >
          New trip
        </ActionButton>
      </nav>
    </header>
  );
}
