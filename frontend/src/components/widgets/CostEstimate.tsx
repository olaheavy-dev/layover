import type { components } from "@/lib/api/schema";

import { capitalise, formatMoney, plural, shownMoney } from "./format";
import { listingSource, pageEdited, unavailableLabel, type CostLine, type Part } from "./costLines";
import { NotKnown } from "./NotKnown";
import { SourceLabel } from "./SourceLabel";
import { WidgetFrame } from "./WidgetFrame";

type Cost = components["schemas"]["CostEstimate"];

const PARTS: Part[] = ["flights", "stay", "meals"];

function Value({ text, estimate }: { text: string; estimate: boolean }) {
  return (
    <span className="flex flex-col items-end text-right font-medium">
      <span>{text}</span>
      {estimate ? (
        <small className="text-text-secondary text-xs font-normal">estimate</small>
      ) : null}
    </span>
  );
}

function Row({
  name,
  value,
  meta,
  source,
}: {
  name: string;
  value: React.ReactNode | null;
  meta?: React.ReactNode;
  source?: React.ReactNode;
}) {
  return (
    <li className="border-border-primary flex flex-col gap-1 border-b pb-3 last:border-b-0">
      <div className="flex items-baseline justify-between gap-4">
        <span className="text-sm font-medium">{name}</span>
        {value}
      </div>
      <div className="text-text-secondary flex flex-wrap items-center justify-between gap-x-3 gap-y-1 text-xs">
        {meta}
        {source}
      </div>
    </li>
  );
}

// What each priced line says about how it was worked out, only from the contract's own fields.
function meta(part: Part, line: CostLine): string {
  const unit = line.unit ? formatMoney(line.unit) : null;
  if (!unit) return "";
  if (part === "flights") {
    return `${unit} each`;
  }
  const edited = pageEdited(line);
  const listings = [listingSource(line), edited ? `(page edited ${edited})` : ""]
    .filter(Boolean)
    .join(" ");
  if (part === "stay") return [`About ${unit} a night`, listings].filter(Boolean).join(", ");
  return [`About ${unit} a meal`, listings].filter(Boolean).join(", ");
}

function label(part: Part, cost: Cost): string {
  if (part === "flights") return "Flights";
  if (part === "stay")
    return cost.nights != null ? `Stay, ${plural(cost.nights, "night")}` : "Stay";
  return "Meals";
}

function lineRow(part: Part, cost: Cost) {
  const line = cost[part];
  const name = label(part, cost);
  const shown = line?.amount ? shownMoney(line.amount) : null;
  if (line?.amount && shown) {
    return (
      <Row
        key={part}
        name={name}
        value={<Value text={shown} estimate={line.amount.is_estimate} />}
        meta={<span>{meta(part, line)}</span>}
        source={line.source ? <SourceLabel label={line.source} /> : null}
      />
    );
  }
  const unavailable = unavailableLabel(part, cost.sources);
  if (unavailable) {
    return (
      <Row
        key={part}
        name={name}
        value={<span className="text-status-warning text-sm">Unavailable</span>}
        meta={line?.missing ? <span>{line.missing}</span> : undefined}
      />
    );
  }
  return <Row key={part} name={name} value={null} meta={<NotKnown missing={line?.missing} />} />;
}

// The local transport and activities lines say the same thing in every sample, so they share a
// row when both are missing for the same reason.
function otherRows(cost: Cost) {
  const transport = cost.local_transport;
  const activities = cost.activities;
  if (transport?.missing && activities?.missing && transport.missing === activities.missing) {
    return [
      <Row
        key="local"
        name="Local transport and activities"
        value={null}
        meta={<NotKnown missing={transport.missing} />}
      />,
    ];
  }
  const rows = [];
  for (const [key, name, line] of [
    ["local_transport", "Local transport", transport],
    ["activities", "Activities", activities],
  ] as const) {
    if (!line) continue;
    const shown = line.amount ? shownMoney(line.amount) : null;
    rows.push(
      line.amount && shown ? (
        <Row
          key={key}
          name={name}
          value={<Value text={shown} estimate={line.amount.is_estimate} />}
          source={line.source ? <SourceLabel label={line.source} /> : null}
        />
      ) : (
        <Row key={key} name={name} value={null} meta={<NotKnown missing={line.missing} />} />
      ),
    );
  }
  return rows;
}

// What is left out of the total, in words, for the line under the figure.
function gapsText(cost: Cost): string {
  const unavailable: string[] = [];
  const unknown: string[] = [];
  for (const part of PARTS) {
    if (cost[part]?.amount) continue;
    (unavailableLabel(part, cost.sources) ? unavailable : unknown).push(part);
  }
  if (cost.local_transport && !cost.local_transport.amount) unknown.push("local transport");
  if (cost.activities && !cost.activities.amount) unknown.push("activities");
  const clauses: string[] = [];
  if (unavailable.length > 0) clauses.push(`${join(unavailable)} could not be checked`);
  if (unknown.length > 0)
    clauses.push(`${join(unknown)} ${unknown.length > 1 ? "are" : "is"} not known`);
  const lead = unavailable.length > 0 ? "so far" : "estimate of the known costs";
  return clauses.length > 0 ? `${lead}, partial: ${clauses.join(", and ")}` : lead;
}

// "stay, local transport and activities"
function join(items: string[]): string {
  if (items.length < 2) return items.join("");
  return `${items.slice(0, -1).join(", ")} and ${items[items.length - 1]}`;
}

function Verdict({ cost }: { cost: Cost }) {
  if (!cost.budget) return null;
  const budget = formatMoney(cost.budget);
  if (!budget) {
    return (
      <p className="text-sm">
        <NotKnown missing="Your budget figure, so Layover cannot compare this total with it" />
      </p>
    );
  }
  const gap = cost.budget_gap ? shownMoney(cost.budget_gap) : null;
  if (gap && cost.budget_position) {
    const amount = capitalise(gap);
    const headline =
      cost.budget_position === "on"
        ? `On your ${budget} budget on the known costs.`
        : `${amount} ${cost.budget_position} your ${budget} budget on the known costs${
            cost.budget_position === "over" ? " alone" : ""
          }.`;
    const rest = cost.is_partial
      ? cost.budget_position === "over"
        ? " The costs that are not known would add to it."
        : " The costs that are not known could take it over."
      : "";
    return (
      <p className="text-sm">
        <strong>{headline}</strong>
        {rest}
      </p>
    );
  }
  const unavailable = PARTS.some(
    (part) => !cost[part]?.amount && unavailableLabel(part, cost.sources),
  );
  if (unavailable) {
    return (
      <p className="text-sm">
        <strong>
          This total is not complete, so Layover is not comparing it with your {budget} budget.
        </strong>{" "}
        A missing cost could change the answer.
      </p>
    );
  }
  const missingPart = PARTS.find((part) => !cost[part]?.amount);
  if (missingPart) {
    return (
      <p className="text-sm">
        <strong>
          {capitalise(missingPart)} is not known, so Layover cannot compare this total with your{" "}
          {budget} budget.
        </strong>
      </p>
    );
  }
  return null;
}

export function CostEstimate({ widget }: { widget: Cost }) {
  const hasBody =
    widget.state === "filled" ||
    (widget.state === "not_known" && PARTS.some((part) => widget[part] != null));
  const total = widget.total?.amount ? shownMoney(widget.total.amount) : null;
  return (
    <WidgetFrame
      title="Cost estimate"
      state={hasBody ? "filled" : widget.state}
      sources={widget.sources}
      missing={widget.missing}
    >
      <div className="flex flex-col gap-3">
        {total ? (
          <p className="font-display flex flex-col text-3xl font-semibold">
            <span>{total}</span>
            <span className="text-text-secondary font-sans text-sm font-normal">
              {widget.is_partial ? gapsText(widget) : "estimate"}
            </span>
          </p>
        ) : (
          <NotKnown missing="The total" />
        )}
        <Verdict cost={widget} />
        <ul className="flex flex-col gap-3" aria-label="Breakdown of the known costs">
          {PARTS.map((part) => lineRow(part, widget))}
          {otherRows(widget)}
        </ul>
      </div>
    </WidgetFrame>
  );
}
