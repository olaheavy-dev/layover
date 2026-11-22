import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { Canvas } from "@/components/layout/Canvas";
import { TopBar } from "@/components/layout/TopBar";
import { SampleBanner } from "@/components/layout/SampleBanner";
import { sectionsOf } from "@/components/trip/sections";
import { TripSections } from "@/components/trip/TripSections";
import { Workspace } from "@/components/trip/Workspace";
import { TimeProvider } from "@/components/widgets/TimeContext";
import { getSampleTrip, SAMPLE_TODAY, SAMPLE_TRIP_ID } from "@/lib/samples";

// The sample trip's samples are read once, at build.
async function sampleTrip() {
  "use cache";
  return getSampleTrip();
}

// Layover keeps no trips yet, so only the sample id is a trip; any other id is a link that does
// not work. Listing the id here makes Next.js prerender it.
export function generateStaticParams() {
  return [{ tripId: SAMPLE_TRIP_ID }];
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ tripId: string }>;
}): Promise<Metadata> {
  const { tripId } = await params;
  if (tripId !== SAMPLE_TRIP_ID) notFound();
  return { title: (await sampleTrip()).name };
}

export default async function TripPage({ params }: { params: Promise<{ tripId: string }> }) {
  const { tripId } = await params;
  if (tripId !== SAMPLE_TRIP_ID) notFound();
  const trip = await sampleTrip();
  const factsReady = trip.place_widgets.filter((widget) => widget.state === "filled").length;
  return (
    <TimeProvider now={SAMPLE_TODAY}>
      <Workspace
        trip={{ name: trip.name, factsReady }}
        top={
          <TopBar tripName={trip.name} nameAs="h1">
            <SampleBanner />
          </TopBar>
        }
        canvas={
          <Canvas sections={sectionsOf(trip)} place={trip.chosen_place ?? undefined}>
            <TripSections trip={trip} />
          </Canvas>
        }
      />
    </TimeProvider>
  );
}
