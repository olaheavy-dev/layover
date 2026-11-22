"""The evaluation runner: reads docs/evaluations/cases.md and runs each case's check.

Step 1 has no model calls, so only the schema part of the WIDGET cases runs, and it reports
`SCHEMA PASS`. Every other case reports `NOT RUN (needs step N)`. Neither is a full `PASS`.
"""
