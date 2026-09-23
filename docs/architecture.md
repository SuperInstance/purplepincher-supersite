# purplepincher-supersite — architecture

**v0.1 — initial scaffold, 9 tests, fleet canary 50/50**

## Layers

```
┌─────────────────────────────────────────────────────────────┐
│  USER                                                        │
│   • Human (visits purplepincher.org)                         │
│   • AI agent (visits /for-agents/)                          │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  SITE (static + worker)                                      │
│   • /, /doctrine/, /fleet/, /for-agents/, /for-humans/      │
│   • /changelog/, /pipeline/                                 │
│   • Static HTML + CSS, hand-curated for v0.1                │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  GAN PIPELINE                                                │
│   • Generator (proposes content from GH events)              │
│   • Adversary (critiques on 4 axes: truth, clarity, witness)│
│   • Orchestrator (one tick: events → proposals → PRs)       │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  GITHUB ORG                                                  │
│   • SuperInstance/  (49 repos, polyformal)                   │
│   • purplepincher/  (33 repos, the org Casey already built) │
└─────────────────────────────────────────────────────────────┘
```

## The Hull Doctrine — applied to the site

| Layer | Hull role |
|-------|-----------|
| Site | **Rigging** on the CF Pages/Worker shell |
| Doctrine pages | **Alive data** — the doctrine is the personal equipment |
| Witness canary on every page | **Tree-rings** — autobiography of the site |
| GAN pipeline | **Rigging that builds rigging** — agents configure how content gets made |
| GH org | **The territory** — the crab's domain |

## The GAN loop in detail

```
GH event
    │
    ▼
Generator Agent
    │  proposes content with witness anchor
    ▼
Adversary Agent
    │  critiques on truth / clarity / witness / GAN-loyalty
    ▼
Verdict
    │  🟢 PROMOTE → stage PR
    │  🟡 REVISE → file review comments, request changes
    │  🔴 NOT VIABLE → archive with witness
    ▼
Casey / human review
    │  approve / archive
    ▼
Site deploys (CF Pages)
```

## Adversary axes

| Axis | Question | Heuristic v0.1 |
|------|----------|-----------------|
| Truthfulness | Does it match code/canon? | Has witnesses + FNV1a canary |
| Clarity | Would a zero-shot reader get it? | Body 50-5000 chars; clear title |
| Witness-presence | Does it leave a tree-ring? | Source URL + canary + doctrine ref |
| GAN-loyalty | Does it serve the doctrine, not advertise? | No promo words |

## Files

- `WORKSHOP.md` — the live workshop doc (12 sections)
- `site/` — the static site source (HTML + CSS)
- `generator/agent.py` — the Generator agent
- `adversary/critic.py` — the Adversary agent
- `pipeline/orchestrate.py` — the orchestrator
- `canary.py` — the FNV1a-64 canary (matches the fleet)
- `run_tests.py` — 9 tests
- `README.md` — public-facing

## Tech choices

- **Plain HTML/CSS** for v0.1 — simpler, faster to ship, no JS deps
- **Astro** planned for v0.2 — adds MDX, content collections, build pipeline
- **Python** for the GAN agents — same language as the rest of the fleet
- **GH Actions** for the cron orchestrator (Phase 3)
- **CF Pages + Worker** for hosting (same as the existing `purplepincher-landing`)

## Migration path to purplepincher org

v0.1 ships under `SuperInstance/` because that's what we have access to.
When the site is mature (Phase 6):

1. Move repo to `purplepincher/` GH org
2. Deploy to `purplepincher.org` (replacing `purplepincher-landing`)
3. Add CF Pages config
4. Enable the GH Actions pipeline cron

The current `purplepincher-landing` (62KB, hand-written landing + WASM demo)
becomes the hero block of the new home page — keep the constraint-theory-core
WASM as the live demo.
