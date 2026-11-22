"use client";

import type { KeyboardEvent } from "react";

export type PhoneView = "chat" | "trip";

const TABS: { view: PhoneView; label: string }[] = [
  { view: "chat", label: "Chat" },
  { view: "trip", label: "Trip" },
];

// The Chat and Trip tabs for phone and tablet (below 1024 px). A proper tab pattern: only the
// selected tab is in the tab order and the arrow keys move between tabs. The page owns the two
// panels and gives them `id="panel-chat"` and `id="panel-trip"` with `aria-labelledby` set to the
// tab ids below. The badge ("3 new") is inside the tab, so it is read out with the tab's name.
// Docs: https://www.w3.org/WAI/ARIA/apg/patterns/tabs/
export function PhoneTabs({
  view,
  onViewChange,
  newCount,
}: {
  view: PhoneView;
  onViewChange: (view: PhoneView) => void;
  newCount?: number;
}) {
  function onKeyDown(event: KeyboardEvent<HTMLButtonElement>) {
    if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;
    event.preventDefault();
    const next = view === "chat" ? "trip" : "chat";
    onViewChange(next);
    document.getElementById(`tab-${next}`)?.focus();
  }

  return (
    <div
      role="tablist"
      aria-label="Chat or trip"
      className="bg-bg-secondary border-border-primary flex border-b lg:hidden"
    >
      {TABS.map(({ view: tab, label }) => {
        const selected = tab === view;
        return (
          <button
            key={tab}
            type="button"
            role="tab"
            id={`tab-${tab}`}
            aria-selected={selected}
            aria-controls={`panel-${tab}`}
            tabIndex={selected ? 0 : -1}
            onClick={() => onViewChange(tab)}
            onKeyDown={onKeyDown}
            className={`inline-flex min-h-11 flex-1 items-center justify-center gap-2 border-b-2 text-sm ${
              selected
                ? "border-accent-primary text-text-primary font-bold underline"
                : "text-text-secondary border-transparent"
            }`}
          >
            {label}{" "}
            {tab === "trip" && newCount ? (
              <span className="bg-accent-primary text-text-on-accent rounded-full px-2 py-0.5 text-xs font-medium">
                {newCount} new
              </span>
            ) : null}
          </button>
        );
      })}
    </div>
  );
}
