// The notice for a visitor who has reached the limit per visitor or the cost cap. The words are the
// approved board's (docs/design/boards/screens/limit-reached.html). It is shown in the gallery only
// for now: the limits arrive in build step 7, and they wire it into `/` and `/trip/{trip_id}`.
export function LimitReached() {
  return (
    <section
      role="status"
      aria-labelledby="limit-title"
      className="bg-bg-tertiary border-border-primary flex flex-col gap-2 rounded-md border p-4"
    >
      <h3 id="limit-title" className="font-display text-lg font-semibold">
        You have reached the limit for planning
      </h3>
      <p className="text-sm">
        Layover limits how much each visitor can plan. You can plan again when the limit resets,
        later on.
      </p>
      <p className="text-sm">Your trip is still here. You can read it and share it.</p>
    </section>
  );
}
