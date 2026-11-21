"""Export the contract as JSON Schema files in the repository's `schemas/` folder.

    python -m app.contract.export            # write the files
    python -m app.contract.export --check    # exit 1, naming the files that differ or are missing

The website and other clients read these files, so they must always match the models.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, get_args

from pydantic import BaseModel

from app.contract.trip import Trip
from app.contract.widgets import WIDGET_KINDS, Widget


def default_out_dir() -> Path:
    """The repository's `schemas/` folder, found from this file, not the working directory."""
    return Path(__file__).resolve().parents[4] / "schemas"


def _widget_models() -> dict[str, type[BaseModel]]:
    union = get_args(Widget)[0]
    models = {
        get_args(model.model_fields["kind"].annotation)[0]: model for model in get_args(union)
    }
    if set(models) != set(WIDGET_KINDS):
        raise RuntimeError("the Widget union and WIDGET_KINDS disagree")
    return models


def _render(schema: dict[str, Any]) -> str:
    return json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def expected_files() -> dict[str, str]:
    """Every exported file: its path under the output folder, and its exact text."""
    files = {"trip.schema.json": _render(Trip.model_json_schema())}
    models = _widget_models()
    for kind in WIDGET_KINDS:
        files[f"widgets/{kind}.schema.json"] = _render(models[kind].model_json_schema())
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="compare, write nothing")
    parser.add_argument("--out", type=Path, default=default_out_dir(), help="output folder")
    args = parser.parse_args(argv)

    files = expected_files()
    if args.check:
        stale = [
            name
            for name, text in files.items()
            if not (args.out / name).is_file() or (args.out / name).read_text() != text
        ]
        for name in stale:
            print(name)
        if stale:
            print("Run `make export-schemas` and commit the result.", file=sys.stderr)
        return 1 if stale else 0

    for name, text in files.items():
        path = args.out / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    print(f"wrote {len(files)} files to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
