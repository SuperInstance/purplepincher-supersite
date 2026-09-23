"""Demo: run the GAN pipeline with sample GH events.

Run this to see the Generator → Adversary → Orchestrator flow in action.

    python3 examples/run_pipeline_demo.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from generator.agent import GHEvent
from pipeline.orchestrate import run_tick
import json


def main():
    """Simulate a tick with three sample GH events."""
    events = [
        GHEvent(
            event_type="release",
            repo="SuperInstance/quilt-port",
            title="quilt-port v0.1.0",
            url="https://github.com/SuperInstance/quilt-port/releases/tag/v0.1.0",
            body="Initial scaffold. The user's port to their quilts.",
            actor="Mavis",
        ),
        GHEvent(
            event_type="pr_merged",
            repo="SuperInstance/cellforge",
            title="feat: causal-consistency verdict on rewind (v0.4.1)",
            url="https://github.com/SuperInstance/cellforge/pull/13",
            body="Dispatcher.rewind_to() returns a verdict dict.",
            actor="Mavis",
        ),
        GHEvent(
            event_type="pr_merged",
            repo="SuperInstance/quilt-port",
            title="doctrine: Hull Doctrine canonized (HULL_DOCTRINE.md)",
            url="https://github.com/SuperInstance/quilt-port/pull/1",
            body="The hermit-crab ontology of agents, models, code, and data.",
            actor="Casey",
        ),
    ]

    report = run_tick(events)

    print("=" * 70)
    print("Pipeline tick report")
    print("=" * 70)
    print(json.dumps(report.to_dict(), indent=2))
    print()
    print("=" * 70)
    print("Staged PRs (🟢 PROMOTE only)")
    print("=" * 70)
    for pr in report.staged_prs:
        print(f"\n[{pr['pr_title']}]")
        print(f"  branch: {pr['branch']}")
        print(f"  files: {[f['path'] for f in pr['files']]}")
        print(f"  labels: {pr['labels']}")


if __name__ == "__main__":
    main()
