import type { components } from "@/lib/api/schema";

import { monthName, shortWeekdayDate } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote } from "./PlaceParts";
import { missingSourceNote } from "./ProposedParts";
import { WidgetFrame } from "./WidgetFrame";

type PublicHolidaysWidget = components["schemas"]["PublicHolidays"];

// The national holidays that fall in the trip month, with the weekday worked out from the date.
// The contract is national only, so the note about local holidays is always there.
export function PublicHolidays({ widget }: { widget: PublicHolidaysWidget }) {
  const where = widget.country ?? widget.place;
  const month = widget.month != null ? monthName(widget.month) : null;
  const period = month && widget.year != null ? `${month} ${widget.year}` : null;
  const days = widget.holidays ?? [];
  const national = `Layover looked at the national list${widget.country ? ` for ${widget.country}` : ""}. Local holidays in one town or region may be missing from it.`;
  const head = (
    <p className="text-text-secondary text-sm">{period ? `${where}, ${period}` : where}</p>
  );

  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <div className="flex flex-col gap-2">
        {head}
        <ErrorNote
          message={`Layover could not work out the public holidays for ${where} just now. No holidays are shown. That does not mean there are none.`}
        />
      </div>
    );
  } else if (widget.state === "empty" && period) {
    body = (
      <div className="flex flex-col gap-2">
        {head}
        <p className="text-sm">
          {period ? `No public holidays in ${period}.` : "No public holidays."}
        </p>
        <p className="text-text-secondary text-sm">{national}</p>
      </div>
    );
  } else if (widget.state === "filled" && days.length > 0) {
    body = (
      <div className="flex flex-col gap-3">
        {head}
        <ul className="flex flex-col">
          {days.map((holiday, index) => (
            <li
              key={`${holiday.day}-${index}`}
              className="border-border-primary flex flex-wrap items-baseline justify-between gap-x-4 border-t py-2 text-sm first:border-t-0"
            >
              <span className="font-medium">{shortWeekdayDate(holiday.day) ?? holiday.day}</span>
              <span>{holiday.name}</span>
            </li>
          ))}
        </ul>
        <p className="text-text-secondary text-sm">
          Some places may close or run fewer services on a public holiday. Check opening times
          before you go.
        </p>
        <p className="text-text-secondary text-sm">{national}</p>
      </div>
    );
  } else if (widget.state !== "loading") {
    body = (
      <div className="flex flex-col gap-2">
        {head}
        <NotKnown
          missing={
            widget.missing ?? `the public holidays for ${where}${period ? ` in ${period}` : ""}`
          }
        />
      </div>
    );
  }
  return (
    <WidgetFrame
      title="Public holidays"
      state={widget.state === "loading" ? "loading" : "filled"}
      sources={widget.sources}
      footerNote={missingSourceNote(widget.sources.length, widget.state === "loading")}
    >
      {body}
    </WidgetFrame>
  );
}
