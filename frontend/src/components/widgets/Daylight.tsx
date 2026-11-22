import type { components } from "@/lib/api/schema";

import { clockTime, dayMonth, hoursMinutes } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote, frameState } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";
import { ActionLink } from "./WidgetParts";

type Light = components["schemas"]["Daylight"];

function Row({ term, value }: { term: string; value: string | null }) {
  return (
    <div className="border-border-primary flex items-baseline justify-between gap-4 border-b pb-2 last:border-b-0">
      <dt className="text-text-secondary text-sm">{term}</dt>
      <dd className="font-medium">{value ?? <NotKnown missing={term.toLowerCase()} />}</dd>
    </div>
  );
}

// Sunrise, sunset and day length for one day, each as the contract gives it.
export function Daylight({ widget }: { widget: Light }) {
  const day = widget.day ? dayMonth(widget.day) : null;
  const credit = widget.sources[0]?.source;
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not check sunrise and sunset just now. No times are shown." />
    );
  } else if (widget.state === "filled") {
    body = (
      <div className="flex flex-col gap-3">
        {day ? (
          <p className="text-text-secondary text-sm">
            {day}
            {widget.dates_set ? "" : ": your dates are not set yet"}
          </p>
        ) : null}
        <dl className="flex flex-col gap-2">
          <Row term="Sunrise" value={widget.sunrise ? clockTime(widget.sunrise) : null} />
          <Row term="Sunset" value={widget.sunset ? clockTime(widget.sunset) : null} />
          <Row
            term="Day length"
            value={
              widget.day_length_minutes != null ? hoursMinutes(widget.day_length_minutes) : null
            }
          />
        </dl>
        {widget.credit_url && credit ? (
          <p>
            <ActionLink href={widget.credit_url}>Times from {credit}</ActionLink>
          </p>
        ) : null}
      </div>
    );
  }
  return (
    <WidgetFrame
      title="Daylight"
      state={frameState(widget.state)}
      sources={widget.sources}
      missing={widget.missing}
    >
      {body}
    </WidgetFrame>
  );
}
