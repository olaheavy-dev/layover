import { notFound } from "next/navigation";

import { SampleBanner } from "@/components/layout/SampleBanner";
import { TopBar } from "@/components/layout/TopBar";
import { SharedTrip } from "@/components/trip/SharedTrip";
import { getSampleTrip, SAMPLE_TRIP_ID } from "@/lib/samples";

async function sampleTrip() {
  "use cache";
  return getSampleTrip();
}

// A shared link is a frozen copy of a trip. Layover keeps none yet, so only the sample id works.
export function generateStaticParams() {
  return [{ shareId: SAMPLE_TRIP_ID }];
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
        <SharedTrip trip={trip} />
      </main>
    </div>
  );
}
