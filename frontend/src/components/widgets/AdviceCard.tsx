import { ArrowUpRight } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { shortDate } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";
import { ActionLink } from "./WidgetParts";

type Advice = components["schemas"]["AdviceCard"];

const ICON = <ArrowUpRight className="size-4" aria-hidden="true" />;

// Entry advice always links to the FCDO page and shows its update date (decision 0011
// rule 6). The link stays in every state. The widget never judges a destination itself.
export function AdviceCard({ widget }: { widget: Advice }) {
  const link = (text: string) => (
    <p>
      <ActionLink href={widget.fcdo_url} icon={ICON}>
        {text}
      </ActionLink>
    </p>
  );
  const readLink = link(`Read the FCDO advice for ${widget.place}`);
  const updated = widget.updated_on ? shortDate(widget.updated_on) : null;
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not read it just now. The FCDO page is still there.">
        {readLink}
      </ErrorNote>
    );
  } else if (widget.state === "not_known") {
    body = (
      <div className="flex flex-col gap-2">
        <NotKnown missing={widget.missing ?? `FCDO travel advice for ${widget.place}`} />
        {link("Find a country on the FCDO travel advice index")}
      </div>
    );
  } else if (widget.state === "filled") {
    body = (
      <div className="flex flex-col gap-2">
        <p>
          {widget.title ? <strong>{widget.title}</strong> : null}
          {widget.title ? <br /> : null}
          {updated ? (
            <span>Updated {updated}</span>
          ) : (
            <NotKnown missing="the date the FCDO last updated this advice" />
          )}
        </p>
        {widget.layover_copy ? <p className="text-sm">{widget.layover_copy}</p> : null}
        {readLink}
      </div>
    );
  }
  return (
    <WidgetFrame
      title="Travel advice"
      state={widget.state === "error" || widget.state === "not_known" ? "filled" : widget.state}
      sources={widget.sources}
      missing={widget.missing}
    >
      {body}
    </WidgetFrame>
  );
}
