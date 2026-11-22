import Link from "next/link";

import { SectionIndex, type SectionId } from "./SectionIndex";

// The right-hand side on desktop, the Trip tab on a phone. One canvas that scrolls, with the
// section index sticky at the top. With no children it shows the empty state from the welcome
// board, with the honesty line and the link to How Layover works.
export function Canvas({
  sections = [],
  place,
  current,
  children,
}: {
  sections?: SectionId[];
  place?: string;
  current?: SectionId;
  children?: React.ReactNode;
}) {
  return (
    <section
      aria-label="Your trip"
      className="bg-bg-primary flex min-h-0 flex-1 flex-col overflow-y-auto"
    >
      <SectionIndex sections={sections} place={place} current={current} />
      <div className="flex flex-col gap-6 p-4 lg:p-6">
        {children ?? (
          <div className="flex flex-col items-start gap-2">
            <h2 className="font-display text-xl font-semibold">Your trip</h2>
            <p className="text-text-secondary text-sm">
              Your plan, prices and place facts appear here as we talk.
            </p>
            <p className="text-sm">
              <span>Every figure shows where it came from and how old it is.</span>{" "}
              <Link href="/how-it-works" className="text-text-link underline">
                How Layover works
              </Link>
            </p>
          </div>
        )}
      </div>
    </section>
  );
}
