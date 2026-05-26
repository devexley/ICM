# Customer Agent Operation Loop (ICM-Compliant)

**Repository:** [devexley/ICM](https://github.com/devexley/ICM)  
**Status:** Design doc (not implemented)  
**Last updated:** 2026-05-26

## Purpose

Define the repeatable workflow for a customer (logged in by email) who uses a **public agent** to develop and test features on a dedicated branch:

- Create/update `customer/{email-slug}` from `features-dev` once on first login.
- Run ICM-constrained agent work on that branch.
- Execute the app’s verify checks before reporting “done”.

This document is intentionally **ICM contract-first**: the portal (or the backend that orchestrates Cursor) ensures the agent is guided by the correct stage `CONTEXT.md` and allowed outputs.

## Concepts in this repo

### ICM hub contract

The hub defines routing and rules:

- `CONTEXT.md` routes to `products/<name>/CONTEXT.md`
- `_config/conventions.md` sets org-wide engineering norms
- `integration/` is where cross-product wiring lives

### Product stages

Each product contains stage contracts:

For the `folio-takehome` product:

- `products/folio-takehome/stages/01_discovery/CONTEXT.md`
- `products/folio-takehome/stages/02_design/CONTEXT.md`
- `products/folio-takehome/stages/03_implement/CONTEXT.md`
- `products/folio-takehome/stages/04_verify/CONTEXT.md`

Each stage contract specifies:

- **Inputs** (which files/concepts the agent should rely on)
- **Process** (the steps to follow, including human checkpoints)
- **Outputs** (files the agent must write under `output/` and/or code under the app tree)

### Runtime verification

For Folio, the verify stage expects the tests:

- `docker compose exec app php tests/test.php`

And a basic smoke check checklist (admin, share link, scheduling edge, search if built).

## Branch safety model (customer isolation)

Branches:

- `main`: protected, never written by the customer agent
- `features-dev`: protected integration line; never written by the customer agent
- `customer/{email-slug}`: agent writes here only

Promotion path is human-gated:

`customer/{email-slug}` → PR → `features-dev` → PR → `main`

## Operation loop (what happens per customer session)

### 0) Login and identity binding

1. Customer signs in by email.
2. Portal maps email → `email-slug` (example: `jane@example.com` → `customer/jane-at-example-com`).
3. Portal authorizes the customer for the repo/portal tenant (invite list or allowlist).

### 1) Ensure dedicated branch exists

On first login (or when branch is missing):

1. Portal calls GitHub to check `customer/{slug}` exists.
2. If missing, create it from `features-dev`.
3. Record branch creation time and the branch ref.

### 2) Agent run policy: stage-by-stage

The portal enforces a strict stage policy. Two options exist:

#### Option A (strict, recommended): one stage per run

Each agent run does exactly one stage:

1. Discovery run: write `stages/01_discovery/output/*` and stop.
2. Design run: write `stages/02_design/output/*` and stop.
3. Implement run: apply migrations + code + tests (and write `03_implement/output/*`) and stop.
4. Verify run: run Docker/tests and write `04_verify/output/*` and stop.

Pros: fewer surprises, easier human review, matches the stage contracts cleanly.

#### Option B (faster): multiple stages per run

The agent may do stages back-to-back in a single run.

Pros: fewer round-trips.

Cons: harder to enforce “no code changes” constraints for discovery/design and harder to attribute diffs.

This document assumes **Option A** for clarity.

### 3) ICM context envelope injected into the agent prompt

Before starting a run, the portal prepares an “ICM envelope” that includes:

1. Product identity: `folio-takehome`
2. Stage contract path for the current stage
3. Git rules: “commit only to the current branch”
4. Verification commands expected for the stage

The cloud VM will already have the repo checked out at `customer/{slug}` if the agent is launched with that branch as the starting ref and `workOnCurrentBranch: true`.

### 4) Persist run metadata for the UI

After each run, the portal stores (at least):

- Cursor agent/run id
- branch name
- git diff summary (optional)
- stage name
- test output summary (especially from verify stage)

This is what the customer sees as “progress”.

## Verification contract (what “done” means)

### For Folio verify stage

At minimum, the portal (or the agent, depending on your design) must execute:

1. `docker compose up` (or ensure it’s already up)
2. `docker compose exec app php tests/test.php`

If tests fail, the run outcome is “failed” and the portal should prompt for a fix request tied to the failing tests.

### For customer UI

The portal should show:

- whether tests passed
- a short excerpt of failing test output when they didn’t
- the branch link (GitHub compare / commit view)

## Security invariants (enforced by portal + git)

1. The agent must only be launched with `startingRef = customer/{slug}`.
2. `features-dev` and `main` must be protected against direct pushes from the portal GitHub App.
3. Customer sessions must be authorized (email → branch mapping enforced on every request).
4. Rate limits and quotas should prevent repeated costly runs.

## Example timeline (one customer task)

1. Customer logs in
2. Portal ensures `customer/jane-at-example-com` exists (created from `features-dev`)
3. User asks: “Implement scheduled publishing”
4. Portal starts stage 01 discovery run
5. Customer approves scope (or portal proceeds automatically depending on policy)
6. Portal starts stage 02 design run
7. Portal starts stage 03 implement run (migrations + code + tests)
8. Portal starts stage 04 verify run (docker + tests)
9. Portal shows results; optional PR to `features-dev` if user requests it

## Acceptance criteria (smoke checks)

1. Login creates the branch from `features-dev` only once.
2. No run results in a direct change to `features-dev` or `main`.
3. Implement stage adds tests for each shipped feature (per stage contract).
4. Verify stage reports pass/fail of `docker compose exec app php tests/test.php`.
5. The portal shows the branch that was modified and the run outcome.

