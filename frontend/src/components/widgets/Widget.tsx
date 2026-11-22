import type { ComponentType } from "react";

import type { SampleWidget } from "@/lib/samples";

import { AdviceCard } from "./AdviceCard";
import { BookingApproval } from "./BookingApproval";
import { BriefSummary } from "./BriefSummary";
import { ClimateChart } from "./ClimateChart";
import { ComparisonTable } from "./ComparisonTable";
import { CostEstimate } from "./CostEstimate";
import { Daylight } from "./Daylight";
import { FareCard } from "./FareCard";
import { MapWidget } from "./MapWidget";
import { Money } from "./Money";
import { NotKnown } from "./NotKnown";
import { PlaceIntro } from "./PlaceIntro";
import { SeaConditions } from "./SeaConditions";

type AnyWidget = SampleWidget["widget"];

// Widget components by `kind`. Each widget task adds its own entry here. A kind with no entry,
// or a value that doesn't match the contract, falls through to Not known and never throws.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const REGISTRY: Partial<Record<string, ComponentType<{ widget: any }>>> = {
  brief_summary: BriefSummary,
  comparison_table: ComparisonTable,
  fare_card: FareCard,
  cost_estimate: CostEstimate,
  booking_approval: BookingApproval,
  climate_chart: ClimateChart,
  sea_conditions: SeaConditions,
  daylight: Daylight,
  money: Money,
  advice_card: AdviceCard,
  place_intro: PlaceIntro,
  map: MapWidget,
};

export function Widget({ widget }: { widget: AnyWidget }) {
  const Component = REGISTRY[widget.kind];
  if (!Component) {
    return <NotKnown missing="This part of the trip can't be shown" />;
  }
  return <Component widget={widget} />;
}
