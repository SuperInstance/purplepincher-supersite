# purplepincher-supersite

**The educational supersite that evolves with the SuperInstance github account.**
**Live at**: purplepincher.org (when deployed; v0.1 currently local)

> "We should reinvent the purplepincher.org site completely to be an educational supersite for superinstance with pipelines for iterive improvements on its own as the github account evolves." — Casey, Sept 23, 2026

## What is this?

A static site that:

1. **Teaches** the Hull Doctrine — the system model that the SuperInstance org lives by
2. **Catalogs** every repo in the fleet, with explainers
3. **Self-improves** via a GAN pipeline — agents propose, agents critique, humans approve
4. **Surfaces** every notable GH event as a changelog entry

The site itself is a witness: it shows the doctrine applied to itself (it's a hermit-crab finding its shell, rigging it, accumulating equipment, recording tree-rings).

## Structure

```
purplepincher.org/
├── /              — the 90-second intro
├── /doctrine/     — the Hull Doctrine, walked through interactively
├── /fleet/        — every repo, explained
├── /for-agents/   — agent-facing intro + contribution guide
├── /for-humans/   — human-facing intro + press kit
├── /changelog/    — activity feed
├── /pipeline/     — the GAN loop, in public
└── /api/          — Worker entry: changelog JSON, search, pipeline status
```

## The GAN loop

```
GH event → Generator Agent (proposes) → Adversary Agent (critiques) → Casey (decides) → Site updated
```

Each step witnesses. Each step is reproducible. The site is a receipted surface — every claim has a witness.

## Tech stack

- **Astro** — static-first with MDX islands
- **TypeScript** — the static parts
- **MDX** — content with embedded components
- **CF Pages** — deployment
- **CF Worker** — `/api/*` routes
- **Python** — GAN pipeline agents
- **GH Actions** — pipeline orchestration

## Versions

- v0.1.0 — workshop doc + scaffold; hand-written doctrine landing; fleet canary verified
- v0.2.0 — fleet generation via GAN
- v0.3.0 — interactive doctrine walkthrough
- v1.0.0 — moves to `purplepincher/` GH org

## Doctrinal commitments

- ✅ **Real today** vs ⚠️ **Real but conditional** vs 🔮 **Aspirational** — every capability claim tagged
- **Witnessed** — every claim has a citation or witness-chain anchor
- **Alive** — changelog entries appear within 24h of GH events (or the pipeline is broken)
- **Forkable** — OSS source; anyone can deploy their own purplepincher-style educational site

## Files

- `WORKSHOP.md` — the live workshop doc (15 sections, iterate here)
- `docs/architecture.md` — diagrams + tier details
- `src/` — the Astro site source
- `generator/` — GAN generator agent (Python)
- `adversary/` — GAN adversary agent (Python)
- `pipeline/` — orchestration config
- `canary.py` — polyformalism canary (matches the fleet)

## License

MIT.
