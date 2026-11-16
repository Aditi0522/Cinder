"""Explicit output contracts avoid silently accepting a changed theorem."""

import re


def extract_proof(raw_output: str, output_format: str) -> str:
    if output_format == "proof":
        proof = raw_output.strip()
    elif output_format == "markdown":
        blocks = re.findall(r"```(?:lean4?|Lean4?)\s*\n(.*?)```", raw_output, re.DOTALL)
        if len(blocks) != 1:
            raise ValueError("Expected exactly one fenced Lean proof block")
        proof = blocks[0].strip()
    else:
        raise ValueError(f"Unsupported output_format: {output_format}")
    if not proof:
        raise ValueError("Empty proof")
    return proof
