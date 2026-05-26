# ICM How-It-Works + Product Integration (Folio)

**Repository:** [devexley/ICM](https://github.com/devexley/ICM)  
**Scope:** Explain how ICM operates in this project and how `products/folio-takehome/` is integrated.  
**Last updated:** 2026-05-26

---

## 1) What “ICM” means in this repo

This repository is organized as an **ICM portfolio hub**. The operating principle is:

- Work is guided by **contracts** (Markdown files).
- An orchestrating agent should **load only the relevant context** for the current step.
- Each step is represented by a **stage** with its own `CONTEXT.md`.
- The stage contract defines:
  - `## Inputs` (what the agent should rely on)
  - `## Process` (what to do)
  - `## Outputs` (what artifacts must be produced)
- Humans review each stage’s outputs before proceeding.

Concretely: the hub + product + stage contracts describe *how work should be performed*, while `scripts/validate_icm.py` enforces that the structure stays consistent.

---

## 2) Hub structure (where routing rules live)

Top-level “hub” identity and routing are defined in:

- `CLAUDE.md` (Layer 0, identity)
- `CONTEXT.md` (Layer 1, routing to products/stages)
- `_config/conventions.md` (Layer 3, org-wide engineering norms)
- `integration/CONTEXT.md` (Layer 2, used when wiring multiple products)
- `scripts/validate_icm.py` (structure enforcement)

### Hub routing rule

The hub `CONTEXT.md` defines a mapping from user intent to what to load, and a strict constraint:

- Do **not** load all products at once.
- Pick a product, then pick one stage.
- Stage files do not live at hub root; they live under `products/<name>/stages/`.

---

## 3) Product structure (where stage contracts live)

Each product lives under `products/<name>/`. This repo currently has:

- `products/folio-takehome/`

Inside a product:

- `CONTEXT.md`: describes the product’s stage list and feature scope
- `CLAUDE.md`: product identity and how to run it
- `_config/conventions.md`: product-specific rules
- `stages/NN_name/CONTEXT.md`: stage-by-stage contracts

### How `folio-takehome` defines stages

`products/folio-takehome/CONTEXT.md` defines four stages:

| Stage | Folder | Role |
|-------|--------|------|
| 01 | `stages/01_discovery/` | Read codebase + capture ambiguities |
| 02 | `stages/02_design/` | Migrations, ID format, search semantics, tradeoffs |
| 03 | `stages/03_implement/` | Code + tests in the product tree |
| 04 | `stages/04_verify/` | Docker + tests, fresh-clone checklist |

Each stage contract contains `## Inputs`, `## Process`, and `## Outputs`.

---

## 4) Stage contracts (what each stage is responsible for)

Here is the operational intent of each stage contract (as written in the product stage `CONTEXT.md` files):

### Stage 01: Discovery

- Inputs: hub conventions, product conventions, `features.md`, app README, and selected reads of the codebase.
- Process: map admin/share/recipient flows; list ambiguities; propose feature order/scope.
- Outputs (written to `stages/01_discovery/output/`):
  - `discovery.md`
  - `scope.md`
- Audit intent: no code changes outside `output/`.

### Stage 02: Design

- Inputs: Stage 01 outputs + conventions.
- Process: resolve feature decisions; design migration approach and URL/share-token strategy; outline tests.
- Outputs (written to `stages/02_design/output/`):
  - `design.md`
  - `migrations.md`
  - `test-plan.md`
- Audit intent: no application code changed yet.

### Stage 03: Implement

- Inputs: Stage 02 outputs + product conventions + the app codebase tree.
- Process:
  - add migration file(s) (do not edit canonical `schema.sql` for new feature columns)
  - implement features and add tests
  - log implementation notes
- Outputs (written to `stages/03_implement/output/`):
  - `implementation.md`
- Audit intent: implementation matches approved design or deviations are documented; tests exist for shipped features.

### Stage 04: Verify

- Inputs: Stage 03 implementation output + Stage 02 design test plan + app tree.
- Process:
  - run Docker and confirm the app serves
  - run the test command
  - do smoke checks and record results
- Outputs (written to `stages/04_verify/output/`):
  - `verify.md`
  - `video-outline.md`
- Audit intent: verify report includes documented pass/fail and rationale for skipped features (if any).

---

## 5) How the product is “integrated” into ICM (in this repo)

In this repo, integration is primarily **contract wiring** (stage dependencies and verify commands), not runtime API coupling.

### A) Wiring by stage dependency paths

Stages depend on prior stage outputs via the `Inputs` tables:

- Stage 02 `Inputs` references:
  - `../01_discovery/output/`
- Stage 03 `Inputs` references:
  - `../02_design/output/`
- Stage 04 `Inputs` references:
  - `../03_implement/output/implementation.md`
  - `../02_design/output/test-plan.md`

This path-based structure means:

- The agent should not “wing it” from memory.
- Each phase’s artifacts become explicit inputs for the next phase.

### B) Wiring by product routing

The hub `CONTEXT.md` routes “Work on Folio” to:

- `products/folio-takehome/CONTEXT.md`

From there, the product defines which stage contracts are valid and in what order.

### C) Wiring by runtime verification commands

The product’s “verify” stage contract uses the actual Folio test/verification workflow:

- `docker compose up` (app serves)
- `docker compose exec app php tests/test.php` (test correctness)

So “integration” here means: the stage contract is grounded in what the product can actually execute and validate.

---

## 6) What enforces the structure

Two scripts ensure the ICM structure stays valid:

1. `scripts/validate_icm.py`
   - validates hub + product + stage contracts exist and contain required sections
   - validates stage naming/order
   - for `folio-takehome`, it enforces the migration policy:
     - feature columns must be added via `migrations/*.sql`
     - `schema.sql` must not define `public_id` / `published_at`
     - seed/migration behavior is consistent
2. `scripts/icm_run.py`
   - runs commands with pre/post validation
   - logs activity to `logs/hub.log`

These are “integration guardrails” that keep the repo aligned with the stage-contract workflow.

---

## 7) Where your customer-agent portal idea fits

You proposed adding a customer-facing, email-authenticated agent that:

- creates `customer/{email-slug}` branches from `features-dev`
- runs agent work that follows the ICM stage contracts
- runs verify/tests before reporting success
- keeps `main`/`features-dev` protected

That portal orchestration logic would live under `integration/` as it is cross-cutting system behavior layered on top of the existing product (`folio-takehome`) and its stage contracts.

