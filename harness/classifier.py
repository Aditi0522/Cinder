"""Failure labels are observations, not claims about a model's capability."""

import re


def repetition_ratio(text: str, n: int = 4) -> float:
    if n < 1:
        raise ValueError("n must be positive")
    tokens = text.split()
    grams = [tuple(tokens[i : i + n]) for i in range(max(0, len(tokens) - n + 1))]
    return 0.0 if not grams else 1 - len(set(grams)) / len(grams)


def classify(verdict: str, errors: list[dict], raw_output: str, truncated: bool) -> list[str]:
    if verdict == "infrastructure_error":
        return ["infrastructure_error"]
    labels = []
    if truncated:
        labels.append("truncated")
    if len(raw_output.split()) >= 32 and repetition_ratio(raw_output) >= 0.5:
        labels.append("repetition")
    if verdict == "pass":
        return labels
    if verdict == "candidate_crash":
        return labels + ["candidate_crash"]
    text = "\n".join(error["message"] for error in errors).lower()
    if verdict == "timeout":
        labels.append("timeout")
    elif verdict == "extraction_error":
        labels.append("no_code_block" if "fenced" in text else "malformed_output")
    elif re.search(r"\b(sorry|admit|sorryax)\b", text):
        labels.append("contains_sorry")
    elif "cinder_policy" in text or "cinder_axioms" in text or "cinder_signature" in text:
        labels.append("policy_violation")
    elif "unknown identifier" in text or "unknown constant" in text:
        labels.append("unknown_identifier")
    elif "cinder_parse" in text or "unexpected token" in text or "expected token" in text:
        labels.append("syntax_error")
    elif "type mismatch" in text:
        labels.append("type_mismatch")
    elif "tactic" in text or "unsolved goals" in text:
        labels.append("tactic_failed")
    else:
        labels.append("other")
    return labels
