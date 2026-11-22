import { MapPin } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { NotKnown } from "./NotKnown";
import { ErrorNote, frameState } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";
import { ActionLink } from "./WidgetParts";

type MapData = components["schemas"]["Map"];
type Place = components["schemas"]["MapPlace"];

function placesOf(widget: MapData): { place: Place; note: string | null }[] {
  const places: { place: Place; note: string | null }[] = [];
  if (widget.centre) places.push({ place: widget.centre, note: "the place you chose" });
  if (widget.hotel) places.push({ place: widget.hotel, note: "your base" });
  for (const stop of widget.stops ?? []) places.push({ place: stop, note: null });
  return places;
}

// The places as a list with links. The list always has everything a map would show, so a map that
// cannot load loses nothing. No map library is installed yet, so no tiles are drawn.
function PlaceList({ places }: { places: { place: Place; note: string | null }[] }) {
  return (
    <ul className="flex flex-col gap-2" aria-label="Places on the map">
      {places.map(({ place, note }, index) => (
        <li key={`${place.name}-${index}`} className="flex items-start gap-2 text-sm">
          <MapPin className="text-text-secondary mt-0.5 size-4 shrink-0" aria-hidden="true" />
          <span className="flex flex-col">
            <span>
              <strong>{place.name}</strong>
              {note ? ` (${note})` : ""}
            </span>
            {place.url ? <ActionLink href={place.url}>See it on a map</ActionLink> : null}
          </span>
        </li>
      ))}
    </ul>
  );
}

export function MapWidget({ widget }: { widget: MapData }) {
  const places = placesOf(widget);
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body =
      places.length > 0 ? (
        <ErrorNote message="The map could not load. The places are listed here instead, so nothing is missing.">
          <PlaceList places={places} />
        </ErrorNote>
      ) : (
        <ErrorNote message="The map could not load. No places are shown." />
      );
  } else if (widget.state === "filled") {
    body =
      places.length === 0 ? (
        <NotKnown missing={widget.missing ?? "the places to show on the map"} />
      ) : (
        <div className="flex flex-col gap-3">
          <PlaceList places={places} />
          {!widget.hotel && (widget.stops ?? []).length === 0 ? (
            <p className="text-text-secondary text-sm">No hotel or stops yet.</p>
          ) : null}
        </div>
      );
  }
  return (
    <WidgetFrame
      title="Map"
      state={frameState(widget.state)}
      sources={widget.sources}
      missing={widget.missing}
    >
      {body}
    </WidgetFrame>
  );
}
