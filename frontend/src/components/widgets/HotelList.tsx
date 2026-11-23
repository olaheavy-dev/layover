import { Circle, MapPinned, Star } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { plural } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";
import { ActionButton, Actions } from "./WidgetParts";

type HotelListWidget = components["schemas"]["HotelList"];
type Hotel = components["schemas"]["Hotel"];

const TITLE = "Where you’re staying";

function Banner({ children }: { children: React.ReactNode }) {
  return (
    <p className="bg-bg-tertiary text-text-primary border-border-primary inline-flex items-start gap-1.5 self-start rounded-md border px-3 py-1.5 text-sm">
      <MapPinned className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
      <span>{children}</span>
    </p>
  );
}

function NotKnownValue() {
  return (
    <span className="text-status-not-known inline-flex items-center gap-1.5 italic">
      <Circle className="size-3" aria-hidden="true" />
      <span>Not known</span>
    </span>
  );
}

// Only http and https addresses become links; anything else is shown as text.
function website(value: string): React.ReactNode {
  try {
    const url = new URL(value);
    if (url.protocol !== "http:" && url.protocol !== "https:") return <NotKnownValue />;
    return (
      <a
        href={url.href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-text-link underline"
      >
        {url.host}
      </a>
    );
  } catch {
    return <NotKnownValue />;
  }
}

function Row({
  hotel,
  isBase,
  actionLabel,
}: {
  hotel: Hotel;
  isBase: boolean;
  actionLabel: string;
}) {
  return (
    <li
      className={`flex flex-wrap items-start justify-between gap-3 rounded-md border p-3 ${
        isBase ? "border-accent-primary bg-bg-tertiary" : "border-border-primary"
      }`}
    >
      <div className="flex min-w-0 flex-col gap-1 text-sm">
        <strong className="font-medium">{hotel.name}</strong>
        {hotel.area ? <p className="text-text-secondary">{hotel.area}</p> : null}
        <dl className="flex flex-wrap gap-x-4 gap-y-1">
          <div className="flex gap-1.5">
            <dt className="text-text-secondary">Stars</dt>
            <dd>{hotel.stars != null ? plural(hotel.stars, "star") : <NotKnownValue />}</dd>
          </div>
          <div className="flex gap-1.5">
            <dt className="text-text-secondary">Website</dt>
            <dd>{hotel.website ? website(hotel.website) : <NotKnownValue />}</dd>
          </div>
        </dl>
      </div>
      {isBase ? (
        <p className="text-text-primary inline-flex min-h-11 items-center gap-1.5 text-sm font-medium">
          <Star className="size-4" aria-hidden="true" />
          <span>Your base</span>
        </p>
      ) : (
        <ActionButton variant="secondary">{actionLabel}</ActionButton>
      )}
    </li>
  );
}

const SKIP = <ActionButton variant="link">Skip, start from the centre</ActionButton>;

// Hotels from OpenStreetMap with names, areas, stars and websites. The contract carries no prices,
// so none is shown. The traveller chooses one as the base for the days, or skips.
export function HotelList({ widget }: { widget: HotelListWidget }) {
  const hotels = widget.hotels ?? [];
  const chosen = hotels.find((hotel) => hotel.name === widget.chosen_hotel);
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not read the hotel list from OpenStreetMap just now.">
        {SKIP}
      </ErrorNote>
    );
  } else if (widget.state !== "empty" && widget.selection !== "skipped" && hotels.length === 0) {
    body = <NotKnown missing={widget.missing ?? `the hotels near ${widget.place}`} />;
  } else if (widget.state === "empty") {
    body = (
      <div className="flex flex-col items-start gap-2 text-sm">
        <p>
          <strong>No hotels are tagged near {widget.place} in OpenStreetMap.</strong> Layover looked
          for hotels and guesthouses around the centre.
        </p>
        <Banner>Days start from the centre of {widget.place}.</Banner>
        <Actions>
          <ActionButton variant="primary">Go to Days</ActionButton>
        </Actions>
      </div>
    );
  } else if (widget.selection === "skipped") {
    body = (
      <div className="flex flex-col items-start gap-2">
        <Banner>You skipped the hotel. Days start from the centre of {widget.place}.</Banner>
        <ActionButton variant="link">Choose a hotel</ActionButton>
      </div>
    );
  } else if (widget.state === "filled" || widget.state === "not_known") {
    const decided = widget.selection === "chosen" || widget.selection === "changed";
    body = (
      <div className="flex flex-col gap-3">
        {decided && chosen ? (
          <Banner>
            {widget.selection === "changed"
              ? `You changed your base to ${chosen.name}. The days are rebuilt from it.`
              : `Days start from ${chosen.name}.`}
          </Banner>
        ) : decided ? (
          <p className="text-text-secondary text-sm">A hotel was chosen. Its name is not known.</p>
        ) : (
          <p className="text-text-secondary text-sm">
            No prices: Layover’s sources have none. Choose one as the base for your days, or skip.
          </p>
        )}
        <ul className="flex flex-col gap-2">
          {hotels.map((hotel, index) => (
            <Row
              key={`${hotel.name}-${index}`}
              hotel={hotel}
              isBase={decided && hotel === chosen}
              actionLabel={decided ? "Choose instead" : "Stay here"}
            />
          ))}
        </ul>
        {decided ? null : <Actions>{SKIP}</Actions>}
      </div>
    );
  }
  return (
    <WidgetFrame
      title={TITLE}
      state={widget.state === "loading" ? "loading" : "filled"}
      sources={widget.sources}
    >
      {body}
    </WidgetFrame>
  );
}
