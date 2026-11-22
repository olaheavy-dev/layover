import { Globe } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { shortDate } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";

type Web = components["schemas"]["WebResults"];

const LABEL = "From a web search, not checked by Layover";

// Only http and https addresses become links. The host is read from the address itself.
function parse(value: string): URL | null {
  try {
    const url = new URL(value);
    return url.protocol === "http:" || url.protocol === "https:" ? url : null;
  } catch {
    return null;
  }
}

// Web results: short quotes with links and the retrieval date. They are never Live or Cached
// facts, so they carry their own label, and the widget has no "Add to trip" action (decision 0011
// rules 1 and 2).
export function WebResults({ widget }: { widget: Web }) {
  // A result with no usable http or https link is left out: each result shown has its link.
  const results = (widget.results ?? []).flatMap((result) => {
    const url = parse(result.url);
    return url ? [{ ...result, url }] : [];
  });
  // Parse the time, then format it in UTC, as the other date helpers do.
  const time = widget.retrieved_at ? new Date(widget.retrieved_at) : null;
  const retrieved =
    time && !Number.isNaN(time.getTime()) ? shortDate(time.toISOString().slice(0, 10)) : null;
  const showFooter = widget.state === "filled" && results.length > 0;
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="I can’t help with that yet. The web search did not answer just now." />
    );
  } else if (widget.state === "empty" || (widget.state === "filled" && results.length === 0)) {
    body = (
      <p className="text-sm">I can’t help with that yet. The web search found nothing I can use.</p>
    );
  } else if (widget.state === "not_known") {
    body = <NotKnown missing={widget.missing ?? "the web results"} />;
  } else if (widget.state === "filled") {
    body = (
      <div className="flex flex-col gap-3">
        <p className="bg-bg-tertiary text-text-primary border-border-primary inline-flex items-center gap-1.5 self-start rounded-md border px-3 py-1.5 text-sm font-medium">
          <Globe className="size-4" aria-hidden="true" />
          <span>{LABEL}</span>
        </p>
        {retrieved ? null : <NotKnown missing="when these results were retrieved" />}
        <ul className="flex flex-col gap-4">
          {results.map((result, index) => {
            const url = result.url;
            const meta = [url.host, retrieved ? `Retrieved ${retrieved}` : null]
              .filter(Boolean)
              .join(" · ");
            return (
              <li key={`${result.url.href}-${index}`} className="flex flex-col gap-1 text-sm">
                <p className="font-medium">
                  <a
                    href={url.href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-text-link underline"
                  >
                    {result.title}
                  </a>
                </p>
                <blockquote className="border-border-primary border-l-2 pl-3">
                  “{result.quote}”
                </blockquote>
                {meta ? <p className="text-text-secondary text-xs">{meta}</p> : null}
              </li>
            );
          })}
        </ul>
      </div>
    );
  }
  return (
    <WidgetFrame
      title="Web results"
      state={widget.state === "loading" ? "loading" : "filled"}
      sources={[]}
      footerNote={
        showFooter ? (
          <>
            {retrieved ? (
              <span className="text-text-secondary text-xs">Retrieved {retrieved}</span>
            ) : null}
            {widget.sources.map((label, index) => (
              <span key={`${label.source}-${index}`} className="text-text-secondary text-xs">
                Source: {label.source}
              </span>
            ))}
          </>
        ) : undefined
      }
    >
      {body}
    </WidgetFrame>
  );
}
