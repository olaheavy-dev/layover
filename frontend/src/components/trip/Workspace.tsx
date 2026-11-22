"use client";

import { useState } from "react";

import { ChatColumn } from "@/components/layout/ChatColumn";
import { PhoneTabs, type PhoneView } from "@/components/layout/PhoneTabs";
import { TripStrip } from "@/components/layout/TripStrip";

// The two-column workspace: the chat on the left and the canvas on the right from 1024 px, each
// scrolling on its own. Below that, the Chat and Trip tabs show one at a time. The page gives the
// top bar and the canvas (both made on the server); this holds only which tab is open. `trip` is
// set once a trip exists: it puts the trip strip above the message box on the Chat tab.
export function Workspace({
  top,
  canvas,
  trip,
  welcome = false,
}: {
  top: React.ReactNode;
  canvas: React.ReactNode;
  trip?: { name: string; factsReady: number };
  // On the welcome screen the welcome question is the page's h1. On a trip, the top bar owns it.
  welcome?: boolean;
}) {
  const [view, setView] = useState<PhoneView>("chat");
  return (
    <div className="relative flex h-dvh flex-col overflow-hidden">
      {top}
      <main className="flex min-h-0 flex-1 flex-col">
        <PhoneTabs view={view} onViewChange={setView} />
        <div className="flex min-h-0 flex-1 flex-col lg:grid lg:grid-cols-[minmax(22rem,2fr)_3fr] lg:grid-rows-[minmax(0,1fr)]">
          <div
            id="panel-chat"
            role="tabpanel"
            aria-labelledby="tab-chat"
            className={`${view === "chat" ? "flex" : "hidden"} border-border-primary min-h-0 flex-1 flex-col lg:flex lg:border-r`}
          >
            <ChatColumn
              headingAs={welcome ? "h1" : "h2"}
              strip={
                trip ? (
                  <TripStrip
                    name={trip.name}
                    factsReady={trip.factsReady}
                    onViewTrip={() => setView("trip")}
                  />
                ) : undefined
              }
            />
          </div>
          <div
            id="panel-trip"
            role="tabpanel"
            aria-labelledby="tab-trip"
            className={`${view === "trip" ? "flex" : "hidden"} min-h-0 flex-1 flex-col lg:flex`}
          >
            {canvas}
          </div>
        </div>
      </main>
    </div>
  );
}
