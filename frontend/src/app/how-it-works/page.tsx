import { ExternalLink } from "lucide-react";
import type { Metadata } from "next";

import { TopBar } from "@/components/layout/TopBar";

import { RULES, SOURCES, SUPERVISOR, TEAM_STEPS } from "./content";

export const metadata: Metadata = { title: "How Layover works" };

const REPO = "https://github.com/olaheavy-dev/layover";
const DATA_SOURCES_LIST = `${REPO}/blob/main/docs/references/data-sources.md`;

const PARTS = [
  { id: "what", label: "What it does" },
  { id: "team", label: "Agent team" },
  { id: "rules", label: "Rules" },
  { id: "sources", label: "Data sources" },
  { id: "evaluation", label: "Evaluation" },
  { id: "code", label: "Code" },
];

function Part({ id, title, children }: { id: string; title: string; children: React.ReactNode }) {
  return (
    <section id={id} aria-labelledby={`${id}-title`} className="flex scroll-mt-16 flex-col gap-3">
      <h2 id={`${id}-title`} className="font-display text-2xl font-semibold">
        {title}
      </h2>
      {children}
    </section>
  );
}

const LINK = "text-text-link underline";

// "How Layover works": one page for every visitor and for recruiters. The words are the approved
// board's (docs/design/boards/screens/how-it-works.html). No trip has been scored yet (the build-1 report
// has schema checks only), so part 5 says so and shows no result (AGENTS.md, "Evaluations at each gate").
export default function HowItWorks() {
  return (
    <div className="flex min-h-dvh flex-col">
      <TopBar action="plan-a-trip" hideHowItWorks />
      <nav
        aria-label="Sections of this page"
        className="bg-bg-primary border-border-primary sticky top-0 z-10 shrink-0 overflow-x-auto border-b"
      >
        <ul className="mx-auto flex max-w-3xl gap-1 px-4">
          {PARTS.map((part) => (
            <li key={part.id} className="shrink-0">
              <a
                href={`#${part.id}`}
                className="text-text-link inline-flex min-h-11 items-center px-2 text-sm"
              >
                {part.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col gap-8 px-4 py-6">
        <header className="flex flex-col gap-3">
          <h1 className="font-display text-3xl font-semibold">How Layover works</h1>
          <p className="text-base">
            Layover is an AI travel planner for people in the UK. Tell it about a trip in your own
            words, and it compares places and plans your days.
          </p>
          <p className="text-base">
            Every figure shows its source and how old it is. Booking is a sandbox demo: no real
            booking or payment.
          </p>
        </header>

        <Part id="what" title="1. What Layover does">
          <p>
            You describe a trip, for example “somewhere warm in May, about £800 for two”. Layover
            asks for what is missing and shows your brief for you to confirm. It then compares three
            places side by side, and plans the days for the place you choose.
          </p>
          <p>
            The figures come from real travel sources. Each one is labelled Live, Cached with its
            age, Fallback or Unavailable, so you can judge it yourself.
          </p>
        </Part>

        <Part id="team" title="2. The agent team">
          <p>
            Layover uses a team of agents. An agent is a program that uses an AI model for one
            narrow job. A supervisor passes work between them and keeps the shared trip.
          </p>
          <figure aria-labelledby="team-cap" className="flex flex-col gap-3">
            <div className="bg-bg-tertiary border-border-primary flex flex-col rounded-md border p-3">
              <strong>{SUPERVISOR.name}</strong>
              <span className="text-text-secondary text-sm">{SUPERVISOR.text}</span>
            </div>
            <ol className="flex flex-col gap-3">
              {TEAM_STEPS.map((step, index) => (
                <li
                  key={step.name}
                  className="bg-bg-secondary border-border-primary flex gap-3 rounded-md border p-3"
                >
                  <span
                    aria-hidden="true"
                    className="bg-accent-primary text-text-on-accent grid size-7 shrink-0 place-items-center rounded-full text-sm font-semibold"
                  >
                    {index + 1}
                  </span>
                  <div className="flex flex-col gap-1">
                    <h3 className="font-semibold">{step.name}</h3>
                    <p className="text-sm">{step.text}</p>
                  </div>
                </li>
              ))}
            </ol>
            <figcaption id="team-cap" className="text-text-secondary text-sm">
              Diagram: the supervisor passes work in order to the brief agent, the research agents
              (one for each place, at the same time), the itinerary agent and the booking steps. The
              same list is written out above.
            </figcaption>
          </figure>
        </Part>

        <Part id="rules" title="3. The rules Layover keeps">
          <p>
            Six rules apply to everything Layover shows. They were agreed on 19 Nov 2026 (decision
            0011).
          </p>
          <ol className="flex flex-col gap-3">
            {RULES.map((rule) => (
              <li
                key={rule.name}
                className="bg-bg-secondary border-border-primary flex flex-col gap-1 rounded-md border p-3"
              >
                <h3 className="font-semibold">{rule.name}</h3>
                <p className="text-sm">{rule.text}</p>
              </li>
            ))}
          </ol>
        </Part>

        <Part id="sources" title="4. Where the data comes from">
          <p>
            Layover uses these sources, under their own terms. The terms were checked on 19 Nov 2026
            and are kept in{" "}
            <a href={DATA_SOURCES_LIST} className={LINK}>
              the data sources list
            </a>
            .
          </p>
          <ul className="flex flex-col gap-3">
            {SOURCES.map((source) => (
              <li
                key={source.href}
                className="bg-bg-secondary border-border-primary flex flex-col gap-1 rounded-md border p-3"
              >
                <h3 className="font-semibold">
                  <a href={source.href} className={`${LINK} inline-flex items-center gap-1.5`}>
                    {source.name}
                    <ExternalLink className="size-4" aria-hidden="true" />
                  </a>
                </h3>
                <p className="text-sm">
                  <span className="font-medium">Gives</span> {source.gives}
                </p>
                <p className="text-sm">
                  <span className="font-medium">Terms</span> {source.terms}
                </p>
              </li>
            ))}
          </ul>
        </Part>

        <Part id="evaluation" title="5. How well it works">
          <p className="text-status-not-known text-sm font-medium italic">
            No evaluation results yet
          </p>
          <p>
            Layover has not been scored yet. When it has, this page will show the quality score with
            the number of trips in the test set. It will also show the team of agents against a
            single agent doing the same trips, on quality, speed and cost.
          </p>
        </Part>

        <Part id="code" title="6. Read the code">
          <p>Layover is a portfolio project, and its code and decisions are public.</p>
          <p>
            <a
              href={REPO}
              className="border-border-control text-text-primary inline-flex min-h-11 items-center gap-1.5 rounded-md border px-4 text-sm font-medium"
            >
              Layover on GitHub
              <ExternalLink className="size-4" aria-hidden="true" />
            </a>
          </p>
        </Part>
      </main>
    </div>
  );
}
