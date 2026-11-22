import { Widget } from "@/components/widgets/Widget";
import type { Trip } from "@/lib/samples";

import { placeWidgetsInOrder, Section, SECTION_TITLES } from "./sections";

// The working trip's canvas sections, in journey order. Each section appears only when it has
// content. Earlier sections do not fold yet: folding comes with the live chat.
export function TripSections({ trip }: { trip: Trip }) {
  return (
    <>
      {trip.brief ? (
        <Section id="brief" title={SECTION_TITLES.brief}>
          <Widget widget={trip.brief} />
        </Section>
      ) : null}
      {trip.comparison ? (
        <Section id="compare" title={SECTION_TITLES.compare}>
          <Widget widget={trip.comparison} />
        </Section>
      ) : null}
      {trip.chosen_place && trip.place_widgets.length > 0 ? (
        <Section id="place" title={trip.chosen_place} kicker="The place you chose">
          <div className="flex flex-col gap-4">
            {placeWidgetsInOrder(trip).map((widget, index) => (
              <Widget key={`${widget.kind}-${index}`} widget={widget} />
            ))}
          </div>
        </Section>
      ) : null}
      {trip.stay ? (
        <Section id="stay" title={SECTION_TITLES.stay}>
          <Widget widget={trip.stay} />
        </Section>
      ) : null}
      {trip.days.length > 0 ? (
        <Section id="days" title={SECTION_TITLES.days}>
          <div className="flex flex-col gap-4">
            {trip.days.map((day) => (
              <Widget key={day.day_number} widget={day} />
            ))}
          </div>
        </Section>
      ) : null}
      {trip.booking ? (
        <Section id="booking" title={SECTION_TITLES.booking}>
          <Widget widget={trip.booking} />
        </Section>
      ) : null}
    </>
  );
}
