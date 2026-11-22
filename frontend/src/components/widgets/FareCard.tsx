import { ArrowUpRight, RefreshCw } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { formatMoney } from "./format";
import { NotKnown } from "./NotKnown";
import { SourceLabel } from "./SourceLabel";
import { WidgetFrame } from "./WidgetFrame";
import { ActionButton, ActionLink } from "./WidgetParts";

type Fare = components["schemas"]["FareCard"];

const LINK_ICON = <ArrowUpRight className="size-4" aria-hidden="true" />;

// A cached return fare per person (the contract's `Fare`), its age and the Aviasales link.
// Error and Not known keep the link, so the traveller can still check the live price.
export function FareCard({ widget }: { widget: Fare }) {
  const link = (text: string) =>
    widget.search_url ? (
      <p>
        <ActionLink href={widget.search_url} icon={LINK_ICON}>
          {text}
        </ActionLink>
      </p>
    ) : null;

  let body: React.ReactNode = null;
  let state: "loading" | "filled" | "empty" = widget.state === "loading" ? "loading" : "filled";
  if (widget.state === "error") {
    body = (
      <div className="flex flex-col items-start gap-2" role="alert">
        <SourceLabel
          label={widget.sources[0] ?? { status: "unavailable", source: "Travelpayouts" }}
        />
        <p className="text-sm">
          Layover could not check fares for this route just now. No fare is shown.
        </p>
        {link("Search flights on Aviasales")}
        <ActionButton
          variant="secondary"
          icon={<RefreshCw className="size-4" aria-hidden="true" />}
        >
          Try again
        </ActionButton>
      </div>
    );
  } else if (
    widget.state === "not_known" ||
    (widget.state === "filled" && (!widget.fare || formatMoney(widget.fare.price) === null))
  ) {
    body = (
      <div className="flex flex-col gap-2">
        <NotKnown missing={widget.missing ?? `the fare to ${widget.destination}`} />
        {link("Check the live price on Aviasales")}
      </div>
    );
  } else if (widget.state === "empty") {
    state = "empty";
  } else if (widget.fare) {
    body = (
      <div className="flex flex-col gap-2">
        <p className="font-display flex flex-col text-3xl font-semibold">
          {formatMoney(widget.fare.price)}
          <span className="text-text-secondary font-sans text-sm font-normal">
            return, per person, from {widget.origin}
          </span>
        </p>
        <p className="text-text-secondary text-sm">A cached fare can have changed since.</p>
        {link("Check the live price on Aviasales")}
      </div>
    );
  }

  // The fare's own source label sits in the footer with the widget's sources.
  const sources = widget.sources.length > 0 || !widget.fare ? widget.sources : [widget.fare.source];
  return (
    <WidgetFrame title="Flights" state={state} sources={sources}>
      {body}
    </WidgetFrame>
  );
}
