import type { ComponentType } from "react";

import type { SampleWidget } from "@/lib/samples";

import { NotKnown } from "./NotKnown";

type AnyWidget = SampleWidget["widget"];

// Widget components by `kind`. Each widget task adds its own entry here. A kind with no entry,
// or a value that doesn't match the contract, falls through to Not known and never throws.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const REGISTRY: Partial<Record<string, ComponentType<{ widget: any }>>> = {};

export function Widget({ widget }: { widget: AnyWidget }) {
  const Component = REGISTRY[widget.kind];
  if (!Component) {
    return <NotKnown missing="This part of the trip can't be shown" />;
  }
  return <Component widget={widget} />;
}
