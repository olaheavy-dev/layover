"use client";

import { Send } from "lucide-react";
import { useId, useState } from "react";

// One example for each main intent; one is for a traveller who does not know where to go.
const EXAMPLE_PROMPTS = [
  "Somewhere warm in May, not sure where",
  "Do I need a visa for Turkey?",
  "Three days in Porto",
  "Cheapest flights from Bristol in March",
];

type Message = { from: "traveller" | "layover"; text: string };

// The chat. It makes no network call: sending shows that the chat isn't connected yet. The real
// chat arrives in a later build step. `strip` is the phone's trip strip, above the message box.
export function ChatColumn({
  strip,
  headingAs: Heading = "h2",
}: {
  strip?: React.ReactNode;
  // The welcome question is the page's h1 on the welcome screen. The page picks the level.
  headingAs?: "h1" | "h2";
}) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [draft, setDraft] = useState("");
  const promptsId = useId();

  function send(text: string) {
    const trimmed = text.trim();
    if (!trimmed) return;
    setMessages((previous) => [
      ...previous,
      { from: "traveller", text: trimmed },
      { from: "layover", text: "The chat isn't connected yet" },
    ]);
    setDraft("");
  }

  return (
    <section aria-label="Chat" className="bg-bg-secondary flex min-h-0 flex-1 flex-col">
      {/* Focusable, so the keyboard can scroll the chat once the prompts scroll away. */}
      <div
        role="region"
        aria-label="Chat messages and examples"
        tabIndex={0}
        className="flex flex-1 flex-col gap-3 overflow-y-auto p-4"
      >
        <Heading className="font-display text-3xl font-semibold">Where to next?</Heading>
        <p className="text-text-secondary text-base">
          Tell me about the trip you have in mind, in your own words.
        </p>
        <p id={promptsId} className="text-sm font-medium">
          Or try one of these
        </p>
        <div role="group" aria-labelledby={promptsId} className="flex flex-col items-start gap-2">
          {EXAMPLE_PROMPTS.map((prompt) => (
            <button
              key={prompt}
              type="button"
              onClick={() => send(prompt)}
              className="border-border-control rounded-md border px-3 py-2 text-left text-sm"
            >
              {prompt}
            </button>
          ))}
        </div>
        <div
          role="log"
          aria-live="polite"
          aria-label="Conversation with Layover"
          className="flex flex-col gap-3"
        >
          {messages.map((message, index) => (
            <p
              key={index}
              className={
                message.from === "traveller"
                  ? "bg-bg-tertiary self-end rounded-md px-3 py-2 text-sm"
                  : "text-text-secondary self-start text-sm"
              }
            >
              {message.text}
            </p>
          ))}
        </div>
      </div>
      {strip ? <div className="px-4 pb-2">{strip}</div> : null}
      <form
        className="border-border-primary flex gap-2 border-t p-4"
        onSubmit={(event) => {
          event.preventDefault();
          send(draft);
        }}
      >
        <label htmlFor="chat-message" className="sr-only">
          Message to Layover
        </label>
        <input
          id="chat-message"
          type="text"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Describe your trip"
          autoComplete="off"
          className="border-border-control min-h-11 flex-1 rounded-md border px-3 text-sm"
        />
        <button
          type="submit"
          aria-label="Send"
          className="bg-accent-primary text-text-on-accent hover:bg-accent-primary-hover active:bg-accent-primary-active inline-flex min-h-11 min-w-11 items-center justify-center rounded-md"
        >
          <Send className="size-4" aria-hidden="true" />
        </button>
      </form>
    </section>
  );
}
