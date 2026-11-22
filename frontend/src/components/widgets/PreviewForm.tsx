"use client";

// A form that does nothing yet: the brief's budget editor arrives with the planner. A server
// component can't pass an event handler, so the handler lives here, in a client component.
export function PreviewForm({
  className,
  children,
}: {
  className?: string;
  children: React.ReactNode;
}) {
  return (
    <form className={className} onSubmit={(event) => event.preventDefault()}>
      {children}
    </form>
  );
}
