"use client";

import { OctagonAlert, Pencil, RefreshCw, Repeat2 } from "lucide-react";
import { useState } from "react";

import type { components } from "@/lib/api/schema";

import { listingSource, pageEdited, unavailableLabel, type CostLine, type Part } from "./costLines";
import { capitalise, formatMoney, plural, shownMoney } from "./format";
import { NotKnown } from "./NotKnown";
import { SourceLabel } from "./SourceLabel";
import { WidgetFrame } from "./WidgetFrame";
import { ActionButton, Actions, CHIP, Skeleton } from "./WidgetParts";

type Table = components["schemas"]["ComparisonTable"];
type PlaceCard = components["schemas"]["PlaceCard"];

function Row({
  name,
  value,
  estimate,
  meta,
  source,
}: {
  name: string;
  value?: string;
  estimate?: boolean;
  meta?: React.ReactNode;
  source?: React.ReactNode;
}) {
  return (
    <div className="border-border-primary flex flex-col gap-1 border-b pb-2 last:border-b-0">
      <dt className="text-text-secondary text-xs">{name}</dt>
      {value ? (
        <dd className="flex items-baseline gap-2 font-medium">
          <span>{value}</span>
          {estimate ? (
            <small className="text-text-secondary text-xs font-normal">estimate</small>
          ) : null}
        </dd>
      ) : null}
      {meta || source ? (
        <dd className="text-text-secondary flex flex-col gap-1 text-xs">
          {meta}
          {source}
        </dd>
      ) : null}
    </div>
  );
}

// "£70 a night, an estimate from 6 Wikivoyage listings, page edited March 2026"
function note(part: Part, line: CostLine): string {
  const unit = line.unit ? formatMoney(line.unit) : null;
  if (!unit) return "";
  if (part === "flights") return `${unit} each`;
  const edited = pageEdited(line);
  const detail = [listingSource(line), edited ? `page edited ${edited}` : ""]
    .filter(Boolean)
    .join(", ");
  return `${unit} a ${part === "stay" ? "night" : "meal"}, an estimate${detail ? ` ${detail}` : ""}`;
}

function costRow(
  name: string,
  part: Part,
  line: CostLine | null | undefined,
  sources: Table["sources"],
) {
  const value = line?.amount ? shownMoney(line.amount) : null;
  if (line?.amount && value) {
    const text = note(part, line);
    return (
      <Row
        key={part}
        name={name}
        value={value}
        estimate={line.amount.is_estimate}
        meta={text ? <span>{text}</span> : undefined}
        source={line.source ? <SourceLabel label={line.source} /> : undefined}
      />
    );
  }
  if (unavailableLabel(part, sources)) {
    return <Row key={part} name={name} value="Unavailable" meta={<span>{line?.missing}</span>} />;
  }
  return (
    <Row
      key={part}
      name={name}
      meta={<NotKnown missing={line?.missing ?? "Layover has no figure for this yet"} />}
    />
  );
}

function missingParts(card: PlaceCard): string[] {
  const names: string[] = [];
  for (const part of ["flights", "stay", "meals"] as const) {
    if (!card[part]?.amount || shownMoney(card[part].amount) === null) names.push(part);
  }
  return names;
}

function Against({ card }: { card: PlaceCard }) {
  const gap = card.budget_gap ? shownMoney(card.budget_gap) : null;
  if (gap && card.budget_position) {
    const amount = capitalise(gap);
    const over = card.budget_position === "over";
    const head =
      card.budget_position === "on" ? "On your budget" : `${amount} ${card.budget_position}`;
    return (
      <Row
        name="Against your budget"
        meta={
          <span>
            <strong className="text-text-primary">{head}</strong>
            {card.budget_position === "on" ? "" : " your budget"} on the known costs
            {over ? " alone." : "."}
            {!over && card.is_partial ? " The costs that are not known could take it over." : ""}
          </span>
        }
      />
    );
  }
  const gaps = missingParts(card);
  return (
    <Row
      name="Against your budget"
      meta={
        <NotKnown
          missing={gaps.length > 0 ? `the ${gaps[0]} figure is missing` : "the budget gap"}
        />
      }
    />
  );
}

function Ready({ card, sources }: { card: PlaceCard; sources: Table["sources"] }) {
  const weather = card.weather;
  const readings = weather
    ? [
        weather.high_c != null ? `${weather.high_c}°C high` : null,
        weather.low_c != null ? `${weather.low_c}°C low` : null,
        weather.rainy_days != null ? plural(weather.rainy_days, "rainy day") : null,
      ].filter(Boolean)
    : [];
  const weatherText =
    weather && readings.length > 0
      ? `Typically ${readings.join(", ")}, averages ${weather.averages_period.replace("-", " to ")}`
      : null;
  return (
    <>
      <dl className="flex flex-col gap-2 text-sm">
        {costRow("Flights", "flights", card.flights, sources)}
        {costRow("Stay", "stay", card.stay, sources)}
        {costRow("Meals", "meals", card.meals, sources)}
        {card.known_costs?.amount && shownMoney(card.known_costs.amount) ? (
          <Row
            name="Known costs"
            value={shownMoney(card.known_costs.amount) ?? undefined}
            estimate={card.known_costs.amount.is_estimate}
            meta={card.is_partial ? <span>Partial: some costs are not known</span> : undefined}
            source={
              card.known_costs.source ? <SourceLabel label={card.known_costs.source} /> : undefined
            }
          />
        ) : (
          <Row
            name="Known costs"
            meta={<NotKnown missing="Layover has no total for this place" />}
          />
        )}
        <Against card={card} />
        {weather && weatherText ? (
          <Row
            name="Weather"
            meta={<span>{weatherText}</span>}
            source={<SourceLabel label={weather.source} />}
          />
        ) : (
          <Row name="Weather" meta={<NotKnown missing="Weather for this place" />} />
        )}
      </dl>
      <Actions>
        <ActionButton variant="secondary">Choose {card.place}</ActionButton>
        <ActionButton
          variant="link"
          label={`Swap place (${card.place})`}
          icon={<Repeat2 className="size-4" aria-hidden="true" />}
        >
          Swap place
        </ActionButton>
      </Actions>
    </>
  );
}

function CardBody({ card, sources }: { card: PlaceCard; sources: Table["sources"] }) {
  if (card.card_state === "loading") {
    return (
      <>
        <p className="sr-only" role="status">
          Checking {card.place}
        </p>
        <div className="flex flex-col gap-3" aria-hidden="true">
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} className="flex flex-col gap-1">
              <Skeleton className="h-3 w-1/3" />
              <Skeleton className="h-4 w-3/4" />
            </div>
          ))}
        </div>
        <p className="text-text-secondary text-sm">Checking fares, costs and weather</p>
      </>
    );
  }
  if (card.card_state === "failed") {
    return (
      <div className="flex flex-col items-start gap-2">
        <p className="text-status-warning inline-flex items-center gap-1.5 text-sm font-medium">
          <OctagonAlert className="size-4" aria-hidden="true" />
          Unavailable
        </p>
        <p className="text-sm">
          Layover could not check fares, costs or weather for {card.place} just now. The other
          places are not affected.
        </p>
        <ActionButton
          variant="secondary"
          label={`Try again for ${card.place}`}
          icon={<RefreshCw className="size-4" aria-hidden="true" />}
        >
          Try again
        </ActionButton>
      </div>
    );
  }
  if (card.card_state === "swapped") {
    return (
      <>
        <p className="text-sm">
          <strong>Researching your place</strong>
          <br />
          Checking fares, costs and weather for {card.place}.
        </p>
        <p className="sr-only" role="status">
          Researching {card.place}
        </p>
        <div className="flex flex-col gap-3" aria-hidden="true">
          {[0, 1, 2, 3, 4].map((i) => (
            <div key={i} className="flex flex-col gap-1">
              <Skeleton className="h-3 w-1/3" />
              <Skeleton className="h-4 w-3/4" />
            </div>
          ))}
        </div>
        <Actions>
          <ActionButton variant="link" icon={<Repeat2 className="size-4" aria-hidden="true" />}>
            Swap back
          </ActionButton>
        </Actions>
      </>
    );
  }
  return <Ready card={card} sources={sources} />;
}

export function ComparisonTable({ widget }: { widget: Table }) {
  const [shownAgain, setShownAgain] = useState(false);
  const cards = widget.cards ?? [];

  if (cards.length === 0) {
    if (widget.state === "empty") {
      return (
        <WidgetFrame title="No place fits yet" state="filled" sources={widget.sources}>
          <div className="flex flex-col gap-3">
            <p className="text-sm">
              <strong>Nothing fits your brief yet.</strong>
              {widget.rules_out ? ` ${capitalise(widget.rules_out)} rules places out.` : ""}
            </p>
            {widget.rules_out ? (
              <ul
                className="flex flex-wrap gap-2"
                aria-label="The part of your brief that rules places out"
              >
                <li className={`${CHIP} border-status-warning gap-2`}>
                  {widget.rules_out}
                  <span className="text-text-secondary text-xs">rules places out</span>
                </li>
              </ul>
            ) : null}
            <Actions>
              <ActionButton
                variant="primary"
                icon={<Pencil className="size-4" aria-hidden="true" />}
              >
                Edit brief
              </ActionButton>
            </Actions>
          </div>
        </WidgetFrame>
      );
    }
    return (
      <WidgetFrame
        title="Compare places"
        state={widget.state}
        sources={widget.sources}
        missing={widget.missing}
      />
    );
  }

  const chosen = widget.chosen_place ?? null;
  if (chosen && !shownAgain) {
    return (
      <WidgetFrame title="Compare places" state="filled" sources={widget.sources}>
        <div className="flex flex-col gap-3">
          <p className="text-sm font-medium">
            Compared {cards.length} places: you chose {chosen}
          </p>
          <ul className="flex flex-col gap-2" aria-label={`The ${cards.length} places compared`}>
            {cards.map((card) => (
              <li key={card.place} className="flex flex-col text-sm">
                <strong>{card.place}</strong>
                <span className="text-text-secondary">
                  {card.place === chosen ? "You chose this" : "Also compared"}
                </span>
              </li>
            ))}
          </ul>
          <Actions>
            <ActionButton variant="link" onClick={() => setShownAgain(true)}>
              Show again
            </ActionButton>
          </Actions>
        </div>
      </WidgetFrame>
    );
  }

  return (
    <WidgetFrame title="Compare places" state="filled" sources={widget.sources}>
      <div className="@container flex flex-col gap-2">
        <p className="text-text-secondary text-xs @[34rem]:hidden">
          Scroll sideways to see the other places.
        </p>
        <ul
          className="-mx-1 flex snap-x snap-mandatory gap-3 overflow-x-auto px-1 pb-2 @[34rem]:mx-0 @[34rem]:grid @[34rem]:grid-cols-3 @[34rem]:overflow-visible @[34rem]:px-0"
          aria-label="The places, scroll sideways on a phone"
        >
          {cards.map((card) => (
            <li
              key={card.place}
              className="bg-bg-primary border-border-primary relative flex w-72 shrink-0 snap-start flex-col gap-3 rounded-md border p-3 @[34rem]:w-auto"
            >
              <div className="flex items-baseline gap-2">
                <h4 className="font-display text-base font-semibold">{card.place}</h4>
                {card.card_state === "swapped" ? (
                  <span className="text-text-secondary text-xs">Your place</span>
                ) : null}
              </div>
              <CardBody card={card} sources={widget.sources} />
            </li>
          ))}
        </ul>
      </div>
    </WidgetFrame>
  );
}
