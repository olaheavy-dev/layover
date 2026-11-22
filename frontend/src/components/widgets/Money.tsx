import type { components } from "@/lib/api/schema";

import { currencySymbol, formatMoney, shortDate } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote, frameState } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";

type MoneyWidget = components["schemas"]["Money"];

// The exchange rate with its date, and a conversion only when the contract carries one. The
// frontend does no conversion: every figure is the contract's (decision 0011 rule 3).
export function Money({ widget }: { widget: MoneyWidget }) {
  const rate =
    widget.rate && widget.to_currency
      ? `${currencySymbol(widget.from_currency)}1 = ${currencySymbol(widget.to_currency)}${widget.rate}`
      : null;
  const date = widget.rate_date ? shortDate(widget.rate_date) : null;
  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not check the exchange rate just now. No rate is shown." />
    );
  } else if (widget.state === "filled") {
    body = !rate ? (
      <NotKnown missing={widget.missing ?? "the exchange rate"} />
    ) : (
      <div className="flex flex-col gap-2">
        {widget.conversion ? (
          <>
            <p className="font-display flex flex-col text-3xl font-semibold">
              {formatMoney(widget.conversion.amount)}
              <span className="text-text-secondary font-sans text-sm font-normal">
                is about {formatMoney(widget.conversion.converted)} at {rate}
              </span>
            </p>
            <p className="text-text-secondary text-sm">
              Worked out by Layover&apos;s code, not by the model.
            </p>
          </>
        ) : (
          <p className="font-display text-3xl font-semibold">{rate}</p>
        )}
        {date ? <p className="text-text-secondary text-sm">Rate for {date}</p> : null}
      </div>
    );
  }
  return (
    <WidgetFrame
      title="Money"
      state={frameState(widget.state)}
      sources={widget.sources}
      missing={widget.missing}
    >
      {body}
    </WidgetFrame>
  );
}
