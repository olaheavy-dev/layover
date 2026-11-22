import { MapPin } from "lucide-react";
import Image from "next/image";

import { ActionButton } from "../widgets/WidgetParts";

// Sits above the message input on the phone's Chat tab once a trip exists. It shows the place photo
// when one is given and an icon otherwise: the strip's data carries no photo yet (issue #79).
export function TripStrip({
  name,
  factsReady,
  photoSrc,
  photoAlt = "",
  onViewTrip,
}: {
  name: string;
  factsReady?: number;
  photoSrc?: string;
  photoAlt?: string;
  onViewTrip: () => void;
}) {
  return (
    <div
      role="group"
      aria-label="Your trip so far"
      className="bg-bg-secondary border-border-primary flex items-center gap-3 rounded-md border p-3"
    >
      {photoSrc ? (
        <Image
          src={photoSrc}
          alt={photoAlt}
          width={40}
          height={40}
          className="size-10 shrink-0 rounded-md object-cover"
        />
      ) : (
        <span className="bg-bg-tertiary text-accent-primary grid size-10 shrink-0 place-items-center rounded-md">
          <MapPin className="size-5" aria-hidden="true" />
        </span>
      )}
      <p className="flex min-w-0 flex-1 flex-col">
        <span className="truncate text-sm font-semibold">{name}</span>
        {factsReady === undefined ? null : (
          <span className="text-text-secondary text-xs">
            {factsReady} {factsReady === 1 ? "fact" : "facts"} ready
          </span>
        )}
      </p>
      <ActionButton variant="secondary" onClick={onViewTrip}>
        View trip
      </ActionButton>
    </div>
  );
}
