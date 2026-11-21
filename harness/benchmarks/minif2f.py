"""miniF2F loader: pinned upstream + audit ledger -> Cinder Problem records + manifest.

Run from the repo root:
    python -m harness.benchmarks.minif2f --environment-id <id from configs/verifier.toml>

Outputs (benchmarks/minif2f/): problems.valid.jsonl, problems.test.jsonl,
problems_excluded.jsonl (carries an extra field, so Problem(**record) rejects it
and the CLI cannot evaluate it), manifest.json. Output is deterministic.
The upstream `maxHeartbeats 0` is dropped from the preamble: the verifier config owns the budget.
"""
import argparse
import hashlib
import json
import subprocess
from dataclasses import asdict
from pathlib import Path

from harness.schema import Problem

ROOT = Path(__file__).resolve().parents[2]
MF = ROOT / "benchmarks" / "minif2f"
BENCH = "minif2f-lean4"
EXPECTED = {"valid": 244, "test": 244}
OPEN, CLOSE = "([{⟨", ")]}⟩"


def file_sha(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_jsonl(path) -> list[dict]:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def write_jsonl(path, rows) -> None:
    Path(path).write_text(
        "".join(json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n" for r in rows),
        encoding="utf-8",
        newline="\n",
    )


def _git(upstream, *args) -> str:
    return subprocess.check_output(["git", "-C", str(upstream), *args], text=True).strip()


def verify_pins(mf: Path = MF) -> dict:
    """Refuse to load unless upstream, extracted data and derived files match pins.json."""
    pins = json.loads((mf / "pins.json").read_text(encoding="utf-8"))
    up = mf / "upstream"
    src = pins["source"]
    if _git(up, "rev-parse", "HEAD") != src["commit"]:
        raise ValueError("upstream commit differs from pins.json")
    if _git(up, "rev-parse", "HEAD^{tree}") != src["tree"]:
        raise ValueError("upstream tree differs from pins.json")
    if _git(up, "status", "--porcelain", "--untracked-files=no"):
        raise ValueError("upstream checkout is modified")
    for rel, digest in pins.get("files", {}).items():
        if file_sha(up / rel) != digest:
            raise ValueError(f"hash mismatch: upstream/{rel}")
    derived = pins.get("derived", {})
    if "extracted.jsonl" not in derived:
        raise ValueError("pins.json has no derived hash for extracted.jsonl (rerun utils/make_pins.py)")
    for rel, digest in derived.items():
        if file_sha(mf / rel) != digest:
            raise ValueError(f"derived file changed since pinning: {rel}")
    for row in read_jsonl(mf / "extracted.jsonl"):
        if file_sha(up / row["source_path"]) != row["source_sha256"]:
            raise ValueError(f"{row['name']}: source differs from extracted.jsonl")
    return pins


def split_declaration(decl: str, name: str) -> tuple[str, str]:
    """Split `theorem NAME <binders> : <goal>` at the first top-level colon.

    Binders must be bracket groups only; the split must round-trip exactly.
    """
    prefix = f"theorem {name}"
    if not decl.startswith(prefix):
        raise ValueError(f"{name}: declaration does not start with its theorem name")
    rest = decl[len(prefix):]
    depth = 0
    for i, ch in enumerate(rest):
        if ch in OPEN:
            depth += 1
        elif ch in CLOSE:
            depth -= 1
            if depth < 0:
                raise ValueError(f"{name}: unbalanced brackets")
        elif depth == 0 and ch == ":":
            binders, goal = rest[:i].strip(), rest[i + 1:].strip()
            break
        elif depth == 0 and not ch.isspace():
            raise ValueError(f"{name}: unbracketed text before the goal separator")
    else:
        raise ValueError(f"{name}: no goal separator found")
    if not goal:
        raise ValueError(f"{name}: empty goal")
    if "".join(f"theorem {name} {binders} : {goal}".split()) != "".join(decl.split()):
        raise ValueError(f"{name}: split does not round-trip")
    return binders, goal


def preamble_from_header(header: str) -> str:
    keep = []
    for line in header.splitlines():
        s = line.strip()
        if not s or s.startswith("import ") or s.startswith("set_option maxHeartbeats"):
            continue
        if not s.startswith("open "):
            raise ValueError(f"unexpected header line: {s}")
        keep.append(s)
    return "\n".join(keep) + "\n"


def to_problem(row: dict, environment_id: str, commit: str, preamble: str,
               imports: tuple = ("Mathlib",)) -> Problem:
    binders, goal = split_declaration(row["declaration"], row["name"])
    return Problem(
        problem_id=f"minif2f.{row['name']}",
        statement=goal,
        environment_id=environment_id,
        imports=tuple(imports),
        preamble=preamble,
        binders=binders,
        metadata={
            "benchmark": BENCH,
            "benchmark_commit": commit,
            "split": row["split"],
            "upstream_name": row["name"],
            "source_path": row["source_path"],
            "theorem_line": row["theorem_line"],
            "source_sha256": row["source_sha256"],
            "header_sha256": row["header_sha256"],
            "statement_sha256": row["statement_sha256"],
        },
    )


def read_ledger(mf: Path, names: set, allow_pending: bool = False) -> dict:
    """Return {name: reason} for decision == exclude. Pending reviews block the build."""
    path = mf / "exclusions.jsonl"
    excluded, seen = {}, set()
    for r in (read_jsonl(path) if path.exists() else []):
        pid, decision = r["problem_id"], r["decision"]
        if pid not in names:
            raise ValueError(f"ledger names an unknown problem: {pid}")
        if pid in seen:
            raise ValueError(f"duplicate ledger row: {pid}")
        seen.add(pid)
        if decision == "exclude":
            if len(set(r.get("reviewers", []))) < 2 or not r.get("notes"):
                raise ValueError(f"{pid}: exclusion needs two reviewers and a reason in notes")
            excluded[pid] = r["notes"]
        elif decision == "pending_review":
            if not allow_pending:
                raise ValueError(f"{pid}: review pending")
        elif decision != "keep":
            raise ValueError(f"{pid}: unknown decision {decision!r}")
    return excluded


def build(environment_id: str, mf: Path = MF, verify: bool = True,
          allow_pending: bool = False, expected: dict = EXPECTED) -> dict:
    pins = verify_pins(mf) if verify else {"source": {"commit": "unverified", "tree": "unverified"}}
    rows = read_jsonl(mf / "extracted.jsonl")
    names = [r["name"] for r in rows]
    if len(set(names)) != len(names):
        raise ValueError("duplicate theorem names")
    counts = {s: sum(r["split"] == s for r in rows) for s in expected}
    if counts != expected or sum(counts.values()) != len(rows):
        raise ValueError(f"split counts {counts} != {expected}")
    headers = {r["header"] for r in rows}
    if len(headers) != 1:
        raise ValueError("expected one shared header")
    preamble = preamble_from_header(headers.pop())
    excluded = read_ledger(mf, set(names), allow_pending)
    commit = pins["source"]["commit"]

    problems = {s: [] for s in expected}
    included = {s: [] for s in expected}
    hashes, dropped = {}, []
    for r in sorted(rows, key=lambda r: (r["split"], r["name"])):
        p = to_problem(r, environment_id, commit, preamble)
        if r["name"] in excluded:
            dropped.append({**asdict(p), "exclusion_reason": excluded[r["name"]]})
            continue
        problems[r["split"]].append(asdict(p))
        included[r["split"]].append(p.problem_id)
        hashes[p.problem_id] = p.problem_hash
    for s in expected:
        write_jsonl(mf / f"problems.{s}.jsonl", problems[s])
    write_jsonl(mf / "problems_excluded.jsonl", dropped)

    ann_path = mf / "annotations.jsonl"
    annotations = {
        f"minif2f.{a['problem_id']}": {k: a.get(k) for k in ("coverage", "final_status", "transform", "flags")}
        for a in (read_jsonl(ann_path) if ann_path.exists() else [])
    }
    manifest = {
        "schema_version": 1,
        "benchmark": BENCH,
        "source": {"commit": commit, "tree": pins["source"]["tree"]},
        "environment_id": environment_id,
        "imports": ["Mathlib"],
        "preamble": preamble,
        "inputs": {n: file_sha(mf / n) for n in ("pins.json", "extracted.jsonl", "exclusions.jsonl", "annotations.jsonl")
                   if (mf / n).exists()},
        "files": {n: file_sha(mf / n) for n in [f"problems.{s}.jsonl" for s in expected] + ["problems_excluded.jsonl"]},
        "counts": {s: {"included": len(included[s]), "excluded": counts[s] - len(included[s])} for s in expected},
        "included": included,
        "excluded": {f"minif2f.{n}": why for n, why in sorted(excluded.items())},
        "problem_hashes": hashes,
        "annotations": annotations,
    }
    (mf / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                                      encoding="utf-8", newline="\n")
    return manifest


def check_problems(manifest_path, problems, allow_test: bool = False) -> None:
    """Evaluation guard: only manifest-included, unmodified problems; test split needs a flag."""
    m = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    included = {pid for ids in m["included"].values() for pid in ids}
    test_ids = set(m["included"].get("test", []))
    for p in problems:
        if p.problem_id in m["excluded"]:
            raise ValueError(f"{p.problem_id} is excluded from the benchmark")
        if p.problem_id not in included:
            raise ValueError(f"{p.problem_id} is not in the benchmark manifest")
        if p.problem_id in test_ids and not allow_test:
            raise ValueError("test split requires --allow-test")
        if p.problem_hash != m["problem_hashes"][p.problem_id]:
            raise ValueError(f"{p.problem_id} differs from the manifest")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--environment-id", required=True)
    ap.add_argument("--allow-pending", action="store_true", help="draft builds only")
    a = ap.parse_args()
    man = build(a.environment_id, allow_pending=a.allow_pending)
    print(json.dumps(man["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
