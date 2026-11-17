#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$HOME/.elan/bin:$PATH"
command -v uv >/dev/null || { echo 'Install uv: https://docs.astral.sh/uv/' >&2; exit 1; }
command -v bwrap >/dev/null || { echo 'Install bubblewrap (Ubuntu: sudo apt install bubblewrap).' >&2; exit 1; }
for dependency in systemd-run prlimit; do
  command -v "$dependency" >/dev/null || { echo "Install required tool: $dependency" >&2; exit 1; }
done
environment=core
if [[ $# -gt 0 ]]; then
  [[ $# == 2 && $1 == --environment ]] || { echo 'Usage: setup.sh [--environment core|minif2f]' >&2; exit 1; }
  environment=$2
fi
case "$environment" in
  core) config=configs/verifier.toml ;;
  minif2f) config=configs/minif2f.toml ;;
  *) echo "Unknown environment: $environment" >&2; exit 1 ;;
esac
systemd-run --user --scope --quiet -p MemoryMax=128M -p TasksMax=16 /usr/bin/true
if ! command -v elan >/dev/null; then
  installer=$(mktemp)
  curl -fsSL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o "$installer"
  sh "$installer" -y --no-modify-path --default-toolchain none
  rm "$installer"
fi
uv sync --locked
uv run python scripts/setup_environment.py "$config"
if [[ $environment == core ]]; then
  uv run pytest -m 'not mathlib'
else
  uv run pytest
fi
