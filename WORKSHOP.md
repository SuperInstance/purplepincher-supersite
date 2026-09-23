# Workshop — `purplepincher-supersite`

**The educational supersite that evolves with the SuperInstance github account.**
**Date**: Sept 23, 2026
**Author**: Casey + Mavis
**Trigger**: *Casey — "we should reinvent the purplepincher.org site completely to be an educational supersite for superinstance with pipelines for iterive improvements on its own as the github account evolves... that is, after it's been not just built, but GAN improved by both agents and me"*
**Status**: **DRAFT** — the site evolves alongside the github org; this workshop doc is the live state.

---

## TL;DR

**`purplepincher.org` is not a static landing page. It's an educational supersite that learns from the SuperInstance github account.**

Three commitments:

1. **Educational, not promotional.** Every page teaches. The doctrine, the code, the names — all explained for both humans and agents.
2. **Self-improving.** The site has its own CI that watches GH activity and proposes new content. Humans + agents review (GAN loop). Approve → publish.
3. **Tied to the github org's evolution.** When a new repo ships, when a doctrine clarification lands, when a release cuts — the site surfaces it, explained.

This is the **second lane** to the quilt-port work. Both lanes run in parallel.

---

## 1. The vision in Casey's words

> "we should reinvent the purplepincher.org site completely to be an educational supersite for superinstance with pipelines for iterive improvements on its own as the github account evolves"

> "we also have the purplepincher org as connected to our superinstance account on github so we can do the front-end work for the purplepincher supersite there when its mature"

> "that is, after it's been not just built, but GAN improved by both agents and me"

Three things to internalize:

### a) Educational supersite

The current landing (`purplepincher-landing`, 62KB of HTML + a Rust WASM demo) is good but **minimal**. Casey wants a complete reinvention — *educational*, not just landing-page.

What does "educational" mean here?

- **The Hull Doctrine** is the core teaching. The site should make it intuitive — for humans, for AI agents, and for the people who'd just glance at the name and say "oh, hermit crabs".
- **Each repo gets an explainer.** Why does `cellforge` exist? What does `moth-corpus` actually do? Why is the FNV1a-64 canary at `0x24a555471370b18d`?
- **Each doctrine clarification gets a page.** When we discover the model is the shell (not just metaphorically), there's a page.
- **Each release cuts a changelog entry**, with receipts.
- **The naming story** is told: why "purplepincher", why "superinstance", why `.dev` instead of `.ai`.

### b) Self-improving via GH pipelines

The site watches the GH account. When something happens, it proposes new content. The proposal:

1. Goes through a generator agent (proposes content based on GH events)
2. Goes through an adversary pass (critique: "is this accurate? does it witness?")
3. Gets reviewed by Casey (and other humans)
4. Either merges into the site or gets archived with a witness

This is the **GAN loop** applied to content. Same doctrine as `mavis-axui-feedback`'s GAN loop, lifted to a documentation surface.

### c) GAN-improved by both agents and Casey

Both agents (Mavis, future subagents) AND Casey iterate. The site is not finished — it's *always being GAN-improved*. Each round:

- Generator proposes
- Adversary critiques
- Both Casey and agents weigh in
- Net improvement lands

This is the **agentic-community** in flow — the team reading and writing, the doctrine refining.

---

## 2. Where it lives

### Repo: `SuperInstance/purplepincher-supersite` (for now)

Casey said: "we also have the purplepincher org as connected to our superinstance account on github so we can do the front-end work for the purplepincher supersite there when its mature"

So:
- **v0.x**: ship under `SuperInstance/` org — that's what we have access to and the work surface
- **When mature**: move to the `purplepincher` org (already exists with 33 repos, including the current `purplepincher-landing`)

The repo will eventually *replace* `purplepincher-landing` as the canonical deploy target.

### Deployment: CF Pages

Same as the existing landing — Cloudflare Pages + a Worker for any dynamic parts (changelog feed, search, the GAN pipeline's UI).

### URL strategy

- `purplepincher.org` — the supersite (replaces the current landing)
- `docs.purplepincher.org` — possibly the same thing if we keep it as one site
- The Worker entry handles `/api/*` for the GAN pipeline's status + recent activity

---

## 3. The site structure (proposed)

```
purplepincher.org/
├── /                              # Home: the doctrine in 90 seconds
├── /doctrine/
│   ├── /                          # Full Hull Doctrine (mirrors HULL_DOCTRINE.md)
│   ├── /shell/                    # The model as shell
│   ├── /rigging/                  # The code as rigging
│   ├── /equipment/                # The data as alive equipment
│   └── /tree-rings/               # The witness chain as autobiography
├── /fleet/
│   ├── /                          # All repos, ranked by activity
│   ├── /quilt-port/               # Per-repo explainer
│   ├── /cellforge/
│   ├── /moth-corpus/
│   └── ... (one per repo)
├── /for-agents/
│   ├── /                          # Agent-facing intro
│   ├── /contribute/               # How to contribute as an agent
│   ├── /cite/                     # How to cite canon in your work
│   └── /prompt-templates/         # The recommended prompts
├── /for-humans/
│   ├── /                          # Human-facing intro
│   ├── /naming/                   # The naming story
│   ├── /press-kit/                # Logos, boilerplate, screenshots
│   └── /case-studies/             # Real users, real receipts
├── /changelog/
│   ├── /                          # Activity feed
│   └── /2026-09-23-hull-doctrine/ # One entry per notable event
├── /pipeline/
│   ├── /                          # The GAN pipeline status (public)
│   └── /agent-log/                # What the agents have proposed, what's live
└── /api/
    └── /                          # Worker entry: changelog JSON, search, etc.
```

Each section has its own purpose:

- **`/`** — the 90-second intro for a zero-shot visitor
- **`/doctrine/`** — the teaching; this is the *why* of everything
- **`/fleet/`** — the inventory; this is the *what* of everything
- **`/for-agents/`** and **`/for-humans/`** — dual entry points
- **`/changelog/`** — the activity stream
- **`/pipeline/`** — the meta: the GAN loop in public

---

## 4. The content model

Every page is one of three types:

### a) Doctrine pages

Static-ish. The Hull Doctrine is canon, so these change slowly. Generated from `HULL_DOCTRINE.md` and sister docs (with a build step that converts MD to MDX with embedded components).

### b) Fleet pages

Auto-generated. The site watches the GH org, and for each repo produces:
- One explainer page (`/fleet/<repo>/`)
- One entry in `/fleet/` index
- One entry in `/changelog/` when updated

The generator agent decides how to explain each repo — based on its README, its witness chain, its recent PRs.

### c) Changelog entries

Generated by the GAN pipeline. Every notable GH event (release, doctrine update, PR merge, witness emission) becomes a changelog entry. The adversary pass ensures each entry is *teaching*, not just narrating.

---

## 5. The GAN pipeline

```
GH event ──► Generator Agent ──► Proposed content
                                     │
                                     ▼
                              Adversary Agent ──► Critique + fixes
                                     │
                                     ▼
                          Casey / human reviewer ──► Approve / archive
                                     │
                                     ▼
                                Site updated
```

### Generator Agent (`generator/agent.py`)

- Watches GH events (PRs, releases, doctrine updates)
- Proposes content based on event type
- Anchors every proposal to a witness (the GH event IS the witness)
- Stages as PR to the site repo

### Adversary Agent (`adversary/critic.py`)

- Reads the proposal
- Checks for: truthfulness (does it match the code/canon?), clarity (would a zero-shot reader get it?), witness-presence (does it leave a tree-ring?), GAN-loyalty (does it serve the doctrine, not advertise?)
- Files review comments on the PR
- If the proposal is misleading, marks `🔴 NOT VIABLE`

### Human reviewer (Casey)

- Reviews the Adversary's critique
- Approves / requests changes / archives
- Approve → PR merges → site deploys

### Pipeline orchestration (`pipeline/`)

- GH Actions cron runs every 6 hours
- Generator proposes from recent activity
- Adversary reviews asynchronously
- Casey / humans review on their schedule
- Site deploys on merge

---

## 6. Tech stack (proposed for v0.1)

- **Astro** — static-first, MDX support, content collections
- **TypeScript** — the static parts
- **MDX** — content with embedded components (interactive demos, callouts)
- **CF Pages** — deployment target
- **CF Worker** — `/api/*` routes (changelog JSON, search, pipeline status)
- **Python** — GAN pipeline agents (separate from the site)
- **GH Actions** — pipeline orchestration

This is conventional. The unusual part is the **GAN agent layer**.

---

## 7. Doctrinal commitments

### a) The site is canon-with-witness

Every page that makes a claim has a witness — either an inline citation to the canon or a witness-chain anchor at the bottom.

### b) The site is alive

Changelog entries that don't appear within 24 hours of the underlying event mean the pipeline is broken. **The site is a receipted surface.**

### c) The site is honest

Honesty convention used throughout (carried from `purplepincher-landing`):
- ✅ **real today** — traced to working code in this org
- ⚠️ **real but conditional** — works, but needs something external
- 🔮 **aspirational / later phase** — a direction, not implemented

Every capability claim is tagged. The site can never lie about what it is.

### d) The site is forkable

Same as `quilt-port`: the site source is OSS, the deployment is convenience. Anyone can fork and deploy their own purplepincher-style educational site.

---

## 8. What this does for the agentic community

This is the *visible* surface of the doctrine. The Hull Doctrine, until now, has lived in `HULL_DOCTRINE.md` inside a code repo. Putting it on `purplepincher.org` means:

- Anyone who visits learns the system model without reading code
- The doctrine gets walked through interactively (callouts, demos, examples)
- New contributors can read the doctrine in their preferred format (HTML vs MD)
- The naming story is told once and forever, on the org's own domain
- The site itself demonstrates the doctrine (it's rigging on the model's hull — built by humans + agents, deployed to a shell, evolving)

---

## 9. Roadmap

### Phase 0 — workshop (this doc)

Iterate the angles. Get Casey's read on:
- Should the doctrine live at `/doctrine/` mirrored from HULL_DOCTRINE.md, or be a re-written HTML version?
- Do we ship v0.1 with hand-written content first, then layer the GAN pipeline, OR ship both at once?
- Where does the GAN pipeline live — same repo as the site, or separate `purplepincher-pipeline`?

### Phase 1 — basic scaffold + doctrine landing

- Astro project structure
- `/` — the 90-second intro
- `/doctrine/` — the Hull Doctrine, full text
- A few hand-written fleet entries
- Deploy to `purplepincher.org` (CF Pages)

### Phase 2 — fleet generation

- Generator agent watches the GH org
- Auto-generates `/fleet/<repo>/` pages from READMEs + witness chains
- Adversary reviews each generation
- Index page lists all repos, sorted by activity

### Phase 3 — changelog + pipeline UI

- Changelog feed
- Pipeline status page (`/pipeline/`)
- Agent-log page (what's been proposed, what's live)
- Open Adversary reviews publicly

### Phase 4 — interactivity

- Interactive Hull Doctrine walkthrough
- Live code demos (embedded WASM from the landing)
- Search + filter
- The doctrine, click-able

### Phase 5 — community contribution

- `/for-agents/` becomes interactive (agents can submit proposals via the UI)
- `/for-humans/` becomes interactive (humans can request topics)
- The site becomes self-sustaining

### Phase 6 — move to purplepincher org

When the site is mature, move the repo from `SuperInstance/` to `purplepincher/` org on GH. This is the "front-end work for the purplepincher supersite" Casey mentioned.

---

## 10. Open questions (workshop!)

1. **Is the existing `purplepincher-landing` Worker retained or replaced?** My instinct: replace (the supersite subsumes it). But the WASM demo is load-bearing — keep it as a hero on the new home page.
2. **What tech stack?** Astro is my first pick. Casey — what do you think?
3. **Where does the GAN pipeline live?** Same repo or separate? My instinct: separate, so the site repo stays clean and the pipeline can be tested in isolation.
4. **How aggressive is the GAN?** A pipeline that generates 5 proposals/day would be noisy. My instinct: 1-2 proposals/day, high quality, with the Adversary pass filtering.
5. **Should the doctrine be the home page, or below the fold?** My instinct: above the fold — the doctrine IS the product.
6. **What about the existing 32 other repos in the purplepincher org?** The pipeline should generate fleet entries for them too, with appropriate context.
7. **How does the user "navigate" the site?** A side-rail with the doctrine sections? A top bar? A "click any term" hover-glossary? My instinct: all three.

---

## 11. The deep meaning

> "the model is the shell, the code is the rigging, the data is alive, the witness chain is the tree-rings"

The site IS the doctrine made visible. It demonstrates itself: it's a hermit-crab finding a shell (the CF Pages / Worker hosting), rigging it (the Astro framework), accumulating equipment (the doctrine, the canon, the recipes), and recording tree-rings (the changelog).

When the site teaches the doctrine, it's not just describing it — *it's living it*. The visitor sees the doctrine applied to itself. That's the lesson no other site can teach.

---

*This workshop is meant to be done in passes. Each pass sharpens one section, raises new questions in another. The end state is an educational supersite that GAN-improves forever, in flow with the github org's evolution.*
