import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { connection } from "next/server";

import { LimitReached } from "@/components/LimitReached";
import { TimeProvider } from "@/components/widgets/TimeContext";
import { Widget } from "@/components/widgets/Widget";
import { galleryEnabled } from "@/lib/gallery";
import { getSampleWidgets, SAMPLE_TODAY, type SampleWidget } from "@/lib/samples";

export const metadata: Metadata = { title: "Widget gallery", robots: { index: false } };

// The page reads the setting and the API on each request. The status and headers are sent at once;
// the body waits, so an API error shows the error page and not a half-drawn page. A development
// page, so no placeholder.
export const instant = false;

// Every widget in every sample state, for development. On only with ENABLE_WIDGET_GALLERY; the
// proxy answers 404 before this page streams, and this guard is the second line.
export default async function WidgetGallery() {
  // Read the setting on every request, not at build.
  await connection();
  if (!galleryEnabled()) notFound();
  const samples = await getSampleWidgets();
  const byKind = new Map<string, SampleWidget[]>();
  for (const sample of samples)
    byKind.set(sample.kind, [...(byKind.get(sample.kind) ?? []), sample]);
  return (
    <TimeProvider now={SAMPLE_TODAY}>
      <main className="mx-auto flex w-full max-w-3xl flex-col gap-10 px-4 py-8">
        <h1 className="font-display text-3xl font-semibold">Widget gallery</h1>
        {[...byKind].map(([kind, items]) => (
          <Kind key={kind} name={kind}>
            {items.map(({ state, widget }) => (
              <Example key={state} title={`${kind} · ${state}`}>
                <Widget widget={widget} />
              </Example>
            ))}
          </Kind>
        ))}
        <Kind name="notices">
          <Example title="limit_reached · shown">
            <LimitReached />
          </Example>
        </Kind>
      </main>
    </TimeProvider>
  );
}

function Kind({ name, children }: { name: string; children: React.ReactNode }) {
  return (
    <section aria-labelledby={`kind-${name}`} className="flex flex-col gap-6">
      <h2 id={`kind-${name}`} className="font-display text-2xl font-semibold">
        {name}
      </h2>
      {children}
    </section>
  );
}

function Example({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="flex flex-col gap-2">
      <p className="text-text-secondary text-sm font-medium">{title}</p>
      {children}
    </div>
  );
}
