import { CircleAlert, RefreshCw } from "lucide-react";

import type { WidgetState } from "./WidgetFrame";
import { ActionButton } from "./WidgetParts";

// The place widgets write their own error text (the board says what could not be checked), so the
// frame is given "filled" for an error and the body below. Every other state is the frame's own.
export function frameState(state: WidgetState): WidgetState {
  return state === "error" ? "filled" : state;
}

// "Unavailable" in words with an icon, what could not be checked, and Try again. The retry is not
// wired yet: the chat and the trip store come in later steps.
export function ErrorNote({ message, children }: { message: string; children?: React.ReactNode }) {
  return (
    <div className="flex flex-col items-start gap-2" role="alert">
      <p className="text-status-warning inline-flex items-center gap-1.5 text-sm font-medium">
        <CircleAlert className="size-4" aria-hidden="true" />
        <span>Unavailable</span>
      </p>
      <p className="text-sm">{message}</p>
      {children}
      <ActionButton variant="secondary" icon={<RefreshCw className="size-4" aria-hidden="true" />}>
        Try again
      </ActionButton>
    </div>
  );
}
