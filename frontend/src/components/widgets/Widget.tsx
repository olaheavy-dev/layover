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
import { FareList } from "./FareList";
import { HotelList } from "./HotelList";
import { ItineraryDay } from "./ItineraryDay";
import { MapWidget } from "./MapWidget";
import { Money } from "./Money";
import { NotKnown } from "./NotKnown";
import { NotKnownWidget } from "./NotKnownWidget";
import { PlaceIntro } from "./PlaceIntro";
import { PublicHolidays } from "./PublicHolidays";
import { SeaConditions } from "./SeaConditions";
import { TimeDifference } from "./TimeDifference";
import { TransportRoute } from "./TransportRoute";
import { WebResults } from "./WebResults";

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
  itinerary_day: ItineraryDay,
  hotel_list: HotelList,
  web_results: WebResults,
  not_known: NotKnownWidget,
  public_holidays: PublicHolidays,
  time_difference: TimeDifference,
  fare_list: FareList,
  transport_route: TransportRoute,
};

export function Widget({ widget }: { widget: AnyWidget }) {
  const Component = REGISTRY[widget.kind];
  if (!Component) {
    return <NotKnown missing="This part of the trip can't be shown" />;
  }
  return <Component widget={widget} />;
}
