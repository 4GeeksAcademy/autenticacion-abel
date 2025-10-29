#!/usr/bin/env bash
set -euo pipefail

REPO="4GeeksAcademy/autenticacion-abel"

usage() {
  cat <<EOF
Usage: $0 <command> [args]

Commands:
  list [branch]               List recent workflow runs (optional branch)
  rerun <run-id>             Re-run a specific workflow run
  dispatch <workflow> <ref>  Dispatch a workflow (path or name) on ref (branch)

Examples:
  $0 list feat/ci-docs-fix
  $0 rerun 18878613312
  $0 dispatch .github/workflows/tests.yml feat/ci-docs-fix

Note: requires GitHub CLI (gh) authenticated. See docs/gh_cli.md
EOF
}

cmd="$1" || { usage; exit 1; }
shift || true

case "$cmd" in
  list)
    branch=""
    if [ "$#" -ge 1 ]; then
      branch="$1"
    fi
    if [ -n "$branch" ]; then
      echo "Listing runs for $REPO on branch $branch..."
      gh run list --repo "$REPO" --branch "$branch" --limit 50
    else
      echo "Listing recent runs for $REPO..."
      gh run list --repo "$REPO" --limit 50
    fi
    ;;

  rerun)
    if [ $# -ne 1 ]; then
      echo "rerun requires a run id" >&2
      usage
      exit 2
    fi
    run_id="$1"
    echo "Re-running run $run_id..."
    gh run rerun "$run_id" --repo "$REPO"
    ;;

  dispatch)
    if [ $# -ne 2 ]; then
      echo "dispatch requires workflow and ref" >&2
      usage
      exit 2
    fi
    workflow="$1"
    ref="$2"
    echo "Dispatching workflow $workflow on ref $ref..."
    gh workflow run "$workflow" --repo "$REPO" --ref "$ref"
    ;;

  *)
    usage
    exit 2
    ;;

esac
