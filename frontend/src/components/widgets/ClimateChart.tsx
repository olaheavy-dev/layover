import type { components } from "@/lib/api/schema";

import { joinNames, monthName, plural } from "./format";
import { NotKnown } from "./NotKnown";
import { ErrorNote, frameState } from "./PlaceParts";
import { WidgetFrame } from "./WidgetFrame";

type Climate = components["schemas"]["ClimateChart"];
type Month = components["schemas"]["ClimateMonth"];

const W = 300;
const H = 140;
const PAD = 16;

function scale(values: number[], top: number, bottom: number) {
  const min = Math.min(...values);
  const max = Math.max(...values);
  const span = max === min ? 1 : max - min;
  return (value: number) => bottom - ((value - min) / span) * (bottom - top);
}

// A drawing of the contract's figures: a line for highs, a dotted line for lows and bars for
// rainy days. The scale only places the marks on the page; no figure is worked out here.
function Chart({ months, label }: { months: Month[]; label: string }) {
  const step = months.length > 1 ? (W - 2 * PAD) / (months.length - 1) : 0;
  const x = (index: number) => (months.length > 1 ? PAD + index * step : W / 2);
  const temps = months.flatMap((m) => [m.high_c, m.low_c]).filter((v): v is number => v != null);
  const rains = months.map((m) => m.rainy_days).filter((v): v is number => v != null);
  const y = temps.length > 0 ? scale(temps, PAD, H - PAD - 20) : null;
  const rainMax = rains.length > 0 ? Math.max(...rains, 1) : 1;
  const line = (pick: (m: Month) => number | null | undefined) =>
    months
      .map((m, i) => ({ i, v: pick(m) }))
      .filter((p): p is { i: number; v: number } => p.v != null && y !== null)
      .map((p) => `${x(p.i)},${y?.(p.v)}`)
      .join(" ");
  const barWidth = Math.min(24, step > 0 ? step * 0.5 : 24);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label={label}>
      {months.map((m, i) =>
        m.rainy_days != null ? (
          <rect
            key={`bar-${m.month}`}
            x={x(i) - barWidth / 2}
            y={H - 20 - (m.rainy_days / rainMax) * 30}
            width={barWidth}
            height={(m.rainy_days / rainMax) * 30}
            className="fill-chart-2 opacity-60"
          />
        ) : null,
      )}
      <polyline
        points={line((m) => m.high_c)}
        fill="none"
        strokeWidth="2"
        className="stroke-chart-1"
      />
      <polyline
        points={line((m) => m.low_c)}
        fill="none"
        strokeWidth="2"
        strokeDasharray="3 4"
        className="stroke-chart-1"
      />
      {months.map((m, i) => (
        <text
          key={`label-${m.month}`}
          x={x(i)}
          y={H - 4}
          textAnchor="middle"
          fontSize="10"
          className="fill-text-secondary"
        >
          {(monthName(m.month) ?? "").slice(0, 3)}
        </text>
      ))}
    </svg>
  );
}

function Legend({ items }: { items: { text: string; className: string }[] }) {
  return (
    <ul className="text-text-secondary flex flex-col gap-1 text-xs">
      {items.map((item) => (
        <li key={item.text} className="flex items-center gap-2">
          <span
            className={`inline-block h-0 w-5 border-t-2 ${item.className}`}
            aria-hidden="true"
          />
          {item.text}
        </li>
      ))}
    </ul>
  );
}

// Null when the month has no reading at all: a line with a name and nothing after it says nothing.
function summary(month: Month, name: string): string | null {
  const parts: string[] = [];
  if (month.high_c != null) parts.push(`highs of ${month.high_c}°C`);
  if (month.low_c != null) parts.push(`lows of ${month.low_c}°C`);
  if (month.rainy_days != null) parts.push(plural(month.rainy_days, "rainy day"));
  return parts.length > 0 ? `${name}: ${joinNames(parts)}, typically.` : null;
}

function Cell({ value, unit = "" }: { value: number | null | undefined; unit?: string }) {
  return <td className="py-1.5 pr-3">{value != null ? `${value}${unit}` : "Not known"}</td>;
}

export function ClimateChart({ widget }: { widget: Climate }) {
  const months = widget.months ?? [];
  const names = months.map((m) => monthName(m.month)).filter((n): n is string => n !== null);
  const period = widget.averages_period?.replace("-", " to ") ?? null;
  const highlight = months.find((m) => m.month === widget.highlight_month);
  const highlightName = highlight ? monthName(highlight.month) : null;
  const highlightSummary = highlight && highlightName ? summary(highlight, highlightName) : null;
  const hasRain = months.some((m) => m.rainy_days != null);

  let body: React.ReactNode = null;
  if (widget.state === "error") {
    body = (
      <ErrorNote message="Layover could not check the typical weather just now. No temperatures or rainy days are shown." />
    );
  } else if (months.length === 0) {
    body = <NotKnown missing={widget.missing ?? "typical weather for this place and period"} />;
  } else if (widget.state === "filled" || widget.state === "not_known") {
    body = (
      <div className="flex flex-col gap-3">
        {highlightSummary ? <p>{highlightSummary}</p> : null}
        <Chart
          months={months}
          label={`Chart of typical weather for ${joinNames(names)}. The table has the same figures.`}
        />
        <Legend
          items={[
            { text: "Typical high (line)", className: "border-chart-1" },
            { text: "Typical low (dotted line)", className: "border-chart-1 border-dotted" },
            ...(hasRain
              ? [{ text: "Rainy days in the month (bars)", className: "border-chart-2" }]
              : []),
          ]}
        />
        {widget.state === "not_known" && widget.missing ? (
          <NotKnown missing={widget.missing} />
        ) : null}
        <details>
          <summary className="text-text-link min-h-11 cursor-pointer text-sm underline">
            Show as table
          </summary>
          <table className="w-full text-left text-sm">
            <caption className="text-text-secondary pb-2 text-left text-xs">
              Typical weather{period ? `, averages for ${period}` : ""}
            </caption>
            <thead>
              <tr className="border-border-primary border-b">
                <th scope="col" className="py-1.5 pr-3 font-medium">
                  Month
                </th>
                <th scope="col" className="py-1.5 pr-3 font-medium">
                  High
                </th>
                <th scope="col" className="py-1.5 pr-3 font-medium">
                  Low
                </th>
                <th scope="col" className="py-1.5 pr-3 font-medium">
                  Rainy days
                </th>
              </tr>
            </thead>
            <tbody>
              {months.map((m) => (
                <tr key={m.month} className="border-border-primary border-b last:border-b-0">
                  <th scope="row" className="py-1.5 pr-3 font-medium">
                    {monthName(m.month) ?? "Not known"}
                  </th>
                  <Cell value={m.high_c} unit="°C" />
                  <Cell value={m.low_c} unit="°C" />
                  <Cell value={m.rainy_days} />
                </tr>
              ))}
            </tbody>
          </table>
        </details>
      </div>
    );
  }
  return (
    <WidgetFrame
      title={names.length > 0 ? `Weather in ${joinNames(names)}` : "Weather"}
      state={frameState(
        widget.state === "not_known" && months.length > 0 ? "filled" : widget.state,
      )}
      sources={widget.sources}
      missing={widget.missing}
    >
      {body}
    </WidgetFrame>
  );
}
