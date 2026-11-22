import type { components } from "@/lib/api/schema";

type MoneyValue = components["schemas"]["MoneyValue"];
type MoneyEstimate = components["schemas"]["MoneyEstimate"];

// The frontend never rounds money (the backend rounds estimates once, to the nearest £10). It
// shows the contract's minor units as given, with integer division only: BigInt keeps it exact.
// Source: Intl.NumberFormat gives the currency's symbol and number of decimal places
// (https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat).
// "GBP" -> "£", "EUR" -> "€". A code Intl doesn't know is shown as the code itself.
export function currencySymbol(code: string): string {
  try {
    const parts = new Intl.NumberFormat("en-GB", {
      style: "currency",
      currency: code,
    }).formatToParts(0);
    return parts.find((part) => part.type === "currency")?.value ?? code;
  } catch {
    return code;
  }
}

export function formatMoney(money: MoneyValue): string {
  const formatter = new Intl.NumberFormat("en-GB", { style: "currency", currency: money.currency });
  const digits = formatter.resolvedOptions().maximumFractionDigits ?? 2;
  const symbol = currencySymbol(money.currency);
  const total = BigInt(money.amount_minor);
  const negative = total < 0n;
  const abs = negative ? -total : total;
  const unit = 10n ** BigInt(digits);
  const major = abs / unit;
  const minor = abs % unit;
  const fraction = minor === 0n ? "" : `.${minor.toString().padStart(digits, "0")}`;
  const gap = /^[A-Za-z]+$/.test(symbol) ? " " : "";
  return `${negative ? "-" : ""}${symbol}${gap}${major.toLocaleString("en-GB")}${fraction}`;
}

// The value the contract says to show: "about £780" for an estimate, "£192" for a listed price.
export function shownMoney(estimate: MoneyEstimate): string {
  return `${estimate.is_estimate ? "about " : ""}${formatMoney(estimate.shown)}`;
}

export function capitalise(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

export function plural(count: number, noun: string): string {
  return `${count} ${noun}${count === 1 ? "" : "s"}`;
}

function parseUtc(value: string): Date | null {
  const date = new Date(`${value.length === 7 ? `${value}-01` : value}T00:00:00Z`);
  return Number.isNaN(date.getTime()) ? null : date;
}

// "2026-03" -> "March 2026"
export function monthYear(value: string): string | null {
  const date = /^\d{4}-\d{2}$/.test(value) ? parseUtc(value) : null;
  if (!date) return null;
  return new Intl.DateTimeFormat("en-GB", {
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

// "2027-05-14" -> "14 May 2027"
export function longDate(value: string): string | null {
  const date = /^\d{4}-\d{2}-\d{2}$/.test(value) ? parseUtc(value) : null;
  if (!date) return null;
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

// "14 to 19 May 2027" within one month; both dates in full otherwise.
export function dateRange(from: string, to: string): string | null {
  const start = longDate(from);
  const end = longDate(to);
  if (!start || !end) return null;
  if (from.slice(0, 7) === to.slice(0, 7)) {
    const day = Number(from.slice(8, 10));
    return `${day} to ${end}`;
  }
  return `${start} to ${end}`;
}

// 5 -> "May". Anything outside 1 to 12 gives null, never a guess.
export function monthName(month: number): string | null {
  if (!Number.isInteger(month) || month < 1 || month > 12) return null;
  return new Intl.DateTimeFormat("en-GB", { month: "long", timeZone: "UTC" }).format(
    new Date(Date.UTC(2000, month - 1, 1)),
  );
}

// "2027-05-15" -> "15 May"
export function dayMonth(value: string): string | null {
  const date = /^\d{4}-\d{2}-\d{2}$/.test(value) ? parseUtc(value) : null;
  if (!date) return null;
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    timeZone: "UTC",
  }).format(date);
}

// "06:20:00" -> "06:20". Anything else gives null.
export function clockTime(value: string): string | null {
  return /^(\d{2}:\d{2})(:\d{2})?$/.exec(value)?.[1] ?? null;
}

// 860 -> "14 h 20 min": whole minutes split into hours and minutes. A unit change only; the
// minutes themselves come from the contract.
export function hoursMinutes(minutes: number): string | null {
  if (!Number.isInteger(minutes) || minutes < 0) return null;
  return `${Math.floor(minutes / 60)} h ${minutes % 60} min`;
}

// ["April", "May", "June"] -> "April, May and June"
export function joinNames(names: string[]): string {
  if (names.length <= 1) return names.join("");
  return `${names.slice(0, -1).join(", ")} and ${names[names.length - 1]}`;
}

// "2026-11-12" -> "12 Nov 2026", the short form the naming conventions use for "updated" dates.
export function shortDate(value: string): string | null {
  const date = /^\d{4}-\d{2}-\d{2}$/.test(value) ? parseUtc(value) : null;
  if (!date) return null;
  return new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  }).format(date);
}

// "2027-05-15" -> "Saturday 15 May 2027". The weekday comes from the date itself.
export function weekdayDate(value: string): string | null {
  const date = /^\d{4}-\d{2}-\d{2}$/.test(value) ? parseUtc(value) : null;
  if (!date) return null;
  const parts = new Intl.DateTimeFormat("en-GB", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).formatToParts(date);
  const get = (type: string) => parts.find((part) => part.type === type)?.value ?? "";
  return `${get("weekday")} ${get("day")} ${get("month")} ${get("year")}`;
}
