import { Canvas } from "@/components/layout/Canvas";
import { chipsOf } from "@/components/widgets/BriefSummary";
import { shortDate } from "@/components/widgets/format";
import { TimeProvider } from "@/components/widgets/TimeContext";
import { Widget } from "@/components/widgets/Widget";
import { CHIP, Chips } from "@/components/widgets/WidgetParts";
import { SAMPLE_TODAY, type Trip } from "@/lib/samples";
import Link from "next/link";

import { placeWidgetsInOrder, Section, SECTION_TITLES, sectionsOf, stayShown } from "./sections";

// The frozen, read-only copy of a trip (information architecture, "Shared trip"). It has no chat,
// no input and no Edit, Choose or Add actions, so it never renders the widgets that carry them
// (the brief, the comparison and the hotel list); it shows the plain facts instead. Booking is a
// sandbox order for the traveller, so it is not part of the copy. Without the tick box
// "Include my budget and who's travelling", the copy leaves out the budget and traveller chips and
// every under or over budget line.
export function SharedTrip({ trip }: { trip: Trip }) {
  const includeBudget = trip.share.include_budget_and_travellers;
  const asOf = trip.share.as_of ? new Date(trip.share.as_of) : SAMPLE_TODAY;
  const asOfText = shortDate(asOf.toISOString().slice(0, 10));
  const brief = trip.brief;
  const chips = brief
    ? chipsOf(brief).filter(
        (chip) => includeBudget || (chip.key !== "adults" && chip.key !== "budget"),
      )
    : [];
  // A day that is empty or failed offers an action ("Look in a wider area", "Try again"), which a
  // read-only copy cannot have, so the copy leaves it out.
  const days = trip.days.filter((day) => day.state !== "empty" && day.state !== "error");
  const comparison = trip.comparison;
  const places = comparison?.cards?.map((card) => card.place) ?? [];
  const chosenHotel = trip.stay?.hotels?.find((hotel) => hotel.name === trip.stay?.chosen_hotel);
  const decided = trip.stay?.selection === "chosen" || trip.stay?.selection === "changed";

  return (
    <TimeProvider now={asOf} asOf>
      <Canvas
        sections={sectionsOf({ ...trip, days }, { shared: true })}
        place={trip.chosen_place ?? undefined}
      >
        <section aria-labelledby="shared-title" className="flex flex-col items-start gap-2">
          <p id="shared-title" className="text-text-secondary text-sm font-medium">
            Shared trip, as of {asOfText}
          </p>
          <p className="text-sm">
            This is a copy of a trip, frozen on {asOfText}. Fares and advice can change after that
            date, so check each source before you plan around it.
          </p>
          <Link
            href="/"
            className="bg-accent-primary text-text-on-accent hover:bg-accent-primary-hover active:bg-accent-primary-active inline-flex min-h-11 items-center rounded-md px-4 text-sm font-medium"
          >
            Plan your own trip
          </Link>
        </section>

        {brief ? (
          <Section id="brief" title={SECTION_TITLES.brief}>
            <Chips label="Your confirmed brief">
              {chips.map((chip) => (
                <li key={chip.key} className={CHIP}>
                  {chip.text}
                </li>
              ))}
            </Chips>
          </Section>
        ) : null}

        {comparison ? (
          <Section id="compare" title={SECTION_TITLES.compare}>
            <p className="text-sm">
              {comparison.chosen_place
                ? `Compared ${places.length} places: you chose ${comparison.chosen_place}`
                : `Compared ${places.length} places`}
            </p>
            <ul aria-label="The places compared" className="flex flex-col gap-1 text-sm">
              {places.map((place) => (
                <li key={place}>
                  <strong>{place}</strong>{" "}
                  <span className="text-text-secondary">
                    {place === comparison.chosen_place ? "You chose this" : "Also compared"}
                  </span>
                </li>
              ))}
            </ul>
          </Section>
        ) : null}

        {trip.chosen_place && trip.place_widgets.length > 0 ? (
          <Section id="place" title={trip.chosen_place} kicker="The place you chose">
            <div className="flex flex-col gap-4">
              {placeWidgetsInOrder(trip).map((widget, index) => (
                <Widget
                  key={`${widget.kind}-${index}`}
                  widget={
                    widget.kind === "cost_estimate" && !includeBudget
                      ? { ...widget, budget: null, budget_gap: null, budget_position: null }
                      : widget
                  }
                />
              ))}
            </div>
          </Section>
        ) : null}

        {trip.stay && stayShown(trip) ? (
          <Section id="stay" title={SECTION_TITLES.stay}>
            <p className="text-sm">
              {decided && chosenHotel
                ? `${chosenHotel.name}${chosenHotel.area ? `, ${chosenHotel.area}` : ""}. The base for the days.`
                : `You skipped the hotel. Days start from the centre of ${trip.stay.place}.`}
            </p>
          </Section>
        ) : null}

        {days.length > 0 ? (
          <Section id="days" title={SECTION_TITLES.days}>
            <div className="flex flex-col gap-4">
              {days.map((day) => (
                <Widget key={day.day_number} widget={day} />
              ))}
            </div>
          </Section>
        ) : null}
      </Canvas>
    </TimeProvider>
  );
}
