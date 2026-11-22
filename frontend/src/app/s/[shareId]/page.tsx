import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { cache } from "react";

import { SampleBanner } from "@/components/layout/SampleBanner";
import { TopBar } from "@/components/layout/TopBar";
import { SharedTrip } from "@/components/trip/SharedTrip";
import { getSampleTrip, SAMPLE_TODAY, SAMPLE_TRIP_ID } from "@/lib/samples";

// One API call per request, shared by the title and the page.
const sampleTrip = cache(getSampleTrip);

// The page reads the API, which is not there at build, so it renders on each request. Nothing is
// sent early, so an API error reaches the error page and not a half-drawn trip.
export const instant = false;

// A shared link is a frozen copy of a trip. Layover keeps none yet, so only the sample id works.

export async function generateMetadata({
  params,
}: {
  params: Promise<{ shareId: string }>;
}): Promise<Metadata> {
  const { shareId } = await params;
  if (shareId !== SAMPLE_TRIP_ID) notFound();
  return { title: `Shared trip: ${(await sampleTrip()).name}` };
}

export default async function SharedPage({ params }: { params: Promise<{ shareId: string }> }) {
  const { shareId } = await params;
  if (shareId !== SAMPLE_TRIP_ID) notFound();
  const trip = await sampleTrip();
  return (
    <div className="relative flex h-dvh flex-col overflow-hidden">
      <TopBar tripName={trip.name} nameAs="h1" shared action="plan-your-own-trip">
        <SampleBanner />
      </TopBar>
      <main className="mx-auto flex min-h-0 w-full max-w-3xl flex-1 flex-col">
        <SharedTrip trip={trip} asOf={trip.is_sample ? SAMPLE_TODAY : trip.share.as_of} />
      </main>
    </div>
  );
}
