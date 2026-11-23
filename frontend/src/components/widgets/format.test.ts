import {
  clockTime,
  durationWords,
  currencySymbol,
  dateRange,
  dayMonth,
  hoursMinutes,
  joinNames,
  monthName,
  formatMoney,
  longDate,
  monthYear,
  plural,
  shortDate,
  shortWeekdayDate,
  shownMoney,
  utcOffset,
  weekdayDate,
} from "./format";

// Expected values are worked out by hand. Source: the contract's MoneyValue (integer minor units,
// two decimal places for GBP, EUR and CHF) and sample-data.md for the Lisbon figures.
describe("formatMoney", () => {
  it("shows whole pounds without pence", () => {
    // Working: 80000 pence / 100 = 800 remainder 0, so "£800".
    expect(formatMoney({ amount_minor: 80000, currency: "GBP" })).toBe("£800");
  });

  it("shows pence when there are some, padded to two digits", () => {
    // Working: 1250 / 100 = 12 remainder 50 -> "£12.50"; 5 / 100 = 0 remainder 5 -> "£0.05".
    expect(formatMoney({ amount_minor: 1250, currency: "GBP" })).toBe("£12.50");
    expect(formatMoney({ amount_minor: 5, currency: "GBP" })).toBe("£0.05");
  });

  it("never rounds: the exact figure is shown as given", () => {
    // Working: 78200 / 100 = 782 remainder 0. 78249 / 100 = 782 remainder 49, kept, not rounded.
    expect(formatMoney({ amount_minor: 78200, currency: "GBP" })).toBe("£782");
    expect(formatMoney({ amount_minor: 78249, currency: "GBP" })).toBe("£782.49");
  });

  it("groups thousands and stays exact above the float comfort zone", () => {
    // Working: 123456789 / 100 = 1234567 remainder 89.
    expect(formatMoney({ amount_minor: 123456789, currency: "GBP" })).toBe("£1,234,567.89");
  });

  it("puts the sign before the symbol", () => {
    // Working: -1800 -> sign, then 1800 / 100 = 18 remainder 0.
    expect(formatMoney({ amount_minor: -1800, currency: "GBP" })).toBe("-£18");
  });

  it("uses the currency's own symbol, or its code with a space", () => {
    // Working: 2100 / 100 = 21 remainder 0. CHF has no one-character symbol in en-GB.
    expect(formatMoney({ amount_minor: 2100, currency: "EUR" })).toBe("€21");
    expect(formatMoney({ amount_minor: 1000, currency: "CHF" })).toBe("CHF 10");
  });
});

describe("formatMoney with a bad amount or currency", () => {
  it.each([
    ["a fraction", { amount_minor: 1.5, currency: "GBP" }],
    ["not a number", { amount_minor: Number.NaN, currency: "GBP" }],
    ["infinity", { amount_minor: Number.POSITIVE_INFINITY, currency: "GBP" }],
    ["beyond a safe integer", { amount_minor: 2 ** 53, currency: "GBP" }],
    ["a lower-case currency", { amount_minor: 100, currency: "gbp" }],
    ["a currency of two letters", { amount_minor: 100, currency: "GB" }],
    ["a currency of four letters", { amount_minor: 100, currency: "GBPX" }],
    ["an empty currency", { amount_minor: 100, currency: "" }],
  ])("gives null for %s, never a crash or a made-up figure", (_name, money) => {
    expect(formatMoney(money)).toBeNull();
  });

  it("still shows the largest safe integer exactly", () => {
    // Working: 9007199254740991 minor units = 90,071,992,547,409.91 pounds (2^53 - 1, the largest safe integer).
    expect(formatMoney({ amount_minor: Number.MAX_SAFE_INTEGER, currency: "GBP" })).toBe(
      "£90,071,992,547,409.91",
    );
  });
});

describe("shownMoney", () => {
  it("gives null when the shown value is bad", () => {
    const bad = { is_estimate: true, shown: { amount_minor: 1.5, currency: "GBP" } };
    expect(shownMoney(bad as never)).toBeNull();
  });

  it("adds 'about' only for an estimate and uses the shown value, never the exact one", () => {
    // Source: cost_estimate/filled.json total: exact 78200, shown 78000, estimate.
    const total = {
      exact: { amount_minor: 78200, currency: "GBP" },
      shown: { amount_minor: 78000, currency: "GBP" },
      is_estimate: true,
    };
    expect(shownMoney(total)).toBe("about £780");
    // Source: cost_estimate/filled.json flights: not an estimate.
    const flights = {
      exact: { amount_minor: 19200, currency: "GBP" },
      shown: { amount_minor: 19200, currency: "GBP" },
      is_estimate: false,
    };
    expect(shownMoney(flights)).toBe("£192");
  });
});

describe("dates and counts", () => {
  it("formats a month and a day", () => {
    expect(monthYear("2026-03")).toBe("March 2026");
    expect(monthYear("nonsense")).toBeNull();
    expect(longDate("2027-05-14")).toBe("14 May 2027");
    expect(longDate("nonsense")).toBeNull();
  });

  it("joins two dates in one month, and keeps both in full when the months differ", () => {
    expect(dateRange("2027-05-14", "2027-05-19")).toBe("14 to 19 May 2027");
    expect(dateRange("2027-05-30", "2027-06-04")).toBe("30 May 2027 to 4 June 2027");
  });

  it("says one or many", () => {
    expect(plural(1, "night")).toBe("1 night");
    expect(plural(5, "night")).toBe("5 nights");
  });
});

describe("place widget formats", () => {
  it("names months and rejects numbers outside 1 to 12", () => {
    // Working: month 5 is the fifth month, May. 0 and 13 are not months.
    expect(monthName(5)).toBe("May");
    expect(monthName(0)).toBeNull();
    expect(monthName(13)).toBeNull();
  });

  it("shows a day and month, and a clock time without seconds", () => {
    expect(dayMonth("2027-05-15")).toBe("15 May");
    expect(dayMonth("May")).toBeNull();
    expect(clockTime("06:20:00")).toBe("06:20");
    expect(clockTime("late")).toBeNull();
  });

  it("splits minutes into hours and minutes", () => {
    // Working: 860 = 14 x 60 (840) + 20, so "14 h 20 min". 60 = 1 h 0 min.
    expect(hoursMinutes(860)).toBe("14 h 20 min");
    expect(hoursMinutes(60)).toBe("1 h 0 min");
    expect(hoursMinutes(-1)).toBeNull();
  });

  it("joins names and finds currency symbols", () => {
    expect(joinNames(["April", "May", "June"])).toBe("April, May and June");
    expect(joinNames(["May"])).toBe("May");
    expect(currencySymbol("GBP")).toBe("£");
    expect(currencySymbol("EUR")).toBe("€");
    expect(currencySymbol("??")).toBe("??");
  });
});

describe("shortDate", () => {
  it("shows the day, the short month and the year", () => {
    // Working: 2026-11-12 is day 12, month 11 (Nov), year 2026.
    expect(shortDate("2026-11-12")).toBe("12 Nov 2026");
    expect(shortDate("12 November")).toBeNull();
  });
});

describe("weekdayDate", () => {
  it("shows the weekday, the day, the month and the year", () => {
    // Working: 1 Jan 2027 is a Friday; 15 May is day 135 of 2027 and (135 - 1) mod 7 = 1, so it is a
    // Saturday and 14 May 2027 is a Friday (the board's "Day 1, Friday 14 May 2027"). Source: the
    // Gregorian calendar (see the shortWeekdayDate working below).
    expect(weekdayDate("2027-05-15")).toBe("Saturday 15 May 2027");
    expect(weekdayDate("15 May")).toBeNull();
  });
});

// Source: the Gregorian calendar. 17 May 2027 is a Monday (1 Jan 2027 was a Friday; 31 + 28 + 31 +
// 30 = 120 days to 1 May, 120 mod 7 = 1, so 1 May is a Saturday; the 17th is 16 days later, 16 mod 7
// = 2, so Monday).
describe("shortWeekdayDate", () => {
  it("gives the short weekday and the full date", () => {
    expect(shortWeekdayDate("2027-05-17")).toBe("Mon 17 May 2027");
    expect(shortWeekdayDate("2027-05-15")).toBe("Sat 15 May 2027");
  });
  it("gives null for anything that is not a date", () => {
    expect(shortWeekdayDate("May")).toBeNull();
  });
});

// Whole minutes into words: a unit change only. 60 min = 1 hour; 90 min = 1 hour 30 minutes.
describe("durationWords", () => {
  it("says hours and minutes in words, singular and plural", () => {
    expect(durationWords(60)).toBe("1 hour");
    expect(durationWords(120)).toBe("2 hours");
    expect(durationWords(90)).toBe("1 hour 30 minutes");
    expect(durationWords(45)).toBe("45 minutes");
    expect(durationWords(330)).toBe("5 hours 30 minutes");
  });
  it("gives null for a negative or fractional number", () => {
    expect(durationWords(-60)).toBeNull();
    expect(durationWords(1.5)).toBeNull();
  });
});

// An offset in minutes as the UTC offset the zone database gives: 60 min = UTC+1; 330 = UTC+5:30.
describe("utcOffset", () => {
  it("formats positive, negative and zero offsets", () => {
    expect(utcOffset(60)).toBe("UTC+1");
    expect(utcOffset(120)).toBe("UTC+2");
    expect(utcOffset(330)).toBe("UTC+5:30");
    expect(utcOffset(-300)).toBe("UTC-5");
    expect(utcOffset(0)).toBe("UTC");
  });
  it("gives null for a fractional number", () => {
    expect(utcOffset(0.5)).toBeNull();
  });
});
