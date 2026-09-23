#!/usr/bin/env python3
"""Run purplepincher-supersite tests."""
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def test_canary():
    """FNV1a-64 canary preserved across the fleet."""
    expected = "0x24a555471370b18d"
    actual = ROOT.joinpath("canary.py").read_text()
    assert expected in actual, f"canary missing expected hash: {expected}"
    print("  ✓ test_canary")


def test_generator_proposes_fleet_entry():
    """Generator routes a release event to a fleet_entry proposal."""
    sys.path.insert(0, str(ROOT))
    from generator.agent import Generator, GHEvent

    gen = Generator()
    event = GHEvent(
        event_type="release",
        repo="SuperInstance/quilt-port",
        title="v0.1.0",
        url="https://example.com",
    )
    proposal = gen.route_event(event)
    assert proposal is not None, "expected a proposal"
    assert proposal.kind == "fleet_entry", f"expected fleet_entry, got {proposal.kind}"
    assert "quilt-port" in proposal.target_path
    print("  ✓ test_generator_proposes_fleet_entry")


def test_generator_proposes_changelog():
    """Generator routes a PR merge to a changelog entry."""
    sys.path.insert(0, str(ROOT))
    from generator.agent import Generator, GHEvent

    gen = Generator()
    event = GHEvent(
        event_type="pr_merged",
        repo="SuperInstance/cellforge",
        title="feat: foo",
        url="https://example.com",
    )
    proposal = gen.route_event(event)
    assert proposal is not None
    assert proposal.kind == "changelog_entry"
    print("  ✓ test_generator_proposes_changelog")


def test_generator_proposes_doctrine_update():
    """Generator routes a doctrine PR to a doctrine_clarification."""
    sys.path.insert(0, str(ROOT))
    from generator.agent import Generator, GHEvent

    gen = Generator()
    event = GHEvent(
        event_type="pr_merged",
        repo="SuperInstance/quilt-port",
        title="doctrine: refine the shell metaphor",
        url="https://example.com",
    )
    proposal = gen.route_event(event)
    assert proposal is not None
    assert proposal.kind == "doctrine_clarification"
    print("  ✓ test_generator_proposes_doctrine_update")


def test_adversary_truthfulness_check():
    """Adversary flags proposals without witnesses."""
    sys.path.insert(0, str(ROOT))
    from generator.agent import Generator, GHEvent, ContentProposal
    from adversary.critic import Adversary

    gen = Generator()
    event = GHEvent(
        event_type="release",
        repo="SuperInstance/quilt-port",
        title="v0.1.0",
        url="https://example.com",
        body="Some content",
    )
    proposal = gen.route_event(event)
    adv = Adversary()
    critique = adv.check_truthfulness(proposal)
    # Has witnesses, should pass
    assert critique.passed
    print("  ✓ test_adversary_truthfulness_check")


def test_adversary_kills_empty_proposal():
    """Adversary refuses a proposal that's empty or has no witnesses."""
    sys.path.insert(0, str(ROOT))
    from generator.agent import ContentProposal
    from adversary.critic import Adversary
    from dataclasses import dataclass

    # Build a bare-bones proposal that violates everything
    @dataclass
    class FakeEvent:
        event_type: str = "release"
        repo: str = "test"
        title: str = ""
        url: str = ""
        body: str = ""

    proposal = ContentProposal(
        proposal_id="x",
        target_path="x",
        title="x",
        body="",
        source_event=FakeEvent(),
        kind="fleet_entry",
        witnesses=[],
    )
    adv = Adversary()
    review = adv.review(proposal)
    assert review.verdict != "🟢 PROMOTE", f"Empty proposal should NOT be promoted: {review.verdict}"
    print(f"  ✓ test_adversary_kills_empty_proposal (verdict={review.verdict})")


def test_pipeline_runs_tick():
    """Pipeline tick produces a report with sane counts."""
    sys.path.insert(0, str(ROOT))
    from generator.agent import GHEvent
    from pipeline.orchestrate import run_tick

    events = [
        GHEvent(
            event_type="release",
            repo="SuperInstance/quilt-port",
            title="v0.1.0",
            url="https://example.com",
            body="x",
        ),
    ]
    report = run_tick(events)
    assert report.events_seen == 1
    assert report.proposals_made >= 1
    assert report.finished_at != ""
    print(f"  ✓ test_pipeline_runs_tick (promoted={report.proposals_promoted}, revise={report.proposals_revise}, killed={report.proposals_killed})")


def test_site_pages_exist():
    """All v0.1 pages are present."""
    pages = [
        "site/index.html",
        "site/doctrine/index.html",
        "site/fleet/index.html",
        "site/for-agents/index.html",
        "site/for-humans/index.html",
        "site/changelog/index.html",
        "site/pipeline/index.html",
        "site/style.css",
    ]
    for p in pages:
        f = ROOT / p
        assert f.exists(), f"missing: {p}"
        assert f.stat().st_size > 100, f"too small: {p}"
    print(f"  ✓ test_site_pages_exist ({len(pages)} pages)")


def test_pages_have_witnesses():
    """Every page includes the FNV1a canary as a witness."""
    pages = list((ROOT / "site").rglob("*.html"))
    for p in pages:
        text = p.read_text()
        assert "0x24a555471370b18d" in text, f"canary missing in {p}"
    print(f"  ✓ test_pages_have_witnesses ({len(pages)} pages)")


TESTS = [
    test_canary,
    test_generator_proposes_fleet_entry,
    test_generator_proposes_changelog,
    test_generator_proposes_doctrine_update,
    test_adversary_truthfulness_check,
    test_adversary_kills_empty_proposal,
    test_pipeline_runs_tick,
    test_site_pages_exist,
    test_pages_have_witnesses,
]


if __name__ == "__main__":
    import traceback
    passed = 0
    failed = 0
    for t in TESTS:
        try:
            t()
            passed += 1
        except Exception as e:
            print(f"  ✗ {t.__name__}: {type(e).__name__}: {e}")
            traceback.print_exc()
            failed += 1
    print(f"\n{passed}/{len(TESTS)} tests passed ({failed} failed)")
    sys.exit(0 if failed == 0 else 1)
