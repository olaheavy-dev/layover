import type { ReactNode } from "react";

// Buttons and links shared by the widgets. They are plain controls over Layover's tokens.
// The actions are not wired to the backend yet (the chat and the trip store come in later steps).
const BASE =
  "inline-flex min-h-11 items-center justify-center gap-1.5 text-sm font-medium focus-visible:outline-2";

const VARIANTS = {
  primary:
    "bg-accent-primary text-text-on-accent hover:bg-accent-primary-hover active:bg-accent-primary-active rounded-md px-4",
  secondary: "border-border-control text-text-primary rounded-md border px-4",
  link: "text-text-link px-1 underline",
} as const;

export function ActionButton({
  variant,
  label,
  icon,
  onClick,
  iconOnlyOnPhone = false,
  children,
}: {
  variant: keyof typeof VARIANTS;
  label?: string;
  icon?: ReactNode;
  onClick?: () => void;
  // Below `sm` only the icon shows, in a 44 px square; the words stay as the accessible name.
  iconOnlyOnPhone?: boolean;
  children: ReactNode;
}) {
  return (
    <button
      type="button"
      className={`${BASE} ${iconOnlyOnPhone ? `min-w-11 ${VARIANTS[variant].replace("px-4", "px-0 sm:px-4")}` : VARIANTS[variant]}`}
      aria-label={label}
      onClick={onClick}
    >
      {icon}
      {iconOnlyOnPhone ? (
        <span className="sr-only whitespace-nowrap sm:not-sr-only">{children}</span>
      ) : (
        children
      )}
    </button>
  );
}

export function ActionLink({
  href,
  icon,
  children,
}: {
  href: string;
  icon?: ReactNode;
  children: ReactNode;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="text-text-link inline-flex min-h-11 items-center gap-1.5 text-sm underline"
    >
      {children}
      {icon}
    </a>
  );
}

export const AVIASALES_URL = "https://www.aviasales.com/";

export function Actions({ children }: { children: ReactNode }) {
  return <div className="flex flex-wrap items-center gap-2">{children}</div>;
}

export function Chips({ label, children }: { label: string; children: ReactNode }) {
  return (
    <ul className="flex flex-wrap gap-2" aria-label={label}>
      {children}
    </ul>
  );
}

export const CHIP =
  "bg-bg-tertiary text-text-primary border-border-primary inline-flex min-h-9 items-center rounded-full border px-3 text-sm";

export function Skeleton({ className }: { className: string }) {
  return (
    <div
      className={`bg-bg-tertiary animate-pulse rounded-sm motion-reduce:animate-none ${className}`}
      aria-hidden="true"
    />
  );
}
