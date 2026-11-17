"""Versioned records shared by local verification and future generation workers."""

import hashlib
import json
from dataclasses import asdict, dataclass, field


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Problem:
    problem_id: str
    statement: str
    environment_id: str
    imports: tuple[str, ...] = ()
    preamble: str = ""
    binders: str = ""
    metadata: dict = field(default_factory=dict)

    @property
    def problem_hash(self) -> str:
        return sha256(json.dumps(asdict(self), sort_keys=True, ensure_ascii=False))


@dataclass(frozen=True)
class Sample:
    problem_id: str
    sample_id: str
    model: str
    seed: int
    prompt_hash: str
    raw_output: str
    token_count: int | None = None
    truncated: bool = False
    output_format: str = "proof"
    metadata: dict = field(default_factory=dict)
    additional_fields: dict = field(default_factory=dict)

    @classmethod
    def from_record(cls, record: dict) -> "Sample":
        from dataclasses import fields

        known = {item.name for item in fields(cls)}
        if not isinstance(record.get("metadata", {}), dict):
            raise TypeError("Sample metadata must be a JSON object")
        additional = dict(record.get("additional_fields", {}))
        extras = {key: value for key, value in record.items() if key not in known}
        if additional.keys() & extras.keys():
            raise ValueError("Ambiguous duplicate fields in additional sample metadata")
        additional.update(extras)
        return cls(
            **{
                key: value
                for key, value in record.items()
                if key in known and key != "additional_fields"
            },
            additional_fields=additional,
        )


@dataclass
class VerificationResult:
    problem_id: str
    sample_id: str
    model: str
    seed: int
    prompt_hash: str
    raw_output: str
    token_count: int | None
    truncated: bool
    extracted_proof: str | None
    verdict: str
    errors: list[dict]
    wall_time_seconds: float
    lean_toolchain: str
    mathlib_commit: str | None
    environment_id: str
    problem_hash: str
    config_hash: str
    labels: list[str] = field(default_factory=list)
    axioms: list[str] = field(default_factory=list)
    schema_version: int = 2
    metadata: dict = field(default_factory=dict)
    peak_rss_kb: int | None = None
    additional_fields: dict = field(default_factory=dict)
    run_id: str | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False, sort_keys=True)
