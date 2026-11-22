import { CircleCheck, Pencil } from "lucide-react";

import type { components } from "@/lib/api/schema";

import { formatMoney, plural } from "./format";
import { PreviewForm } from "./PreviewForm";
import { ActionButton, Actions, CHIP, Chips } from "./WidgetParts";
import { WidgetFrame } from "./WidgetFrame";

type Brief = components["schemas"]["BriefSummary"];

// The chips come only from fields the brief has. A missing field gets no chip: the chat asks for
// it, and the widget never guesses one (journey board, "Your brief").
export function chipsOf(brief: Brief): { key: string; text: string }[] {
  const chips: { key: string; text: string }[] = [];
  if (brief.origin) chips.push({ key: "origin", text: `From ${brief.origin}` });
  const trip = [
    brief.when ?? null,
    brief.nights != null ? plural(brief.nights, "night") : null,
  ].filter(Boolean);
  if (trip.length > 0) chips.push({ key: "when", text: trip.join(" · ") });
  if (brief.adults != null) chips.push({ key: "adults", text: plural(brief.adults, "adult") });
  const budget = brief.budget ? formatMoney(brief.budget) : null;
  if (budget) chips.push({ key: "budget", text: `${budget} in total` });
  if (brief.feel) chips.push({ key: "feel", text: brief.feel });
  return chips;
}

const EYEBROW: Record<string, string> = {
  waiting: "Waiting for your OK",
  editing: "Editing",
  confirmed: "Confirmed",
};

export function BriefSummary({ widget }: { widget: Brief }) {
  const briefState = widget.brief_state ?? "waiting";
  const chips = chipsOf(widget);
  const editIcon = <Pencil className="size-4" aria-hidden="true" />;
  return (
    <WidgetFrame
      title="Your brief"
      state={widget.state}
      sources={widget.sources}
      missing={widget.missing}
    >
      <div className="flex flex-col gap-3">
        <p className="text-text-secondary text-xs font-medium tracking-wide uppercase">
          {EYEBROW[briefState]}
        </p>
        {briefState === "confirmed" ? (
          <>
            <Chips label="Your confirmed brief">
              {chips.map((chip) => (
                <li key={chip.key} className={CHIP}>
                  {chip.text}
                </li>
              ))}
            </Chips>
            <p className="text-status-live inline-flex items-center gap-1.5 text-sm">
              <CircleCheck className="size-4" aria-hidden="true" />
              Confirmed by you
            </p>
            <Actions>
              <ActionButton variant="link" icon={editIcon}>
                Edit
              </ActionButton>
            </Actions>
          </>
        ) : (
          <>
            <Chips
              label={
                briefState === "editing"
                  ? "Your brief, editing the budget"
                  : "Your brief, waiting for your OK"
              }
            >
              {chips.map((chip) =>
                briefState === "editing" && chip.key === "budget" ? (
                  <li key={chip.key} className="basis-full">
                    <PreviewForm className="flex flex-col gap-2">
                      <label htmlFor="brief-budget" className="text-sm font-medium">
                        Budget
                      </label>
                      <div className="flex flex-wrap items-center gap-2">
                        <input
                          id="brief-budget"
                          type="text"
                          inputMode="decimal"
                          defaultValue={(widget.budget && formatMoney(widget.budget)) || ""}
                          className="border-border-control bg-bg-primary text-text-primary min-h-11 w-40 rounded-md border px-3 text-sm"
                        />
                        <ActionButton variant="primary">Save</ActionButton>
                        <ActionButton variant="link">Cancel</ActionButton>
                      </div>
                      <p className="text-text-secondary text-xs">
                        Press Enter to save. The brief updates before any search starts.
                      </p>
                    </PreviewForm>
                  </li>
                ) : (
                  <li key={chip.key}>
                    <button type="button" className={`${CHIP} gap-1.5`}>
                      {chip.text} <Pencil className="size-3" aria-hidden="true" />
                      <span className="sr-only">(edit)</span>
                    </button>
                  </li>
                ),
              )}
            </Chips>
            {briefState === "waiting" ? (
              <p className="text-text-secondary text-sm">
                Nothing is searched until you confirm. Tap a part to change it.
              </p>
            ) : null}
            <Actions>
              <ActionButton
                variant="primary"
                icon={<CircleCheck className="size-4" aria-hidden="true" />}
              >
                Confirm brief
              </ActionButton>
              {briefState === "waiting" ? (
                <ActionButton variant="secondary" icon={editIcon}>
                  Edit brief
                </ActionButton>
              ) : null}
            </Actions>
          </>
        )}
      </div>
    </WidgetFrame>
  );
}
