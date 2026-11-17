"""Read host-visible worker RSS, including children in nested PID namespaces."""

from pathlib import Path


def process_tree_rss(pid: int, *, include_root: bool = True) -> tuple[int, int]:
    """Return maximum-process and summed RSS in KiB at this sampling instant."""
    pending = [pid]
    seen = set()
    sizes = []
    while pending:
        current = pending.pop()
        if current in seen:
            continue
        seen.add(current)
        path = Path(f"/proc/{current}")
        try:
            if include_root or current != pid:
                for line in (path / "status").read_text().splitlines():
                    if line.startswith("VmRSS:"):
                        sizes.append(int(line.split()[1]))
                        break
            # Children may belong to a pool thread rather than the task leader.
            for children in (path / "task").glob("*/children"):
                pending.extend(int(child) for child in children.read_text().split())
        except (OSError, ValueError):
            continue
    return max(sizes, default=0), sum(sizes)
