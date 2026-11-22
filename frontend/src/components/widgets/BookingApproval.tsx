import {
  ArrowUpRight,
  Check,
  CircleAlert,
  CircleCheck,
  CircleX,
  FlaskConical,
  Pencil,
  RefreshCw,
  Search,
  X,
} from "lucide-react";

import type { components } from "@/lib/api/schema";

import { dateRange, formatMoney, longDate, plural } from "./format";
import { NotKnown } from "./NotKnown";
import { WidgetFrame } from "./WidgetFrame";
import { ActionButton, ActionLink, Actions, AVIASALES_URL } from "./WidgetParts";

type Booking = components["schemas"]["BookingApproval"];

const SANDBOX = (
  <p className="bg-bg-tertiary text-text-primary border-border-primary inline-flex items-center gap-1.5 self-start rounded-md border px-3 py-1.5 text-sm font-medium">
    <FlaskConical className="size-4" aria-hidden="true" />
    <span>Sandbox: no real booking or payment</span>
  </p>
);

const EYEBROW: Record<string, string> = {
  waiting: "Waiting for your approval",
  flights_only: "Waiting for your approval",
  approved: "Approved",
  declined: "Declined",
  price_changed: "The price changed",
};

function Summary({ rows }: { rows: { name: string; value: React.ReactNode; missing: string }[] }) {
  return (
    <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-sm">
      {rows.map((row) => (
        <div key={row.name} className="contents">
          <dt className="text-text-secondary">{row.name}</dt>
          <dd>{row.value ?? <NotKnown missing={row.missing} />}</dd>
        </div>
      ))}
    </dl>
  );
}

function priceText(money: Booking["sandbox_price"], adults: Booking["adults"]): string | null {
  const text = money ? formatMoney(money) : null;
  if (!text) return null;
  return adults != null ? `${text} for ${adults}` : text;
}

function Status({ tone, children }: { tone: "ok" | "no" | "warn"; children: React.ReactNode }) {
  const style = {
    ok: ["text-status-live", <CircleCheck key="i" className="size-4" aria-hidden="true" />],
    no: ["text-text-secondary", <CircleX key="i" className="size-4" aria-hidden="true" />],
    warn: ["text-status-warning", <CircleAlert key="i" className="size-4" aria-hidden="true" />],
  }[tone];
  return (
    <p className={`${style[0]} inline-flex items-center gap-1.5 text-sm font-medium`}>
      {style[1]}
      {children}
    </p>
  );
}

const Decline = (
  <ActionButton variant="secondary" icon={<X className="size-4" aria-hidden="true" />}>
    Decline
  </ActionButton>
);

export function BookingApproval({ widget }: { widget: Booking }) {
  const frame = (state: "loading" | "filled", body?: React.ReactNode) => (
    <WidgetFrame title="Try booking" state={state} sources={widget.sources} notice={SANDBOX}>
      {body}
    </WidgetFrame>
  );

  if (widget.state === "loading") return frame("loading");

  const route =
    widget.origin && widget.destination ? `${widget.origin} to ${widget.destination}` : null;
  const when =
    widget.depart && widget.return_date ? dateRange(widget.depart, widget.return_date) : null;
  const travellers = widget.adults != null ? plural(widget.adults, "adult") : null;
  const details = [route, when, travellers].filter(Boolean);

  if (widget.state === "error") {
    return frame(
      "filled",
      <div className="flex flex-col items-start gap-2" role="alert">
        <p className="text-status-warning inline-flex items-center gap-1.5 text-sm font-medium">
          <CircleAlert className="size-4" aria-hidden="true" />
          Unavailable
        </p>
        <p className="text-sm">
          Layover could not reach the Duffel sandbox just now. Nothing was ordered.
        </p>
        <ActionButton
          variant="secondary"
          icon={<RefreshCw className="size-4" aria-hidden="true" />}
        >
          Try again
        </ActionButton>
      </div>,
    );
  }

  if (widget.state === "empty") {
    const depart = widget.depart ? longDate(widget.depart) : null;
    return frame(
      "filled",
      <div className="flex flex-col gap-3">
        <p className="text-sm">
          <strong>
            {route
              ? `The sandbox has no offer for ${route}${depart ? ` on ${depart}` : ""}.`
              : "The sandbox has no offer for this trip."}
          </strong>{" "}
          Nothing was ordered.
        </p>
        <Actions>
          <ActionButton variant="secondary" icon={<Pencil className="size-4" aria-hidden="true" />}>
            Edit brief
          </ActionButton>
          <ActionLink
            href={AVIASALES_URL}
            icon={<ArrowUpRight className="size-4" aria-hidden="true" />}
          >
            Look on Aviasales
          </ActionLink>
        </Actions>
      </div>,
    );
  }

  const bookingState = widget.booking_state ?? "waiting";
  const price = priceText(widget.sandbox_price, widget.adults);
  const newPrice = priceText(widget.new_price, widget.adults);
  const newPriceShort = widget.new_price ? formatMoney(widget.new_price) : null;
  const eyebrow = EYEBROW[bookingState];

  const summary = (
    <Summary
      rows={[
        { name: "Flights", value: route, missing: "The flight route" },
        {
          name: "Out",
          value: widget.depart ? longDate(widget.depart) : null,
          missing: "The out date",
        },
        {
          name: "Back",
          value: widget.return_date ? longDate(widget.return_date) : null,
          missing: "The return date",
        },
        { name: "Travellers", value: travellers, missing: "The number of travellers" },
        {
          name: "Price",
          value: price ? (
            <>
              <span className="font-medium">{price}</span>
              <span className="text-text-secondary"> (Sandbox price, not the fare above)</span>
            </>
          ) : null,
          missing: "The sandbox price",
        },
      ]}
    />
  );

  let body: React.ReactNode;
  if (bookingState === "approved") {
    body = (
      <>
        <Status tone="ok">
          {widget.order_ref ? `Approved. Sandbox order ${widget.order_ref}.` : "Approved."}
        </Status>
        {summary}
        <p className="text-text-secondary text-sm">
          No real booking was made and no payment was taken.
        </p>
      </>
    );
  } else if (bookingState === "declined") {
    body = (
      <>
        <Status tone="no">Declined. Nothing was ordered.</Status>
        {details.length > 0 ? (
          <p className="text-text-secondary text-sm">{details.join(", ")}.</p>
        ) : null}
        <Actions>
          <ActionButton variant="link" icon={<Search className="size-4" aria-hidden="true" />}>
            Search again
          </ActionButton>
        </Actions>
      </>
    );
  } else if (bookingState === "price_changed") {
    body = (
      <>
        <Status tone="warn">The price changed at the price check. Layover asks again.</Status>
        <Summary
          rows={[
            { name: "Price you saw", value: price, missing: "The first sandbox price" },
            {
              name: "Price now",
              value: newPrice ? <span className="font-medium">{newPrice}</span> : null,
              missing: "The new sandbox price",
            },
          ]}
        />
        {newPrice ? (
          <p className="text-text-secondary text-sm">
            Nothing is ordered. Approve only if {newPrice} is fine for you. These are sandbox
            prices, not the fare above.
          </p>
        ) : null}
        <Actions>
          {newPriceShort ? (
            <ActionButton variant="primary" icon={<Check className="size-4" aria-hidden="true" />}>
              Approve at {newPriceShort}
            </ActionButton>
          ) : null}
          {Decline}
        </Actions>
      </>
    );
  } else {
    body = (
      <>
        {summary}
        {bookingState === "flights_only" ? (
          <p className="bg-bg-tertiary border-border-primary inline-flex items-center gap-1.5 rounded-md border px-3 py-2 text-sm">
            <CircleAlert className="size-4" aria-hidden="true" />
            Flights only. Layover cannot add a hotel to the sandbox booking yet.
          </p>
        ) : price ? (
          <p className="text-text-secondary text-sm">Nothing is ordered until you press Approve.</p>
        ) : (
          <p className="text-text-secondary text-sm">
            Layover has no sandbox price, so it can&apos;t ask you to approve yet. Nothing was
            ordered.
          </p>
        )}
        <Actions>
          {price ? (
            <ActionButton variant="primary" icon={<Check className="size-4" aria-hidden="true" />}>
              Approve
            </ActionButton>
          ) : null}
          {Decline}
        </Actions>
      </>
    );
  }

  return frame(
    "filled",
    <div className="flex flex-col gap-3">
      <p className="text-text-secondary text-xs font-medium tracking-wide uppercase">{eyebrow}</p>
      {body}
    </div>,
  );
}
