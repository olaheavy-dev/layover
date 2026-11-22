import { Circle } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { WidgetFrame } from "./WidgetFrame";

type NotKnownContract = components["schemas"]["NotKnown"];

// The standalone "Not known" answer: what is missing, why, and what Layover can do instead. Each
// row comes from the contract; a row it does not give is left out, never filled in.
export function NotKnownWidget({ widget }: { widget: NotKnownContract }) {
  const rows = [
    { name: "What is missing", value: widget.missing },
    { name: "Why", value: widget.reason },
    { name: "What Layover can do", value: widget.instead },
  ].filter((row) => row.value);
  return (
    <WidgetFrame
      title={widget.missing ?? "Not known"}
      state={widget.state === "loading" ? "loading" : "filled"}
      sources={widget.sources}
      notice={
        <p className="text-status-not-known inline-flex items-center gap-1.5 self-start text-sm italic">
          <Circle className="size-3" aria-hidden="true" />
          <span>Not known</span>
        </p>
      }
    >
      <dl className="flex flex-col gap-2 text-sm">
        {rows.map((row) => (
          <div key={row.name}>
            <dt className="text-text-secondary">{row.name}</dt>
            <dd>{row.value}</dd>
          </div>
        ))}
      </dl>
    </WidgetFrame>
  );
}
