"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { ORDER, SectionIndex, type SectionId } from "./SectionIndex";

// The right-hand side on desktop, the Trip tab on a phone. One canvas that scrolls, with the
// section index sticky at the top. With no children it shows the empty state from the welcome
// board, with the honesty line and the link to How Layover works.
//
// The index marks the section in view. A thin reading line sits just under the sticky index; the
// section that crosses it is the current one (an IntersectionObserver; a small scroll listener marks the last section at the end of the canvas).
// Until a section crosses it, the first one is marked. A page can still force one with `current`.
// Two cases the line cannot see are handled by hand. At the very end of the canvas the last
// section is marked, because a short last section may never reach the line. And a click on an
// index link scrolls inside the canvas only (the browser's own anchor jump also scrolls the page
// wrapper and pushes the top bar off screen), marks that section, and keeps it marked until the
// traveller scrolls away.
// Docs: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
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
  const scroller = useRef<HTMLElement>(null);
  const [seen, setSeen] = useState<SectionId | null>(null);
  const [atEnd, setAtEnd] = useState(false);
  const [pinned, setPinned] = useState<SectionId | null>(null);
  const pinnedTop = useRef(0);
  // The sections as the index lists them, in journey order.
  const shown = ORDER.filter((id) => sections.includes(id));
  const key = shown.join(",");

  useEffect(() => {
    const root = scroller.current;
    if (!root || typeof IntersectionObserver === "undefined") return;
    const ids = key === "" ? [] : (key.split(",") as SectionId[]);
    const onLine = new Set<SectionId>();
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          const id = ids.find((candidate) => candidate === entry.target.id);
          if (!id) continue;
          if (entry.isIntersecting) onLine.add(id);
          else onLine.delete(id);
        }
        // Both on the line at once: the later section is the one the traveller has scrolled to.
        const latest = ids.filter((id) => onLine.has(id)).at(-1);
        if (latest) setSeen(latest);
      },
      // From just under the sticky index (44 px) to a hand's width below it.
      { root, rootMargin: "-48px 0px -90% 0px" },
    );
    for (const id of ids) {
      const element = root.querySelector(`#${id}`);
      if (element) observer.observe(element);
    }
    return () => observer.disconnect();
  }, [key]);

  useEffect(() => {
    const root = scroller.current;
    if (!root) return;
    const onScroll = () => {
      // Only when there is something to scroll: a canvas that fits has no end to reach.
      setAtEnd(
        root.scrollHeight > root.clientHeight &&
          root.scrollTop + root.clientHeight >= root.scrollHeight - 1,
      );
      // A scroll that is not the one our own click made releases the clicked section.
      if (Math.abs(root.scrollTop - pinnedTop.current) > 1) setPinned(null);
    };
    onScroll();
    root.addEventListener("scroll", onScroll, { passive: true });
    return () => root.removeEventListener("scroll", onScroll);
  }, [key]);

  function onIndexClick(event: React.MouseEvent<HTMLElement>) {
    const root = scroller.current;
    const link = (event.target as HTMLElement).closest("nav a[href^='#']");
    if (!root || !link) return;
    const id = shown.find((candidate) => `#${candidate}` === link.getAttribute("href"));
    const target = id ? root.querySelector<HTMLElement>(`#${id}`) : null;
    if (!id || !target) return;
    event.preventDefault();
    const bar = root.querySelector("nav")?.getBoundingClientRect().height ?? 0;
    const top =
      root.scrollTop + target.getBoundingClientRect().top - root.getBoundingClientRect().top - bar;
    root.scrollTo({ top });
    pinnedTop.current = root.scrollTop;
    setPinned(id);
    // The anchor jump would have moved focus to the section; do it here without scrolling again.
    root.querySelector<HTMLElement>(`#${id}-title`)?.focus({ preventScroll: true });
    history.replaceState(null, "", `#${id}`);
  }

  const marked = current ?? pinned ?? (atEnd ? shown.at(-1) : undefined) ?? seen ?? shown[0];

  return (
    // The click handler only catches clicks that bubble up from the index links inside.
    <section
      ref={scroller}
      aria-label="Your trip"
      onClick={onIndexClick}
      className="bg-bg-primary flex min-h-0 flex-1 flex-col overflow-y-auto"
    >
      <SectionIndex sections={sections} place={place} current={marked} />
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
