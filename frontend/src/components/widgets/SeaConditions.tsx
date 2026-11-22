import type { components } from "@/lib/api/schema";

import { monthName } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote, frameState } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";

type Sea = components["schemas"]["SeaConditions"];

// The sea temperature as the contract gives it, for the place and month it names. An inland place
// gets no widget at all (the backend does not send one), so there is no empty card here.
export function SeaConditions({ widget }: { widget: Sea }) {
  const month = widget.month != null ? monthName(widget.month) : null;
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not check the sea temperature just now. No figure is shown." />
    );
  } else if (widget.state === "filled") {
    body =
      widget.sea_temp_c == null ? (
        <NotKnown missing={widget.missing ?? "sea temperature for this coast"} />
      ) : (
        <p className="font-display flex flex-col text-3xl font-semibold">
          {widget.sea_temp_c}°C
          <span className="text-text-secondary font-sans text-sm font-normal">
            the sea off {widget.place}
            {month ? ` in ${month}` : ""}
          </span>
        </p>
      );
  }
  return (
    <WidgetFrame
      title="Sea temperature"
      state={frameState(widget.state)}
      sources={widget.sources}
      missing={widget.missing}
    >
      {body}
    </WidgetFrame>
  );
}
