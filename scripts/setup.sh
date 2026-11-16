#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.elan/bin:$PATH"
command -v uv >/dev/null || { echo 'Install uv: https://docs.astral.sh/uv/' >&2; exit 1; }
command -v bwrap >/dev/null || { echo 'Install bubblewrap (Ubuntu: sudo apt install bubblewrap).' >&2; exit 1; }
if ! command -v elan >/dev/null; then
  installer=$(mktemp)
  curl -fsSL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o "$installer"
  sh "$installer" -y --no-modify-path --default-toolchain none
  rm "$installer"
fi
elan toolchain install "$(cat lean-toolchain)"
uv sync --locked
lake build
uv run pytest
