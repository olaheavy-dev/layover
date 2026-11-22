import type { ComponentType } from "react";

import type { SampleWidget } from "@/lib/samples";

import { BookingApproval } from "./BookingApproval";
import { BriefSummary } from "./BriefSummary";
import { ComparisonTable } from "./ComparisonTable";
import { CostEstimate } from "./CostEstimate";
import { FareCard } from "./FareCard";
import { NotKnown } from "./NotKnown";

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
};

export function Widget({ widget }: { widget: AnyWidget }) {
  const Component = REGISTRY[widget.kind];
  if (!Component) {
    return <NotKnown missing="This part of the trip can't be shown" />;
  }
  return <Component widget={widget} />;
}
