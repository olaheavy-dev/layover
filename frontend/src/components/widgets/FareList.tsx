import type { components } from "@/lib/api/schema";

import { formatMoney, monthYear } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote } from "./PlaceParts";
import { missingSourceNote, OutLink } from "./ProposedParts";
import { SourceLabel } from "./SourceLabel";
import { WidgetFrame } from "./WidgetFrame";
import { ActionButton, Actions } from "./WidgetParts";

type FareListWidget = components["schemas"]["FareList"];
type Row = components["schemas"]["FareRow"];

// "Bristol (BRS)" -> "Bristol": the board's title and sentences use the place name alone.
function placeName(origin: string): string {
  return origin.replace(/\s*\([^)]*\)\s*$/, "") || origin;
}

function FareRow({ row }: { row: Row }) {
  const fare = row.fare;
  return (
    <li className="border-border-primary flex flex-col gap-1 border-t py-3 first:border-t-0">
      <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
        <strong className="font-medium">{row.destination}</strong>
        {fare ? (
          <span className="flex flex-wrap items-baseline gap-x-2">
            <span className="font-display text-xl font-semibold">{formatMoney(fare.price)}</span>
            <span className="text-text-secondary text-sm">return, per person</span>
          </span>
        ) : null}
      </div>
      {fare ? (
        fare.source ? (
          <SourceLabel label={fare.source} />
        ) : (
          <span className="text-text-secondary text-xs">Source: Not known</span>
        )
      ) : (
        <NotKnown missing={row.missing ?? `the fare to ${row.destination}`} />
      )}
      <OutLink href={row.search_url}>Check live price for {row.destination}</OutLink>
    </li>
  );
}

// The cached fares from one airport in a month, in the order the contract gives them (the
// contract only accepts lowest first). Every price shows its own age; none is a live price.
export function FareList({ widget }: { widget: FareListWidget }) {
  const place = placeName(widget.origin);
  const rows = widget.rows ?? [];
  const month = monthYear(widget.month);
  const head = (
    <p className="text-text-secondary text-sm">
      From {widget.origin}
      {month ? `, leaving in ${month}` : ""}
    </p>
  );

  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <div className="flex flex-col gap-2">
        {head}
        <ErrorNote
          message={`Layover could not check fares from ${place} just now. No fare is shown.`}
        >
          <OutLink href={widget.search_url}>Search flights on Aviasales</OutLink>
        </ErrorNote>
      </div>
    );
  } else if (widget.state === "filled" && rows.length > 0) {
    body = (
      <div className="flex flex-col gap-2">
        {head}
        <ul className="flex flex-col">
          {rows.map((row, index) => (
            <FareRow key={`${row.destination}-${index}`} row={row} />
          ))}
        </ul>
        <p className="text-text-secondary text-sm">
          Lowest fare first. A cached fare can have changed since. No comparison with usual prices
          is made.
        </p>
      </div>
    );
  } else if (widget.state !== "loading") {
    body = (
      <div className="flex flex-col items-start gap-2">
        {head}
        <NotKnown
          missing={
            widget.missing ?? `cached fares from ${widget.origin}${month ? ` in ${month}` : ""}`
          }
        />
        {widget.state === "empty" || widget.state === "not_known" ? (
          <p className="text-text-secondary text-sm">
            Layover looked at fares to any place and found none. A different month or airport may
            have some.
          </p>
        ) : null}
        <Actions>
          <OutLink href={widget.search_url}>Search flights on Aviasales</OutLink>
          <ActionButton variant="secondary">Change month</ActionButton>
        </Actions>
      </div>
    );
  }
  return (
    <WidgetFrame
      title={`Lowest cached fares from ${place}`}
      state={widget.state === "loading" ? "loading" : "filled"}
      sources={widget.sources}
      footerNote={missingSourceNote(widget.sources.length, widget.state === "loading")}
    >
      {body}
    </WidgetFrame>
  );
}
