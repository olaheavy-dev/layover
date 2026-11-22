import { CalendarPlus, Circle, MapPinned, RefreshCw } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { clockTime, weekdayDate } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote } from "./PlaceParts";
import { SourceLabel } from "./SourceLabel";
import { WidgetFrame } from "./WidgetFrame";
import { ActionButton, Actions } from "./WidgetParts";

type Day = components["schemas"]["ItineraryDay"];
type Stop = components["schemas"]["Stop"];

function Banner({ children }: { children: React.ReactNode }) {
  return (
    <p className="bg-bg-tertiary text-text-primary border-border-primary inline-flex items-start gap-1.5 self-start rounded-md border px-3 py-1.5 text-sm">
      <MapPinned className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
      <span>{children}</span>
    </p>
  );
}

function HoursNotKnown() {
  return (
    <span className="text-status-not-known inline-flex items-center gap-1.5 italic">
      <Circle className="size-3" aria-hidden="true" />
      <span>Opening times: Not known</span>
    </span>
  );
}

// Opening hours come from the sample as given, never filled in. A "known" stop with either time
// missing or unreadable is Not known, never half a range.
function Hours({ stop }: { stop: Stop }) {
  switch (stop.hours_status) {
    case "known": {
      const opens = stop.opens ? clockTime(stop.opens) : null;
      const closes = stop.closes ? clockTime(stop.closes) : null;
      return opens && closes ? (
        <p>{`Open ${opens} to ${closes}`}</p>
      ) : (
        <p>
          <HoursNotKnown />
        </p>
      );
    }
    case "not_known":
      return (
        <p>
          <HoursNotKnown />
        </p>
      );
    case "depends_on_day":
      return (
        <div className="flex flex-col items-start">
          <p>Opening times depend on the day. Add your dates to see them.</p>
          <ActionButton
            variant="link"
            icon={<CalendarPlus className="size-4" aria-hidden="true" />}
          >
            Add your dates
          </ActionButton>
        </div>
      );
    case "not_applicable":
      return null;
  }
}

function StopRow({ stop, number }: { stop: Stop; number: number }) {
  const source = stop.source;
  return (
    <li className="flex gap-3">
      <span
        className="bg-bg-tertiary border-border-primary flex size-7 shrink-0 items-center justify-center rounded-full border text-sm font-medium"
        aria-hidden="true"
      >
        {number}
      </span>
      <div className="flex min-w-0 flex-col gap-0.5 text-sm">
        <strong className="font-medium">
          <span className="sr-only">Stop {number}: </span>
          {stop.name}
        </strong>
        <Hours stop={stop} />
        {source ? (
          source.status === "live" ? (
            <p className="text-text-secondary text-xs">Source: {source.source}</p>
          ) : (
            <p>
              <SourceLabel label={source} />
            </p>
          )
        ) : (
          <p className="text-text-secondary text-xs">Source: Not known</p>
        )}
      </div>
    </li>
  );
}

// One day's stops. Each stop carries its own source; the card's sources sit in the footer.
export function ItineraryDay({ widget }: { widget: Day }) {
  const dayText = widget.day ? weekdayDate(widget.day) : null;
  const title = dayText ? `Day ${widget.day_number}, ${dayText}` : `Day ${widget.day_number}`;
  const stops = widget.stops ?? [];
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote
        message={`Layover could not read places for Day ${widget.day_number} from OpenStreetMap or Wikivoyage just now.`}
      />
    );
  } else if (widget.state === "filled" && stops.length === 0) {
    body = <NotKnown missing={widget.missing ?? "the places for this day"} />;
  } else if (widget.state === "empty") {
    body = (
      <div className="flex flex-col items-start gap-2 text-sm">
        <p>
          <strong>Too few sourced places for the afternoon.</strong> Layover leaves it free rather
          than guessing.
        </p>
        <Actions>
          <ActionButton
            variant="secondary"
            icon={<RefreshCw className="size-4" aria-hidden="true" />}
          >
            Look in a wider area
          </ActionButton>
          <ActionButton variant="link">Leave it free</ActionButton>
        </Actions>
      </div>
    );
  } else if (widget.state === "not_known" && stops.length === 0) {
    body = <NotKnown missing={widget.missing ?? title} />;
  } else if (widget.state === "filled" || widget.state === "not_known") {
    body = (
      <div className="flex flex-col gap-3">
        {widget.rebuilt ? (
          <Banner>
            {widget.base
              ? `Rebuilt after you changed your hotel to ${widget.base}.`
              : "Rebuilt after you changed your hotel."}
          </Banner>
        ) : null}
        {widget.starts_from_centre ? (
          <Banner>Days start from the centre.</Banner>
        ) : widget.base && !widget.rebuilt ? (
          <p className="text-text-secondary text-sm">Starts from {widget.base}.</p>
        ) : null}
        <ol className="flex flex-col gap-3">
          {stops.map((stop, index) => (
            <StopRow key={`${stop.name}-${index}`} stop={stop} number={index + 1} />
          ))}
        </ol>
      </div>
    );
  }
  return (
    <WidgetFrame
      title={title}
      state={widget.state === "loading" ? "loading" : "filled"}
      sources={widget.sources}
    >
      {body}
    </WidgetFrame>
  );
}
