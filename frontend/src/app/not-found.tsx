import { Link2 } from "lucide-react";
import type { Metadata } from "next";
import Link from "next/link";

import { TopBar } from "@/components/layout/TopBar";

export const metadata: Metadata = { title: "Link not found" };

// Shown at the requested address when a trip or share link does not work, and for any address that
// matches no page. It never says whether a trip ever existed (information architecture, "Limits and
// errors"). The words are the approved board's (docs/design/boards/screens/link-not-found.html).
export default function NotFound() {
  return (
    <div className="flex min-h-dvh flex-col">
      <TopBar action="none" />
      <main className="mx-auto flex w-full max-w-2xl flex-1 flex-col justify-center gap-3 px-4 py-10">
        <p className="text-text-secondary inline-flex items-center gap-2 text-sm font-medium">
          <Link2 className="size-4" aria-hidden="true" />
          Link not found
        </p>
        <h1 className="font-display text-3xl font-semibold">This link does not work</h1>
        <p className="text-base">
          The address may be wrong, or the link may no longer work. Check that you copied all of it.
        </p>
        <p className="flex flex-wrap items-center gap-3">
          <Link
            href="/"
            className="bg-accent-primary text-text-on-accent hover:bg-accent-primary-hover active:bg-accent-primary-active inline-flex min-h-11 items-center gap-1.5 rounded-md px-4 text-sm font-medium"
          >
            Plan a new trip
          </Link>
          <Link
            href="/how-it-works"
            className="text-text-link inline-flex min-h-11 items-center px-1 text-sm underline"
          >
            How Layover works
          </Link>
        </p>
      </main>
    </div>
  );
}
