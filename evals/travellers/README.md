# Scripted travellers

A scripted traveller plays the traveller in one evaluation trip ([cases](../../docs/evaluations/cases.md)). It answers the brief questions, picks a place, and approves or rejects the booking, so a trip can run the same way every time.

One JSON file per trip. (JSON, not YAML: PyYAML is only a development package in the backend, and the runner reads these files with the standard library.) The runner loads each file into `ScriptedTraveller` (`backend/src/app/evals/travellers.py`) and rejects unknown or missing fields.

| Field | Type | Meaning |
|---|---|---|
| `description` | text, optional | What the trip tests |
| `answers` | object of text | The traveller's answer to each brief question, keyed by the brief field (departure airport, when, length, people, budget, feel). At least one |
| `place_to_pick` | text | The place the traveller picks from the comparison |
| `approve` | true or false | Whether the traveller approves the booking at the approval step (`false` tests that nothing is booked) |

The people in these files are invented. Never put a real person's details here.
