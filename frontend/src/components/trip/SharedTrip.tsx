import { Canvas } from "@/components/layout/Canvas";
import { chipsOf } from "@/components/widgets/BriefSummary";
import { plural, shortDate } from "@/components/widgets/format";
import { TimeProvider } from "@/components/widgets/TimeContext";
import { Widget } from "@/components/widgets/Widget";
import { CHIP, Chips } from "@/components/widgets/WidgetParts";
import type { Trip } from "@/lib/samples";
import Link from "next/link";

import { placeWidgetsInOrder, Section, SECTION_TITLES, sectionsOf, stayShown } from "./sections";

type Stay = NonNullable<Trip["stay"]>;

// What the copy says about the hotel. "Skipped" only when the traveller skipped it; a chosen or
// changed hotel is named from the contract's `chosen_hotel`, with its area when a listed row matches.
function stayText(stay: Stay): string {
  if (stay.selection === "skipped") {
    return `You skipped the hotel. Days start from the centre of ${stay.place}.`;
  }
  if (!stay.chosen_hotel) return "A hotel was chosen. Its name is not known.";
  const row = stay.hotels?.find((hotel) => hotel.name === stay.chosen_hotel);
  return `${stay.chosen_hotel}${row?.area ? `, ${row.area}` : ""}. The base for the days.`;
}

function readDate(value: Date | string | null | undefined): Date | null {
  if (!value) return null;
  const date = value instanceof Date ? value : new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
}

// The frozen, read-only copy of a trip (information architecture, "Shared trip"). It has no chat,
// no input and no Edit, Choose or Add actions, so it never renders the widgets that carry them
// (the brief, the comparison and the hotel list); it shows the plain facts instead. Booking is a
// sandbox order for the traveller, so it is not part of the copy. Without the tick box
// "Include my budget and who's travelling", the copy leaves out the budget and traveller chips and
// every under or over budget line.
//
// `asOf` is the date the copy was frozen. The page passes the sample's own day for the sample trip
// and the share settings' `as_of` for any other trip. With no date, or one that cannot be read,
// the copy says "Shared trip" and shows no date: Layover never invents one.
export function SharedTrip({ trip, asOf: given }: { trip: Trip; asOf?: Date | string | null }) {
  const includeBudget = trip.share.include_budget_and_travellers;
  const asOf = readDate(given);
  const asOfText = asOf ? shortDate(asOf.toISOString().slice(0, 10)) : null;
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

  return (
    <TimeProvider now={asOf} asOf={asOf !== null}>
      <Canvas
        sections={sectionsOf({ ...trip, days }, { shared: true })}
        place={trip.chosen_place ?? undefined}
      >
        <section aria-labelledby="shared-title" className="flex flex-col items-start gap-2">
          <p id="shared-title" className="text-text-secondary text-sm font-medium">
            {asOfText ? `Shared trip, as of ${asOfText}` : "Shared trip"}
          </p>
          <p className="text-sm">
            {asOfText
              ? `This is a copy of a trip, frozen on ${asOfText}. Fares and advice can change after that date, so check each source before you plan around it.`
              : "This is a copy of a trip. Fares and advice can change, so check each source before you plan around it."}
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
                ? `Compared ${plural(places.length, "place")}: you chose ${comparison.chosen_place}`
                : `Compared ${plural(places.length, "place")}`}
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
            <p className="text-sm">{stayText(trip.stay)}</p>
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
