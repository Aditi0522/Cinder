#!/usr/bin/env python3
"""Convert pinned miniF2F extractions into atp-checkers JSONL input."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "benchmarks/minif2f/extracted.jsonl"


def load_records(path: Path) -> list[dict]:
    records = []
    seen = set()

    with path.open(encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            if not line.strip():
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{path}:{line_number}: invalid JSON: {exc}"
                ) from exc

            if not isinstance(record, dict):
                raise ValueError(f"{path}:{line_number}: expected JSON object")

            required = (
                "name",
                "header",
                "declaration",
                "split",
                "statement_sha256",
                "source_path",
                "source_sha256",
                "header_sha256",
                "theorem_line",
            )
            missing = [key for key in required if key not in record]
            if missing:
                raise ValueError(
                    f"{path}:{line_number}: missing fields: {missing}"
                )

            name = record["name"]
            if not isinstance(name, str) or not name.strip():
                raise ValueError(f"{path}:{line_number}: invalid theorem name")

            if name in seen:
                raise ValueError(f"{path}:{line_number}: duplicate theorem: {name}")
            seen.add(name)

            if not isinstance(record["header"], str) or not isinstance(
                record["declaration"], str
            ):
                raise ValueError(
                    f"{path}:{line_number}: header/declaration must be strings"
                )

            records.append(record)

    if not records:
        raise ValueError(f"No records found in {path}")

    return records


def convert(record: dict) -> dict:
    header = record["header"].rstrip()
    declaration = record["declaration"].rstrip()

    # The extracted declaration intentionally excludes the original proof.
    lean_code = f"{header}\n\n{declaration} := by\n  sorry\n"

    return {
        "id": record["name"],
        "lean_code": lean_code,
        "source": "minif2f-lean4",
        "split": record["split"],
        "statement_sha256": record["statement_sha256"],
        "source_path": record["source_path"],
        "source_sha256": record["source_sha256"],
        "header_sha256": record["header_sha256"],
        "theorem_line": record["theorem_line"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Extraction JSONL (default: {DEFAULT_INPUT})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output JSONL path",
    )
    parser.add_argument(
        "--names",
        nargs="+",
        help="Optional theorem names to include",
    )
    args = parser.parse_args()

    try:
        records = load_records(args.input)

        if args.names:
            requested = set(args.names)
            available = {record["name"] for record in records}
            missing = sorted(requested - available)
            if missing:
                raise ValueError(f"Requested theorem names not found: {missing}")

            records = [
                record for record in records if record["name"] in requested
            ]

        if not records:
            raise ValueError("No records selected")

        output = [convert(record) for record in records]

        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as f:
            for row in output:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

        print(f"Input records:  {len(load_records(args.input))}")
        print(f"Selected:       {len(output)}")
        print(f"Output:         {args.out}")
        print(f"Theorems:       {', '.join(row['id'] for row in output)}")
        return 0

    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
