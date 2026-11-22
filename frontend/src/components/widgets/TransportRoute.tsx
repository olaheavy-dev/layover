import { Footprints, TrainFront } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { clockTime, shortWeekdayDate } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote } from "./PlaceParts";
import { NotKnownValue, OutLink } from "./ProposedParts";
import { WidgetFrame } from "./WidgetFrame";

type TransportRouteWidget = components["schemas"]["TransportRoute"];

// TfL's journey planner, for the "plan it yourself" link.
const TFL_JOURNEY_PLANNER_URL = "https://tfl.gov.uk/plan-a-journey/";

// The credit TfL's open data terms ask to be shown beside its data (docs/references/data-sources.md).
const CREDITS = (
  <span className="text-text-secondary flex flex-col text-xs">
    <span>Powered by TfL Open Data</span>
    <span>Contains OS data © Crown copyright and database rights 2016</span>
  </span>
);

const PLAN_LINK = (
  <OutLink href={TFL_JOURNEY_PLANNER_URL}>Plan it on the TfL Journey Planner</OutLink>
);

// The steps of one London journey to an airport and the total the contract gives. The total is
// never added up here.
export function TransportRoute({ widget }: { widget: TransportRouteWidget }) {
  const legs = widget.legs ?? [];
  const day = widget.planned_for ? shortWeekdayDate(widget.planned_for) : null;
  const leaves = widget.leaves_at ? clockTime(widget.leaves_at) : null;
  const plan = day
    ? `TfL plan for ${day}${widget.dates_set ? "" : ", the middle of the month: your dates are not set yet"}${leaves ? `, leaving ${leaves}` : ""}`
    : null;

  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not ask TfL for a journey just now. No route or duration is shown.">
        {PLAN_LINK}
      </ErrorNote>
    );
  } else if (widget.state === "filled" && legs.length > 0) {
    body = (
      <div className="flex flex-col gap-3">
        <p className="font-display flex flex-col text-2xl font-semibold">
          {widget.total_minutes != null ? `About ${widget.total_minutes} min` : <NotKnownValue />}
          <span className="text-text-secondary font-sans text-sm font-normal">
            from {widget.origin}
          </span>
        </p>
        <ol className="flex flex-col">
          {legs.map((leg, index) => (
            <li
              key={`${leg.mode}-${index}`}
              className="border-border-primary grid grid-cols-[2rem_minmax(0,1fr)_auto] items-center gap-3 border-t py-3 text-sm first:border-t-0"
            >
              <span className="bg-bg-tertiary text-accent-primary grid size-8 place-items-center rounded-full">
                {leg.mode.toLowerCase() === "walk" ? (
                  <Footprints className="size-4" aria-hidden="true" />
                ) : (
                  <TrainFront className="size-4" aria-hidden="true" />
                )}
              </span>
              <span>{leg.description ?? leg.mode}</span>
              <span className="font-semibold whitespace-nowrap">{leg.minutes} min</span>
            </li>
          ))}
        </ol>
        {plan ? <p className="text-text-secondary text-sm">{plan}</p> : null}
      </div>
    );
  } else if (widget.state !== "loading") {
    body = (
      <div className="flex flex-col items-start gap-2">
        <NotKnown missing={widget.missing ?? `a journey to ${widget.destination}`} />
        {PLAN_LINK}
      </div>
    );
  }
  return (
    <WidgetFrame
      title={`To ${widget.destination}`}
      state={widget.state === "loading" ? "loading" : "filled"}
      sources={widget.sources}
      footerNote={widget.state === "loading" ? undefined : CREDITS}
    >
      {body}
    </WidgetFrame>
  );
}
