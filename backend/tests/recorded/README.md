# Recorded responses

The merge check (`make check`, CI) never calls a real outside service. It reads the recordings in
this folder instead. A test that does call a real service (Travelpayouts, Duffel, Open-Meteo,
exchange rates, FCDO) is marked `live` and is left out of the merge check.

The `sample/example.json` file is only a sample. It shows the format and is not real provider data.

## Format

One JSON file per exchange, at `tests/recorded/<provider>/<name>.json`:

| Field | Meaning |
| --- | --- |
| `provider` | The provider's name, the same as its folder |
| `captured_at` | The date the response was captured (`YYYY-MM-DD`) |
| `source` | The URL of the provider's API or documentation |
| `request` | What was asked (method, path, parameters) |
| `response` | What came back |

Load one with `load_recording(provider, name)` from `tests/recorded_check.py`. It fails if the
date or source is missing.

## Rules

- A recording never holds a key, a token or personal data. `test_no_secrets_in_recordings` fails
  on a key named `token`, `api_key`, `authorization`, `x-access-token` or `password` (any case, at
  any depth), on a value containing `duffel_test_` or `duffel_live_`, and on an email address.
  Remove or replace the value before committing.
- Refresh a recording by running the `live` test that wrote it. The run rewrites the file and its
  `captured_at`. Do this when the provider's API version changes or a `live` run shows its response
  has changed, in a pull request of its own.
