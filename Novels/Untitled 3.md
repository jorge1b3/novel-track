# 5e Dataset Phase 2 — SQLite Normalization Design

**Date:** 2026-08-16
**Status:** Approved (design sections 1-3 reviewed by user)

## Goal

Turn the current loose collection of category JSON files into a single, fully
connected SQLite database that powers a backend-driven web app. Every entity,
tag, and reference becomes queryable, traversable, and filterable.

## Decisions (from brainstorming)

- Target: **web app with a backend** (Python: FastAPI/Flask + SQLite).
- **SQLite is the single source of truth.** The per-category JSON files and
  `_index.json` are retired at the end of the rollout.
- The static navigator is **rebuilt as a backend-driven app** (same visual
  language, reusing its proven rendering logic).
- Requested features: global search, linked tags/filters, reference graph
  traversal, analytics/queries, resolve remaining unresolved references.

## Current state (baseline)

- Stage 1 `extract_5etools.py` cleans raw 5etools markup → `data_out/raw/`.
- Stage 2 `structure_5etools.py` assigns ids, types attacks, resolves refs →
  31 category JSON + `_index.json` + `metadata.json` (145 MB, 17,684 entities).
- Known gaps to fix in phase 2:
  - **1,141 bestiary entries still carry raw `_copy`** (5etools inheritance);
    e.g. "Ghalta, Primal Hunger" inherits stats/actions from base "Elder
    Dinosaur" and renders incomplete.
  - **Tag codes are opaque/unlinked**: `damageTags` single letters incl.
    nonstandard `Y`, `L`; `miscTags` codes (`MW`, `AOE`, `MA`, `MLW`, `RCH`,
    `HPR`, `RNG`, `RW`, `THW`, `CUR`, `DIS`). `conditionInflict`,
    `savingThrowForced`, `actionTags` are readable words but still not linked.
  - **507 unresolved refs** are left as `{{ref:tag:name}}` tokens resolved
    only at app runtime.

## Architecture

```
5etools-src/ → extract_5etools.py (stage 1, unchanged) → raw JSON
  → structure_5etools.py (stage 2, rewritten) → data_out/5e.db (only artifact)
  → app/backend/ (FastAPI, read-only over 5e.db)
  → app/frontend/ (vanilla JS SPA, talks only to the API)
```

## Data model (`data_out/5e.db`)

```
meta                  — schema_version, dataset_version, generated_at, source,
                        stats JSON (counts per category, resolved/unresolved,
                        attacks)
entities              — id TEXT PK
                      - category TEXT NOT NULL
                      - name TEXT, sort_name TEXT
                      - source TEXT, adventure_source TEXT
                      - type TEXT
                      - payload TEXT NOT NULL   (original entity JSON)
                      - cr REAL, school TEXT, rarity TEXT, level INT
                        (denormalized, nullable, for fast analytics)
                      - derived_from TEXT NULL  (base entity id, when _copy used)
entities_fts (FTS5)   — standalone FTS5 virtual table, rowid = entities.rowid,
                        columns: name, payload (porter + unicode61 tokenizers);
                        rebuilt on every build run
references            — from_id TEXT → to_id TEXT, ref_type TEXT
                      - PRIMARY KEY (from_id, to_id, ref_type)
                      - INDEX on to_id  (bidirectional traversal)
unresolved_refs       — from_id TEXT, tag TEXT, name TEXT, reason TEXT,
                        attempts INT
tags                  — id TEXT PK
                      - kind TEXT (damage_type | condition | skill | misc |
                                   saving_throw | action_tag)
                      - code TEXT (raw source code, e.g. "F", "MW")
                      - name TEXT (human label, e.g. "Fire", "Magic Weapon")
                      - target_entity_id TEXT NULL  (FK → entities, when the
                        tag corresponds to a real entity, e.g. conditions/skills)
entity_tags           — entity_id TEXT → tags.id  (junction)
                      - PRIMARY KEY (entity_id, tag_id)
```

Notes:
- `payload` keeps the original JSON so rendering is faithful; relational
  columns exist for querying, not as a replacement.
- Tag codes are decoded into canonical `tags` rows. Conditions/skills that
  already exist as entities link via `target_entity_id`; damage types and misc
  tags are standalone rows.
- FTS5 search covers every entity's name + full payload in one index.

## Build pipeline (stage 2 rewrite)

Order of operations inside `structure_5etools.py`:

1. Read raw files → build entities in memory (id assignment, as today).
2. **Materialize `_copy`**: recursively shallow-merge the base entity into the
   variant (variant fields win); repeat while the base itself has `_copy`.
   Record `derived_from`. This is done BEFORE attack typing and ref resolution
   so inherited actions are typed and referenced correctly.
3. **Decode tags** → populate `tags` + `entity_tags` (damage types, misc,
   conditions, saving throws, action tags).
4. **Attack typing** (existing logic, now on materialized entities).
5. **Ref resolution**: existing resolver + a build-time **fuzzy pass** to
   shrink the 507 unresolved; true orphans → `unresolved_refs` with `reason`.
6. Write tables + FTS5 index + `meta`.
7. **Validation step** (see Testing) — fail the build on invariant violations.

## Backend (`app/backend/`)

FastAPI + stdlib `sqlite3`. Read-only connection opened per request; WAL mode.
Pydantic validates query params.

```
GET /api/meta                     — versions, counts, stats
GET /api/categories               — category → count (sidebar)
GET /api/search?q=&category=&source=&damage_type=&condition=&save=
                                  — FTS5 global search + facet filters,
                                    paginated (limit/offset), sorted by rank
GET /api/entities/{id}            — payload + tags + reference counts
GET /api/entities/{id}/references?direction=in|out
                                  — resolved edges, both directions
GET /api/entities/{id}/unresolved — orphan refs for this entity
GET /api/filters                  — facet lists (sources, damage types,
                                    conditions, saves, misc, CR range,
                                    schools, rarities)
GET /api/analytics/damage-types   — entity count per damage type
GET /api/analytics/monsters-by-cr — histogram
GET /api/analytics/spells-by-school — histogram
```

Error responses: 404 JSON `{detail}` for unknown ids; 400 for invalid params;
503 on DB errors.

## Frontend (`app/frontend/`)

Vanilla JS SPA (no framework), same dark-fantasy visual language as the
navigator. Rendering functions from `navigator/app.js` (field cards, attack
badges, data tables, ref chips) are ported into modules.

Views:
- **Home** — dataset stats from `/api/meta`, shortcuts.
- **Global search** — header search bar, live results across all categories,
  filters applied.
- **Category list** — the 31 categories with counts (sidebar), entity tables.
- **Entity detail** — payload rendering + **linked tag chips** (clicking a
  "Fire" chip → all entities dealing fire) + **References** view (what it
  references / what references it, traversable both ways).
- **Unresolved refs** — muted chips with recorded reason.
- **Analytics** — histogram views (damage types, monsters by CR, spells by
  school).

## Error handling

- **Build:** fail-fast with clear messages on invariant violations; `rebuild.sh`
  is idempotent (DB dropped and rebuilt each run).
- **Resolution:** orphans don't fail the build; recorded with a reason in
  `unresolved_refs` and surfaced as muted chips. Fuzzy-pass results are logged
  for tuning.
- **Backend:** read-only per-request connections; 404/400/503 JSON errors;
  Pydantic validation on all params.
- **Frontend:** fetch-error banner; empty states for search/filters; loading
  indicators for heavy payloads; 404 view for unknown ids.

## Testing

- **Pipeline unit tests:** `_copy` materialization, tag decoding, fuzzy ref
  resolution.
- **Validation script** (runs at end of build, fails build on violation):
  - all `references.from_id`/`to_id` exist in `entities`
  - all `entity_tags` targets exist; no duplicate `entity_tags` pairs
  - entity ids unique; `references` PK unique
  - per-category counts == `meta` stats; total == sum
  - no leftover `{@…}` / `[[/…]]` markup anywhere in payloads
  - FTS5: `fireball` returns the Fireball spell, `dragon` returns dragons
- **Backend tests:** pytest + FastAPI TestClient against a fixture DB built
  from a subset of categories; every endpoint incl. 404/400 paths.
- **Frontend smoke:** `node --check` + smoke script hitting the live API +
  manual checklist (global search, tag filter, ref traversal both directions,
  analytics page, unresolved chip).

## Rollout (staging)

1. **Stage A — Data layer:** rewrite `structure_5etools.py` → `5e.db` +
   validation + `rebuild.sh`. The static navigator keeps working this stage
   (JSON still generated) so nothing breaks.
2. **Stage B — Backend:** FastAPI + tests reading `5e.db`.
3. **Stage C — Frontend:** rebuild as API-driven; on acceptance, retire the
   static navigator and the JSON files (JSON removal is the last step).

## Out of scope

- Two-way dataset sync / build versioning/migrations between builds.
- Auth/multi-user.
- Editing/writing data.
- Framework adoption for the frontend (staying vanilla).
