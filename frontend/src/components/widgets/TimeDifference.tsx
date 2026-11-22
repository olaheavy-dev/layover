import type { components } from "@/lib/api/schema";

import { dayMonth, durationWords, utcOffset } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote } from "./PlaceParts";
import { missingSourceNote, NotKnownValue } from "./ProposedParts";
import { WidgetFrame } from "./WidgetFrame";

type TimeDifferenceWidget = components["schemas"]["TimeDifference"];

// How far ahead of or behind the UK the place is, as the contract gives it. Hours and minutes are
// only the contract's minutes put into words; nothing is added or subtracted here.
export function TimeDifference({ widget }: { widget: TimeDifferenceWidget }) {
  const diff = widget.difference_minutes;
  const words = diff != null ? durationWords(Math.abs(diff)) : null;
  const date = widget.on_date ? dayMonth(widget.on_date) : null;
  const when = date ? (widget.dates_set ? date : `${date}, the middle of the month`) : null;

  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not read the time zone data just now. No time difference is shown." />
    );
  } else if (widget.state === "filled" && diff != null && words) {
    let headline: string;
    let line: string | null;
    if (diff === 0) {
      headline = "Same time as the UK";
      line = when ? `On ${when}${widget.dates_set ? "" : ": your dates are not set yet"}` : null;
    } else {
      headline = `${words} ${diff > 0 ? "ahead" : "behind"}`;
      line = when
        ? `${widget.place} is ${diff > 0 ? "ahead of" : "behind"} the UK on ${when}`
        : null;
    }
    const uk = widget.uk_offset_minutes != null ? utcOffset(widget.uk_offset_minutes) : null;
    const there =
      widget.place_offset_minutes != null ? utcOffset(widget.place_offset_minutes) : null;
    body = (
      <div className="flex flex-col gap-2">
        <p className="font-display text-xl font-semibold">{headline}</p>
        {line ? <p className="text-text-secondary text-sm">{line}</p> : null}
        <dl className="flex flex-wrap gap-x-6 gap-y-1 text-sm">
          <div className="flex gap-1.5">
            <dt className="text-text-secondary">UK</dt>
            <dd>{uk ?? <NotKnownValue />}</dd>
          </div>
          <div className="flex gap-1.5">
            <dt className="text-text-secondary">{widget.place}</dt>
            <dd>{there ?? <NotKnownValue />}</dd>
          </div>
        </dl>
      </div>
    );
  } else if (widget.state !== "loading") {
    body = <NotKnown missing={widget.missing ?? `a time difference for ${widget.place}`} />;
  }
  return (
    <WidgetFrame
      title={`Time in ${widget.place}`}
      state={widget.state === "loading" ? "loading" : "filled"}
      sources={widget.sources}
      footerNote={missingSourceNote(widget.sources.length, widget.state === "loading")}
    >
      {body}
    </WidgetFrame>
  );
}
