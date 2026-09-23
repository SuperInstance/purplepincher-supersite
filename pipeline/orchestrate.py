"""Pipeline orchestrator — runs the GAN loop end-to-end.

This is the orchestrator that the GH Actions cron (Phase 3) will invoke.

For each tick:
1. Watch GH events
2. Route events → Generator proposals
3. Adversary reviews each proposal
4. Stage PRs for 🟢 PROMOTE
5. Notify Casey of 🟡 REVISE and 🔴 NOT VIABLE

Doctrine: receipted-everything. Every tick emits a witness.
"""
from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import List

# Make the generator/adversary packages importable when run as a script
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generator.agent import Generator, GHEvent, ContentProposal
from adversary.critic import Adversary, AdversaryReview, VERDICT_PROMOTE


@dataclass
class TickReport:
    """The witness of one pipeline tick."""
    tick_id: str
    started_at: str
    finished_at: str = ""
    events_seen: int = 0
    proposals_made: int = 0
    proposals_promoted: int = 0
    proposals_revise: int = 0
    proposals_killed: int = 0
    staged_prs: List[dict] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "tick_id": self.tick_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "events_seen": self.events_seen,
            "proposals_made": self.proposals_made,
            "proposals_promoted": self.proposals_promoted,
            "proposals_revise": self.proposals_revise,
            "proposals_killed": self.proposals_killed,
            "staged_prs": self.staged_prs,
            "notes": self.notes,
        }


def run_tick(events: List[GHEvent], orgs: List[str] = None) -> TickReport:
    """Run one pipeline tick."""
    tick_id = f"tick-{int(datetime.now(timezone.utc).timestamp())}"
    report = TickReport(
        tick_id=tick_id,
        started_at=datetime.now(timezone.utc).isoformat() + "Z",
    )

    report.events_seen = len(events)
    if not events:
        report.notes.append("No events to process. Pipeline is quiet.")
        report.finished_at = datetime.now(timezone.utc).isoformat() + "Z"
        return report

    gen = Generator(orgs=orgs)
    adv = Adversary()

    for event in events:
        proposal = gen.route_event(event)
        if not proposal:
            report.notes.append(f"Skipped event {event.event_type} (no proposal route).")
            continue
        report.proposals_made += 1

        review = adv.review(proposal)
        if review.verdict == VERDICT_PROMOTE:
            report.proposals_promoted += 1
            staged = gen.stage_pr(proposal)
            report.staged_prs.append(staged)
        elif "REVISE" in review.verdict:
            report.proposals_revise += 1
        else:
            report.proposals_killed += 1

    report.finished_at = datetime.now(timezone.utc).isoformat() + "Z"
    return report


def main():
    """Demo tick."""
    # Sample events (in production: from GH watch)
    events = [
        GHEvent(
            event_type="release",
            repo="SuperInstance/quilt-port",
            title="quilt-port v0.1.0",
            url="https://github.com/SuperInstance/quilt-port/releases/tag/v0.1.0",
            body="Initial scaffold of quilt-port — the user's port to their quilts.",
        ),
        GHEvent(
            event_type="pr_merged",
            repo="SuperInstance/cellforge",
            title="feat: causal-consistency verdict on rewind (v0.4.1)",
            url="https://github.com/SuperInstance/cellforge/pull/13",
            body="Dispatcher.rewind_to() now returns a verdict dict.",
        ),
    ]
    report = run_tick(events)
    print(json.dumps(report.to_dict(), indent=2))


if __name__ == "__main__":
    main()
