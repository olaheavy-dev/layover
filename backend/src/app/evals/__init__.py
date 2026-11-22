"""The evaluation runner: reads docs/evaluations/cases.md and runs each case's check.

Step 1 has no model calls, so only the schema part of the WIDGET cases runs. Every other case
reports `NOT RUN (needs step N)`, never `PASS`.
"""
