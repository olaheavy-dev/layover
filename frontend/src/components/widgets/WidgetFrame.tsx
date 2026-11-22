import { CircleAlert } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { NotKnown } from "./NotKnown";
import { SourceLabel } from "./SourceLabel";

type Label = components["schemas"]["SourceLabel"];
export type WidgetState = "loading" | "filled" | "empty" | "error" | "not_known";

// The card every widget sits in: a title, the body for its state, and the source footer.
// `children` is the filled body. The other states have a shared shape so each widget needn't
// rebuild them.
export function WidgetFrame({
  title,
  state,
  sources,
  missing,
  emptyText = "Nothing to show yet",
  now,
  notice,
  footerNote,
  children,
}: {
  title: string;
  state: WidgetState;
  sources: Label[];
  missing?: string | null;
  emptyText?: string;
  now?: Date;
  // A line that stays above the body in every state, such as "Sandbox: no real booking or payment".
  notice?: React.ReactNode;
  // A short fixed label that sits in the footer beside the source labels.
  footerNote?: React.ReactNode;
  children?: React.ReactNode;
}) {
  let body: React.ReactNode;
  switch (state) {
    case "loading":
      body = (
        <div className="flex flex-col gap-2" role="status">
          <span className="sr-only">Loading {title}</span>
          <div className="bg-bg-tertiary h-4 w-2/3 rounded-sm" aria-hidden="true" />
          <div className="bg-bg-tertiary h-4 w-1/2 rounded-sm" aria-hidden="true" />
        </div>
      );
      break;
    case "empty":
      body = <p className="text-text-secondary text-sm">{emptyText}</p>;
      break;
    case "error":
      body = (
        <p className="text-status-warning inline-flex items-center gap-1.5 text-sm" role="alert">
          <CircleAlert className="size-4" aria-hidden="true" />
          <span>This part of the trip couldn&apos;t load. Try again in a moment.</span>
        </p>
      );
      break;
    case "not_known":
      body = <NotKnown missing={missing ?? title} />;
      break;
    case "filled":
      body = children;
      break;
  }
  return (
    <section
      className="bg-bg-secondary border-border-primary flex flex-col gap-3 rounded-md border p-4"
      aria-busy={state === "loading"}
    >
      <h3 className="font-display text-lg font-semibold">{title}</h3>
      {notice}
      {body}
      {sources.length > 0 || footerNote ? (
        <footer className="border-border-primary flex flex-wrap gap-x-4 gap-y-1 border-t pt-2">
          {sources.map((label, index) => (
            <SourceLabel key={`${label.source}-${index}`} label={label} now={now} />
          ))}
          {footerNote}
        </footer>
      ) : null}
    </section>
  );
}
