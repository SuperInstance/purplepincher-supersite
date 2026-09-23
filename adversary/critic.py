"""Adversary Agent — critiques proposals.

The Adversary reads every proposal from the Generator and reviews it on
four axes:

1. Truthfulness — does it match the code/canon?
2. Clarity — would a zero-shot reader get it?
3. Witness-presence — does it leave a tree-ring?
4. GAN-loyalty — does it serve the doctrine, not advertise?

Mark proposals with verdicts:
- 🟢 PROMOTE (ready for human review)
- 🟡 REVISE (needs fixes — comments say what)
- 🔴 NOT VIABLE (misleading or doctrine-violating)

Doctrine (Sept 23, 2026):
- The Adversary is sacred. No proposal — from Casey, from agents, from anyone — escapes its scrutiny.
- A receipted refusal is more valuable than silent acceptance.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from generator.agent import ContentProposal


VERDICT_PROMOTE = "🟢 PROMOTE"
VERDICT_REVISE = "🟡 REVISE"
VERDICT_NOT_VIABLE = "🔴 NOT VIABLE"


@dataclass
class Critique:
    """A critique of one axis."""
    axis: str
    passed: bool
    comment: str


@dataclass
class AdversaryReview:
    """The full Adversary review of a proposal."""
    proposal_id: str
    verdict: str
    critiques: List[Critique]
    reviewed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat() + "Z")

    def to_dict(self):
        return {
            "proposal_id": self.proposal_id,
            "verdict": self.verdict,
            "critiques": [
                {"axis": c.axis, "passed": c.passed, "comment": c.comment}
                for c in self.critiques
            ],
            "reviewed_at": self.reviewed_at,
        }


class Adversary:
    """The GAN Adversary.

    Reviews proposals. Files review comments. Promotes, revises, or kills.
    """

    def check_truthfulness(self, proposal: ContentProposal) -> Critique:
        """Does the proposal match the code/canon?

        Heuristic v0.1: a proposal with witnesses is more likely truthful
        than one without. A proposal that names a `content_hash` or `FNV1a`
        is more likely truthful than one that doesn't.
        """
        witnesses_ok = len(proposal.witnesses) > 0
        has_canary = "0x24a555471370b18d" in proposal.body or "FNV1a" in proposal.body
        if witnesses_ok and has_canary:
            return Critique(
                axis="truthfulness",
                passed=True,
                comment=f"Has {len(proposal.witnesses)} witnesses and the FNV1a canary. Likely truthful.",
            )
        if witnesses_ok:
            return Critique(
                axis="truthfulness",
                passed=True,
                comment=f"Has {len(proposal.witnesses)} witnesses. Canary missing — request it be added.",
            )
        return Critique(
            axis="truthfulness",
            passed=False,
            comment="No witnesses cited. Cannot verify. Request witness citations before promote.",
        )

    def check_clarity(self, proposal: ContentProposal) -> Critique:
        """Would a zero-shot reader get it?

        Heuristic v0.1: a body < 50 chars is too terse; > 5000 chars is
        probably drifting. A title that explains what the page is about is good.
        """
        body_len = len(proposal.body)
        title_clear = len(proposal.title) > 8 and " " in proposal.title
        if body_len < 50:
            return Critique(
                axis="clarity",
                passed=False,
                comment=f"Body too short ({body_len} chars). Add substance — a zero-shot reader needs context.",
            )
        if body_len > 5000:
            return Critique(
                axis="clarity",
                passed=False,
                comment=f"Body too long ({body_len} chars). Likely drifting. Tighten or split.",
            )
        if not title_clear:
            return Critique(
                axis="clarity",
                passed=False,
                comment="Title is unclear. Use a noun phrase that names what's on the page.",
            )
        return Critique(
            axis="clarity",
            passed=True,
            comment=f"Body {body_len} chars, title clear. Likely readable.",
        )

    def check_witness_presence(self, proposal: ContentProposal) -> Critique:
        """Does it leave a tree-ring?

        Heuristic: every proposal should cite the source event AND the FNV1a
        canary. If not, the witness is broken.
        """
        has_source = any(
            ev.get("url") for ev in [proposal.source_event.__dict__]
        )
        body = proposal.body
        has_canary = "0x24a555471370b18d" in body
        has_doctrine = "doctrine" in body.lower() or "STITCH" in body or "WITNESS" in body
        if has_source and has_canary and has_doctrine:
            return Critique(
                axis="witness-presence",
                passed=True,
                comment="Source cited, canary present, doctrine mentioned. Tree-ring intact.",
            )
        missing = []
        if not has_source:
            missing.append("source URL")
        if not has_canary:
            missing.append("FNV1a canary")
        if not has_doctrine:
            missing.append("doctrine reference")
        return Critique(
            axis="witness-presence",
            passed=False,
            comment=f"Missing: {', '.join(missing)}. Add before promote.",
        )

    def check_gan_loyalty(self, proposal: ContentProposal) -> Critique:
        """Does it serve the doctrine, not advertise?

        Heuristic: a proposal that uses promo words ("amazing", "best", "must",
        "click here", "buy now") violates GAN loyalty.
        """
        body = proposal.body.lower()
        promo_markers = ["amazing", "best ever", "must-buy", "click here", "buy now", "incredible", "revolutionary"]
        violations = [m for m in promo_markers if m in body]
        if violations:
            return Critique(
                axis="gan-loyalty",
                passed=False,
                comment=f"Promo language detected: {', '.join(violations)}. The doctrine serves the crab, not the marketing.",
            )
        return Critique(
            axis="gan-loyalty",
            passed=True,
            comment="No promo language detected. Loyal to the doctrine.",
        )

    def review(self, proposal: ContentProposal) -> AdversaryReview:
        """Run all four axes; emit a verdict."""
        critiques = [
            self.check_truthfulness(proposal),
            self.check_clarity(proposal),
            self.check_witness_presence(proposal),
            self.check_gan_loyalty(proposal),
        ]
        passed = sum(1 for c in critiques if c.passed)
        if passed == len(critiques):
            verdict = VERDICT_PROMOTE
        elif passed >= len(critiques) - 1:
            verdict = VERDICT_REVISE
        else:
            verdict = VERDICT_NOT_VIABLE
        return AdversaryReview(
            proposal_id=proposal.proposal_id,
            verdict=verdict,
            critiques=critiques,
        )


# Convenience CLI

def main():
    import json
    from generator.agent import Generator, GHEvent

    gen = Generator()
    sample = GHEvent(
        event_type="release",
        repo="SuperInstance/quilt-port",
        title="quilt-port v0.1.0",
        url="https://github.com/SuperInstance/quilt-port/releases/tag/v0.1.0",
        body="Initial scaffold of quilt-port — the user's port to their quilts.",
    )
    proposal = gen.route_event(sample)
    if proposal:
        adv = Adversary()
        review = adv.review(proposal)
        print(json.dumps(review.to_dict(), indent=2))


if __name__ == "__main__":
    main()
