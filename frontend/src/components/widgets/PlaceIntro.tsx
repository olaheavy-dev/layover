import type { components } from "@/lib/api/schema";

import { NotKnown } from "./NotKnown";
import { ErrorNote, frameState } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";

type Intro = components["schemas"]["PlaceIntro"];

// A short introduction from Wikivoyage, or from Wikipedia as the fallback, in the contract's own
// words. The contract carries no photo, so none is shown.
export function PlaceIntro({ widget }: { widget: Intro }) {
  const paragraphs = widget.paragraphs ?? [];
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not read the introduction just now. No introduction is shown." />
    );
  } else if (widget.state === "filled") {
    body =
      paragraphs.length === 0 ? (
        <NotKnown missing={widget.missing ?? `an introduction to ${widget.place}`} />
      ) : (
        <div className="flex flex-col gap-3">
          {widget.hero_line ? <p className="font-display text-lg">{widget.hero_line}</p> : null}
          <blockquote className="border-border-primary flex flex-col gap-2 border-l-2 pl-3">
            {paragraphs.map((text, index) => (
              <p key={index}>{text}</p>
            ))}
          </blockquote>
          {widget.intro_source === "wikipedia" ? (
            <p className="text-text-secondary text-sm">
              Wikivoyage has no guide for this place, so Layover used Wikipedia.
            </p>
          ) : null}
        </div>
      );
  }
  return (
    <WidgetFrame
      title={`About ${widget.place}`}
      state={frameState(widget.state)}
      sources={widget.sources}
      missing={widget.missing}
    >
      {body}
    </WidgetFrame>
  );
}
