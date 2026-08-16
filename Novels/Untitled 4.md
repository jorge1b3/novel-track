# SQLite Normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the loose category-JSON dataset with a single normalized SQLite database (`data_out/5e.db`) that powers a backend-driven web app with global search, linked tag filters, bidirectional reference graphs, and analytics.

**Architecture:** 3 staged phases. (A) Rework `structure_5etools.py` to materialize `_copy`/`_mod` inheritance, decode tag codes, and emit `5e.db` (+ validation) while still writing JSON. (B) FastAPI backend over `5e.db`. (C) Rebuild the frontend as API-driven and retire JSON.

**Tech Stack:** Python 3 + stdlib `sqlite3` (with FTS5), FastAPI + uvicorn (in a venv at `app/backend/.venv`), pytest + httpx (TestClient), vanilla JS ES modules.

**Note:** the repo root is NOT a git repository, so the "commit" steps are omitted from this plan.

---

## 1. Application context

The project turns the raw 5etools 5e data dump (`5etools-src/`) into a usable, typed dataset for personal use.

- `extract_5etools.py` (stage 1) cleans `{@tag ...}` markup and merges source files → `data_out/raw/`.
- `structure_5etools.py` (stage 2) assigns stable ids (`<category>-<slug>-<source>`, `adventure-entry-...`), resolves `[tag:name|source]` references into `{{ref:<id>}}` tokens, types monster attacks into structured objects, and aggregates per-entity `references`.
- A static navigator (`navigator/`, vanilla JS) currently browses the 31 category JSON files (145 MB, 17,684 entities, 53,031 indexed ids incl. nested adventure sections).

### What the user wants

A "phase two" that makes ALL data connected, on top of which a bigger app can be built. Specifically (decided in brainstorming):

- **Global search** across all categories at once (FTS).
- **Linked tags/filters** — decode opaque codes (`damageTags` letters like `A`/`B`/`Y`, `miscTags` like `MW`/`RCH`) into real, linkable tags; filter "monsters dealing fire damage", "monsters that inflict the grappled condition", "forces a CON save", etc.
- **Reference graph traversal** — what an entity references and what references it, both directions, across the whole dataset.
- **Analytics/queries** — damage-type distributions, monsters-by-CR, spells-by-school.
- **Resolve remaining references** — the ~507 unresolved refs get a build-time fuzzy pass; true orphans stay marked with a reason.
- **SQLite becomes the single source of truth**; JSON files are retired at the end.
- **Rebuild the frontend as a backend-driven app** (same dark-fantasy visual language).

### Known data gaps this plan fixes

1. **1,141 bestiary entries still carry raw `_copy`** — variants like "Elder Dinosaur (Ghalta, Primal Hunger)" only store *overrides*; their stats/actions live in the base "Elder Dinosaur" entry and must be materialized at build time. The `_mod` (inheritance) system inside `_copy` uses modes: `appendArr`, `prependArr`, `insertArr`, `appendIfNotExistsArr`, `replaceArr` (with `replace`), `removeArr`, `replaceTxt`, `setProp`, `addSkills`, `addSpells`, `replaceSpells`, `removeSpells`; wildcard keys `_` and `*` mean "apply everywhere in the subtree".
2. **Opaque tag codes** — the fork's `damageTags` mapping (verified empirically AND in `5etools-src/js/parser.js:4484-4498`): `A`=acid `B`=bludgeoning `C`=cold `F`=fire `I`=poison `L`=lightning `N`=necrotic `O`=force `P`=piercing `R`=radiant `S`=slashing `T`=thunder `Y`=psychic. `miscTags` (from `parser.js:2033-2046`): `AOE`=Has Areas of Effect, `CUR`=Inflicts Curse, `DIS`=Inflicts Disease, `HPR`=Has HP Reduction, `MW`=Has Weapon Attacks, Melee, `RW`=Has Weapon Attacks, Ranged, `MA`=Has Attacks, Melee, `RA`=Has Attacks, Ranged, `MLW`=Has Melee Weapons, `RNG`=Has Ranged Weapons, `RCH`=Has Reach Attacks, `THW`=Has Thrown Weapons. Spell schools (this fork, single-letter): `A`=Abjuration `C`=Conjuration `D`=Divination `E`=Enchantment `I`=Illusion `N`=Necromancy `T`=Transmutation `V`=Evocation.
3. **507 unresolved refs** — currently left as `{{ref:tag:name}}` and only fuzzy-matched at app runtime.
4. **Adventure section references not attributed** — today all adventure refs aggregate into one list; they must be attributed per section.

---

## 2. Design (approved spec summary)

Full spec: `docs/superpowers/specs/2026-08-16-sqlite-normalization-design.md`.

### Data model (`data_out/5e.db`)

```
meta                  — key TEXT PK, value TEXT (schema_version, dataset_version,
                        generated_at, source JSON, counts JSON, stats JSON)
entities              — id TEXT PK, category, name, sort_name, source,
                        adventure_source, type, cr REAL, school, rarity,
                        level INT, derived_from, payload TEXT (entity JSON)
entities_fts (FTS5)   — contentless (content=''), rowid = entities.rowid,
                        columns: name, payload; tokenize 'porter unicode61'
references            — from_id, to_id, ref_type; PK(from_id,to_id,ref_type);
                        INDEX(to_id)
unresolved_refs       — from_id, tag, name, source, reason, attempts INT
tags                  — id PK, kind, code, name, target_entity_id NULL
                        kinds: damage_type | condition | skill | misc |
                               saving_throw | action_tag
entity_tags           — entity_id, tag_id; PK(entity_id, tag_id); INDEX(tag_id)
```

### Build pipeline (stage A)

1. Read raw → `build_ids` (as today)
2. **Materialize** `_copy`/`_mod` per category (before attack typing + ref resolution)
3. Decode tags → `tags` + `entity_tags`
4. Attack typing (existing logic, on materialized entities)
5. Ref resolution + **fuzzy pass** → `references` / `unresolved_refs`
6. Attribute adventure section refs per section
7. Write JSON (stage A only) + build `5e.db` + validate

### Backend endpoints

```
GET /api/meta | /api/categories
GET /api/search?q=&category=&source=&damage_type=&condition=&save=&school=&rarity=&cr_min=&cr_max=&limit=&offset=
GET /api/entities/{id}
GET /api/entities/{id}/references?direction=in|out
GET /api/entities/{id}/unresolved
GET /api/filters
GET /api/analytics/damage-types | monsters-by-cr | spells-by-school
```
Backend also serves the frontend statically at `/`. 404/400 JSON errors.

### Frontend

Vanilla JS ES modules, hash routes `#/`, `#/c/<cat>`, `#/s/<encoded params>`, `#/e/<id>`, `#/a/<name>`. Views: home (stats), global search, category list, entity detail (payload + tag chips + refs in/out), unresolved chips, analytics histograms.

---

## 3. File structure

```
materialize.py                          NEW  _copy/_mod inheritance
fuzzy.py                                NEW  second-pass ref resolution
db_writer.py                            NEW  schema, build_db, tag decode
validate_db.py                          NEW  invariant checks
structure_5etools.py                    MODIFY  materialize, section refs, db+validate
rebuild.sh                              NEW  extract -> structure -> validate
tests/test_materialize.py               NEW
tests/test_fuzzy.py                     NEW
tests/test_db_writer.py                 NEW
tests/fixtures/*.json                   NEW  tiny fixtures for db/backend tests
app/backend/requirements.txt            NEW
app/backend/main.py                     NEW  FastAPI (API + static frontend)
app/backend/run.sh                      NEW
app/backend/tests/test_api.py           NEW
app/frontend/index.html                 NEW
app/frontend/style.css                  NEW
app/frontend/js/api.js                  NEW
app/frontend/js/render.js               NEW  ported render logic
app/frontend/js/app.js                  NEW  routing + views
app/frontend/smoke.sh                   NEW
```

---

## PHASE A — DATA LAYER

### Task A1: `materialize.py` — `_copy`/`_mod` inheritance

**Files:**
- Create: `materialize.py`
- Test: `tests/test_materialize.py`

- [ ] **Step 1: Write the failing tests**

```python
import copy
import pytest

import materialize


def make(extra):
    ent = {"name": "A", "source": "PSX", "id": "monster-a-psx"}
    ent.update(extra)
    return ent


def lookup_from(entities):
    return {materialize.norm_key(e["name"]): e for e in entities}


@pytest.fixture
def base():
    return make({
        "ac": 17, "hp": 100, "languages": ["Common"],
        "action": [{"name": "Bite", "entries": ["Melee Attack: +5 to hit, one target."]}],
        "skills": {"perception": 4},
    })


def test_plain_copy_merges_base_fields(base):
    variant = make({
        "name": "A (Young)", "_copy": {"name": "A", "source": "PSX"}, "page": 5,
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    assert out["ac"] == 17
    assert out["hp"] == 100
    assert out["page"] == 5
    assert out["name"] == "A (Young)"
    assert out["id"] == "monster-a-psx"
    assert out["derived_from"] == "monster-a-psx"


def test_append_arr_adds_actions(base):
    variant = make({
        "name": "A (Young)",
        "_copy": {"name": "A", "source": "PSX", "_mod": {
            "action": {"mode": "appendArr", "items": [
                {"name": "Multiattack", "entries": ["The creature attacks."]}]}}},
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    names = [a["name"] for a in out["action"]]
    assert names == ["Bite", "Multiattack"]


def test_replace_arr_with_replace(base):
    variant = make({
        "name": "A (Young)",
        "_copy": {"name": "A", "source": "PSX", "_mod": {
            "action": {"mode": "replaceArr", "replace": "Bite", "items": [
                {"name": "Bite", "entries": ["New bite."]}]}}},
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    assert out["action"][0]["entries"] == ["New bite."]


def test_replace_arr_whole(base):
    variant = make({
        "name": "A (Young)",
        "_copy": {"name": "A", "source": "PSX", "_mod": {
            "languages": {"mode": "replaceArr", "items": ["Draconic"]}}},
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    assert out["languages"] == ["Draconic"]


def test_prepend_and_remove(base):
    variant = make({
        "name": "A (Young)",
        "_copy": {"name": "A", "source": "PSX", "_mod": {
            "action": [
                {"mode": "prependArr", "items": [{"name": "Slam", "entries": ["S."]}]},
                {"mode": "removeArr", "names": "Bite"},
            ]}},
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    assert [a["name"] for a in out["action"]] == ["Slam"]


def test_insert_arr_index_and_negative(base):
    variant = make({
        "name": "A (Young)",
        "_copy": {"name": "A", "source": "PSX", "_mod": {
            "action": {"mode": "insertArr", "index": -1, "items": {"name": "Stomp", "entries": ["St."]}}}},
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    assert [a["name"] for a in out["action"]] == ["Bite", "Stomp"]


def test_wildcard_replace_txt(base):
    variant = make({
        "name": "A (Young)",
        "_copy": {"name": "A", "source": "PSX", "_mod": {
            "*": {"mode": "replaceTxt", "replace": "the dragon", "with": "A (Young)", "flags": "i"}}},
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    assert out["action"][0]["entries"] == ["Melee Attack: +5 to hit, one target."]


def test_wildcard_add_skills_and_set_prop(base):
    variant = make({
        "name": "A (Young)",
        "_copy": {"name": "A", "source": "PSX", "_mod": {
            "_": [
                {"mode": "addSkills", "skills": {"stealth": 8}},
                {"mode": "setProp", "prop": "vulnerable", "value": ["cold"]},
            ]}},
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    assert out["skills"]["stealth"] == 8
    assert out["skills"]["perception"] == 4
    assert out["vulnerable"] == ["cold"]


def test_add_replace_remove_spells():
    base = make({"spellcasting": {"spells": {
        "0": {"spells": ["[spell:fire bolt]"]},
        "1": {"slots": 2, "spells": ["[spell:burning hands]"]},
        "2": {"spells": ["[spell:scorching ray]"]},
    }}})
    variant = make({
        "name": "A (Young)",
        "_copy": {"name": "A", "source": "PSX", "_mod": {
            "_": [
                {"mode": "addSpells", "spells": {"1": {"spells": ["[spell:shield]"]}, "will": ["[spell:mage hand]"]}},
                {"mode": "replaceSpells", "spells": {"2": [{"replace": "[spell:scorching ray]", "with": "[spell:fireball]"}]}},
                {"mode": "removeSpells", "daily": {"3e": ["[spell:magic missile]"]}},
            ]}},
    })
    out = materialize.materialize_entity(variant, lookup_from([base, variant]))
    sc = out["spellcasting"]["spells"]
    assert "[spell:shield]" in sc["1"]["spells"]
    assert sc["will"] == ["[spell:mage hand]"]
    assert sc["2"]["spells"] == ["[spell:fireball]"]
    assert sc.get("daily") is None or "3e" not in sc["daily"]


def test_recursive_copy(base):
    mid = make({"name": "B", "source": "PSX", "ac": 99, "_copy": {"name": "A", "source": "PSX"}})
    top = make({"name": "C", "source": "PSX", "hp": 1, "_copy": {"name": "B", "source": "PSX"}})
    out = materialize.materialize_entity(top, lookup_from([base, mid, top]))
    assert out["ac"] == 99
    assert out["hp"] == 1


def test_missing_base_raises():
    variant = make({"name": "X", "source": "PSX", "_copy": {"name": "Nope", "source": "PSX"}})
    with pytest.raises(materialize.MissingBaseError):
        materialize.materialize_entity(variant, lookup_from([variant]))


def test_does_not_mutate_base(base):
    variant = make({"name": "A (Young)", "_copy": {"name": "A", "source": "PSX", "_mod": {
        "action": {"mode": "appendArr", "items": [{"name": "Multiattack", "entries": []}]}}}})
    materialize.materialize_entity(variant, lookup_from([base, variant]))
    assert [a["name"] for a in base["action"]] == ["Bite"]
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_materialize.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'materialize'`

- [ ] **Step 3: Implement `materialize.py`**

```python
"""Materialize 5etools `_copy`/`_mod` inheritance into complete entities."""

import copy
import re


class MissingBaseError(Exception):
    pass


class CopyCycleError(Exception):
    pass


def norm_key(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def _as_list(x):
    return x if isinstance(x, list) else [x]


def _norm_name(x):
    if isinstance(x, dict):
        return norm_key(x.get("name") or x.get("caption") or "")
    return norm_key(str(x))


def _iter_nodes(v):
    yield v
    if isinstance(v, dict):
        for x in v.values():
            yield from _iter_nodes(x)
    elif isinstance(v, list):
        for x in v:
            yield from _iter_nodes(x)


def _resolve(obj, path):
    results = []

    def walk(cur, i):
        if i == len(path):
            results.append(cur)
            return
        comp = path[i]
        if isinstance(cur, dict) and comp in cur:
            walk(cur[comp], i + 1)
        elif isinstance(cur, list):
            for item in cur:
                walk(item, i)

    walk(obj, 0)
    return results


def _replace_text_in(v, search, with_, flags):
    rx = re.compile(search, flags)
    if isinstance(v, str):
        return rx.sub(with_, v)
    if isinstance(v, list):
        for i, x in enumerate(v):
            v[i] = _replace_text_in(x, search, with_, flags)
    elif isinstance(v, dict):
        for k in list(v.keys()):
            v[k] = _replace_text_in(v[k], search, with_, flags)
    return v


def _as_list_of(obj):
    return obj if isinstance(obj, list) else [obj]


def _apply_to_array(node, op):
    """Array mutation ops against `node` (the array value found at the path)."""
    mode = op.get("mode")
    if mode == "appendArr":
        node.extend(copy.deepcopy(op.get("items", [])))
    elif mode == "prependArr":
        node[0:0] = copy.deepcopy(_as_list_of(op.get("items", [])))
    elif mode == "insertArr":
        items = copy.deepcopy(_as_list_of(op.get("items", [])))
        idx = int(op.get("index", 0))
        if idx < 0:
            idx = max(0, len(node) + 1 + idx)
        node[idx:idx] = items
    elif mode == "appendIfNotExistsArr":
        seen = {_norm_name(x) for x in node}
        for item in copy.deepcopy(op.get("items", [])):
            if _norm_name(item) not in seen:
                node.append(item)
                seen.add(_norm_name(item))
    elif mode == "replaceArr":
        items = copy.deepcopy(_as_list_of(op.get("items", [])))
        repl = op.get("replace")
        if repl:
            for i, x in enumerate(node):
                if _norm_name(x) == _norm_name(repl):
                    node[i] = items[0]
                    break
        else:
            node[:] = items
    elif mode == "removeArr":
        names = {_norm_name(n) for n in _as_list(op.get("names"))}
        node[:] = [x for x in node if _norm_name(x) not in names]


def _replace_spells_list(lst, pairs):
    for pair in pairs:
        src = norm_key(pair.get("replace"))
        with_ = pair.get("with")
        for i, s in enumerate(lst):
            if norm_key(s) == src:
                lst[i] = with_


def _add_skills(node, skills):
    if not isinstance(node, dict) or "skills" not in node:
        return
    cur = node["skills"]
    if isinstance(cur, dict):
        for name, bonus in skills.items():
            cur[name] = int(bonus)
    elif isinstance(cur, list):
        for name, bonus in skills.items():
            cur.append({name: int(bonus)})


def _add_spells(node, spells):
    if not isinstance(node, dict) or "spells" not in node:
        return
    cur = node["spells"]
    for level, value in spells.items():
        if isinstance(value, dict) and "spells" in value:
            bucket = cur.setdefault(level, {})
            bucket.setdefault("spells", []).extend(copy.deepcopy(value["spells"]))
        elif isinstance(value, list):
            cur.setdefault(level, []).extend(copy.deepcopy(value))


def _remove_spells(cur, remove_spec):
    for bucket, vals in remove_spec.items():
        entry = cur.get(bucket)
        if isinstance(entry, dict):
            if isinstance(vals, dict):
                _remove_spells(entry, vals)
            elif "spells" in entry:
                rm = {norm_key(x) for x in vals}
                entry["spells"] = [s for s in entry.get("spells", []) if norm_key(s) not in rm]
        elif isinstance(entry, list) and isinstance(vals, list):
            rm = {norm_key(x) for x in vals}
            cur[bucket] = [s for s in entry if norm_key(s) not in rm]


def _replace_spells(node, spells):
    if not isinstance(node, dict) or "spells" not in node:
        return
    cur = node["spells"]
    for level, reps in spells.items():
        entry = cur.get(level)
        if isinstance(entry, dict) and "spells" in entry:
            _replace_spells_list(entry["spells"], reps)
        elif isinstance(entry, list):
            _replace_spells_list(entry, reps)


def _apply_op(node, op):
    mode = op.get("mode")
    if mode in ("appendArr", "prependArr", "insertArr", "appendIfNotExistsArr",
                "replaceArr", "removeArr"):
        if isinstance(node, list):
            _apply_to_array(node, op)
        elif isinstance(node, dict) and mode == "replaceArr":
            items = copy.deepcopy(_as_list_of(op.get("items", [])))
            repl = op.get("replace")
            if not repl and items and isinstance(items[0], dict):
                node.clear()
                node.update(items[0])
    elif mode == "replaceTxt":
        _replace_text_in(node, op.get("replace", ""), op.get("with", ""), op.get("flags", ""))
    elif mode == "setProp":
        if isinstance(node, dict) and op.get("prop"):
            node[op["prop"]] = copy.deepcopy(op.get("value"))
    elif mode == "addSkills":
        _add_skills(node, op.get("skills", {}))
    elif mode == "addSpells":
        _add_spells(node, op.get("spells", {}))
    elif mode == "removeSpells":
        if isinstance(node, dict) and "spells" in node:
            _remove_spells(node["spells"], {k: v for k, v in op.items() if k != "mode"})
    elif mode == "replaceSpells":
        _replace_spells(node, op.get("spells", {}))


def apply_mod(root, field, ops):
    if field in ("_", "*"):
        nodes = list(_iter_nodes(root))
        for op in _as_list(ops):
            for node in nodes:
                _apply_op(node, op)
    else:
        targets = _resolve(root, field.split("."))
        for op in _as_list(ops):
            for node in targets:
                _apply_op(node, op)


def materialize_entity(ent, lookup, _seen=None):
    """Return a complete deep copy of `ent` with `_copy` inheritance applied.

    `lookup`: dict mapping normalized base name -> base entity (same category).
    """
    copy_info = ent.get("_copy")
    if not copy_info:
        return copy.deepcopy(ent)

    if _seen is None:
        _seen = set()
    base = lookup.get(norm_key(copy_info.get("name")))
    if base is None:
        raise MissingBaseError("%s copies missing base %r"
                               % (ent.get("name"), copy_info.get("name")))
    bkey = id(base)
    if bkey in _seen:
        raise CopyCycleError("cycle while materializing %r" % ent.get("name"))
    _seen.add(bkey)
    try:
        base_full = (materialize_entity(base, lookup, _seen)
                     if base.get("_copy") else copy.deepcopy(base))
    finally:
        _seen.discard(bkey)

    merged = copy.deepcopy(base_full)
    mod = copy_info.get("_mod")
    if mod:
        for field, ops in mod.items():
            apply_mod(merged, field, ops)
    for k, v in ent.items():
        if k.startswith("_"):
            continue
        merged[k] = copy.deepcopy(v)
    merged["derived_from"] = base_full.get("id")
    return merged


def materialize_category(entities):
    """Materialize every entity in a category list, in place."""
    lookup = {}
    for ent in entities:
        if isinstance(ent, dict) and ent.get("name"):
            lookup[norm_key(ent["name"])] = ent
    out = []
    for ent in entities:
        if not isinstance(ent, dict):
            out.append(ent)
            continue
        if ent.get("_copy"):
            ent = materialize_entity(ent, lookup)
        out.append(ent)
    return out
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_materialize.py -q`
Expected: all pass (`14 passed`).

---

### Task A2: `fuzzy.py` — second-pass reference resolution

**Files:**
- Create: `fuzzy.py`
- Test: `tests/test_fuzzy.py`

- [ ] **Step 1: Write the failing tests**

```python
import pytest

import fuzzy


def nindex(pairs):
    return {fuzzy.norm_nopunct(k): v for k, v in pairs}


def test_plain_entity_no_match_returns_none():
    assert fuzzy.fuzzy_resolve("spell", "Fireball", None, {}, {}) is None


def test_prefix_strip_matches():
    name_index = nindex([("Soulmonger", "adventure-entry-soulmonger-tftyp")])
    assert fuzzy.fuzzy_resolve("adventure", "the Soulmonger", None, name_index, {}) \
        == ("adventure-entry-soulmonger-tftyp", "name-index")


def test_suffix_strip_matches():
    name_index = nindex([("Chapter 3", "adventure-entry-chapter-3-dungrunglung-tftyp")])
    assert fuzzy.fuzzy_resolve("adventure", "Chapter 3 map", None, name_index, {}) \
        == ("adventure-entry-chapter-3-dungrunglung-tftyp", "name-index")


def test_parenthetical_strip_matches():
    name_index = nindex([("Fellow Students", "adventure-entry-fellow-students-scc")])
    assert fuzzy.fuzzy_resolve("adventure", "Fellow Students (Book)", None, name_index, {}) \
        == ("adventure-entry-fellow-students-scc", "name-index")


def test_nopunct_matches():
    name_index = nindex([("SCC-CK", "adventure-entry-scc-ck-scc")])
    assert fuzzy.fuzzy_resolve("adventure", "SCC CK", None, name_index, {}) \
        == ("adventure-entry-scc-ck-scc", "name-index")
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_fuzzy.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'fuzzy'`

- [ ] **Step 3: Implement `fuzzy.py`**

```python
"""Second-pass reference resolution: safe name-form heuristics.

Only accepts EXACT normalized-name hits against the index, so it can never
introduce a wrong link — it just tries more name forms than the main resolver.
"""

import re


def norm_nopunct(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def _candidates(name):
    low = (name or "").strip().lower()
    cands = [norm_nopunct(low)]
    for pfx in ("see ", "area ", "areas "):
        if low.startswith(pfx):
            cands.append(norm_nopunct(low[len(pfx):]))
    for sfx in (" table", " map", " diagram", " chart", " area", " areas"):
        if low.endswith(sfx):
            cands.append(norm_nopunct(low[:-len(sfx)]))
    base = (name or "").split("(")[0].strip()
    if base and norm_nopunct(base) not in cands:
        cands.append(norm_nopunct(base))
    return [c for c in cands if c]


def fuzzy_resolve(tag, name, source, name_index, collections):
    """Return (entity_id, rule) if an exact normalized name-form matches.

    `name_index`: {(collection, norm_nopunct_name): entity_id}
    `collections`: ordered list of collections to try for this tag.
    """
    if not collections or not name_index:
        return None
    for coll in collections:
        for cand in _candidates(name):
            eid = name_index.get((coll, cand))
            if eid:
                return eid, "name-index"
    return None
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_fuzzy.py -q`
Expected: all pass (`5 passed`).

---

### Task A3: Wire materialization + fuzzy pass into `structure_5etools.py`

**Files:**
- Modify: `structure_5etools.py`
- Test: `tests/test_structure_integration.py`

- [ ] **Step 1: Write the failing integration test**

```python
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import structure_5etools as s


def build(tmpdir, raw_entries):
    """Run the structure pipeline (ids + materialize + process) over raw
    entries and return the processed category list."""
    os.makedirs(os.path.join(tmpdir, "data_out", "raw"), exist_ok=True)
    for fname, data in raw_entries.items():
        with open(os.path.join(tmpdir, "data_out", "raw", fname), "w", encoding="utf-8") as f:
            json.dump(data, f)
    s.RAW = os.path.join(tmpdir, "data_out", "raw")
    s.OUT = os.path.join(tmpdir, "data_out")
    s.main()
    with open(os.path.join(tmpdir, "data_out", "bestiary.json"), encoding="utf-8") as f:
        return json.load(f)


def test_materialize_runs_in_pipeline(tmpdir):
    base = {"name": "Elder Dinosaur", "source": "PSX", "page": 1, "ac": 25,
            "action": [{"name": "Bite", "entries": ["Melee Weapon Attack: +19 to hit, one target."]}]}
    variant = {"name": "Elder Dinosaur (Ghalta, Primal Hunger)", "source": "PSX", "page": 2,
               "_copy": {"name": "Elder Dinosaur", "source": "PSX", "_mod": {
                   "action": {"mode": "appendArr", "items": [
                       {"name": "Multiattack", "entries": ["The elder dinosaur attacks."]}]}}}}
    ents = build(tmpdir, {"bestiary.json": [base, variant]})
    ghalta = [e for e in ents if "Ghalta" in e["name"]][0]
    assert ghalta["ac"] == 25
    assert [a["name"] for a in ghalta["action"]] == ["Bite", "Multiattack"]
    assert ghalta["derived_from"] == ents[0]["id"]
    # no _copy remains anywhere
    assert all("_copy" not in e for e in ents)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_structure_integration.py -q`
Expected: FAIL — Ghalta has no `ac`/`action` (not materialized yet).

- [ ] **Step 3: Modify `structure_5etools.py`**

Add imports at the top (after the existing imports):

```python
import fuzzy
import materialize
```

Add a `_build_name_index` helper and change `main()`:

```python
def build_name_index(by_name):
    """{(collection, norm_nopunct(name)): id} for fuzzy resolution."""
    return {("adventure_data", fuzzy.norm_nopunct(n)): eid
            for (coll, n), eid in by_name.items()}
```

Replace the body of `main()` between the `build_ids` line and the per-category
loop so the new flow is:

```python
    print("Assigning ids + building index...")
    by_name, by_name_source, _TOKEN_INDEX = build_ids(all_data)
    index = build_index(all_data)
    name_index = build_name_index(by_name)

    print("Materializing _copy inheritance...")
    materialized = 0
    for raw_file, _, _ in ID_CONFIG:
        all_data[raw_file] = materialize.materialize_category(all_data[raw_file])
        materialized += sum(1 for e in all_data[raw_file]
                            if isinstance(e, dict) and e.get("derived_from"))
    print("  %d entities materialized" % materialized)
```

Change the ref-resolution fallback in `resolve_ref` so an unresolved lookup
also consults the fuzzy pass:

```python
def resolve_ref(tag, name, source, by_name, by_name_source):
    ...existing body unchanged...
    return None
```

Add after `_lookup_candidates` (and after the `if tag == "item": ... return _token_resolve(...)` branch — i.e. the very end of `resolve_ref`) a fuzzy fallback. The simplest correct change: in `resolve_ref`, just before `return None`, add:

```python
    collections = []
    coll = TAG_COLLECTION.get(tag)
    if coll:
        collections.append(coll)
    collections.extend(TAG_FALLBACKS.get(tag, []))
    hit = fuzzy.fuzzy_resolve(tag, name, source, _NAME_INDEX, collections)
    if hit:
        return hit[0]
    return None
```

and define the module-global `_NAME_INDEX = None`, set in `main()` right after
`name_index = build_name_index(by_name)`:

```python
    global _NAME_INDEX
    _NAME_INDEX = name_index
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_structure_integration.py -q`
Expected: PASS.

- [ ] **Step 5: Run the full pipeline and spot-check materialization**

Run: `python3 structure_5etools.py`
Expected:
- prints `N entities materialized` with N > 1000
- `python3 -c "import json;d=json.load(open('data_out/bestiary.json'));g=[e for e in d if 'Ghalta' in e['name']][0];print(g['ac'], [a['name'] for a in g['action']][-1])"` shows `25 Multiattack`
- `python3 -c "import json;d=json.load(open('data_out/bestiary.json'));print(sum('_copy' in e for e in d))"` prints `0`

---

### Task A4: `db_writer.py` — schema, tag decoding, DB build

**Files:**
- Create: `db_writer.py`
- Test: `tests/test_db_writer.py`

- [ ] **Step 1: Write the failing tests**

```python
import json
import os
import sqlite3

import db_writer

FIX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")


def test_damage_map_full():
    expected = {"A": "acid", "B": "bludgeoning", "C": "cold", "F": "fire",
                "I": "poison", "L": "lightning", "N": "necrotic", "O": "force",
                "P": "piercing", "R": "radiant", "S": "slashing", "T": "thunder",
                "Y": "psychic"}
    assert db_writer.DAMAGE_MAP == expected


def test_misc_map_has_known_codes():
    assert db_writer.MISC_MAP["MW"] == "Has Weapon Attacks, Melee"
    assert db_writer.MISC_MAP["RCH"] == "Has Reach Attacks"


def test_extract_tags():
    ent = {"damageTags": ["F", "Y"], "miscTags": ["MW", "RCH"],
           "conditionInflict": ["grappled", "prone"],
           "savingThrowForced": ["constitution", "strength"],
           "actionTags": ["Multiattack", "Bite"]}
    condition_ids = {"grappled": "condition-grappled-phb", "prone": "condition-prone-phb"}
    tags = db_writer.extract_tags(ent, condition_ids, {})
    kinds = [t[0] for t in tags]
    assert kinds == ["damage_type", "damage_type", "misc", "misc",
                     "condition", "condition", "saving_throw", "saving_throw",
                     "action_tag", "action_tag"]
    fire = tags[0]
    assert fire == ("damage_type", "F", "Fire", None)
    grappled = tags[4]
    assert grappled[3] == "condition-grappled-phb"


def test_tag_id():
    assert db_writer.tag_id("damage_type", None, "Fire", None) == "damage-type-fire"
    assert db_writer.tag_id("condition", None, "Grappled", "condition-grappled-phb") == "condition-grappled-phb"
    assert db_writer.tag_id("misc", "MW", "Has Weapon Attacks, Melee", None) == "misc-mw"


def test_build_db_end_to_end(tmp_path):
    db_path = os.path.join(str(tmp_path), "5e.db")
    monsters = [
        {"id": "monster-ork-mm", "category": "bestiary", "name": "Ork", "source": "MM",
         "type": "humanoid", "cr": "1/2", "damageTags": ["S"],
         "conditionInflict": ["grappled"], "references": [
             {"type": "skill", "id": "skill-investigation-phb"},
             {"type": "spell", "name": "Fireball", "source": "PHB", "unresolved": True}]},
        {"id": "spell-fireball-phb", "category": "spells", "name": "Fireball",
         "source": "PHB", "school": "V", "level": 3},
        {"id": "skill-investigation-phb", "category": "skills", "name": "Investigation",
         "source": "PHB"},
    ]
    db_writer.build_db(db_path, monsters,
                       {"grappled": "condition-grappled-phb"}, {},
                       {"schemaVersion": "1.0.0", "datasetVersion": "test"})
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    assert conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0] == 3
    row = conn.execute("SELECT * FROM entities WHERE id='monster-ork-mm'").fetchone()
    assert row["cr"] == 0.5
    ref = conn.execute("SELECT * FROM references").fetchone()
    assert ref["from_id"] == "monster-ork-mm"
    assert ref["to_id"] == "skill-investigation-phb"
    unres = conn.execute("SELECT * FROM unresolved_refs").fetchone()
    assert unres["tag"] == "spell" and unres["name"] == "Fireball"
    tag = conn.execute("SELECT * FROM tags WHERE id='damage-type-slashing'").fetchone()
    assert tag["name"] == "Slashing"
    linked = conn.execute(
        "SELECT t.id FROM entity_tags et JOIN tags t ON et.tag_id=t.id "
        "WHERE et.entity_id='monster-ork-mm' AND t.kind='condition'").fetchone()
    assert linked["id"] == "condition-grappled-phb"
    school = conn.execute("SELECT school FROM entities WHERE id='spell-fireball-phb'").fetchone()
    assert school["school"] == "Evocation"
    fts = conn.execute(
        "SELECT e.id FROM entities_fts f JOIN entities e ON e.rowid=f.rowid "
        "WHERE entities_fts MATCH ?", ['"fireball"*']).fetchall()
    assert any(r["id"] == "spell-fireball-phb" for r in fts)
    conn.close()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_db_writer.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'db_writer'`

- [ ] **Step 3: Implement `db_writer.py`**

```python
"""Build data_out/5e.db from processed entities."""

import json
import sqlite3

DAMAGE_MAP = {
    "A": "acid", "B": "bludgeoning", "C": "cold", "F": "fire",
    "I": "poison", "L": "lightning", "N": "necrotic", "O": "force",
    "P": "piercing", "R": "radiant", "S": "slashing", "T": "thunder",
    "Y": "psychic",
}

MISC_MAP = {
    "AOE": "Has Areas of Effect", "CUR": "Inflicts Curse",
    "DIS": "Inflicts Disease", "HPR": "Has HP Reduction",
    "MW": "Has Weapon Attacks, Melee", "RW": "Has Weapon Attacks, Ranged",
    "MA": "Has Attacks, Melee", "RA": "Has Attacks, Ranged",
    "MLW": "Has Melee Weapons", "RNG": "Has Ranged Weapons",
    "RCH": "Has Reach Attacks", "THW": "Has Thrown Weapons",
}

SCHOOL_MAP = {
    "A": "Abjuration", "C": "Conjuration", "D": "Divination",
    "E": "Enchantment", "I": "Illusion", "N": "Necromancy",
    "T": "Transmutation", "V": "Evocation",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS entities (
  id TEXT PRIMARY KEY,
  category TEXT NOT NULL,
  name TEXT,
  sort_name TEXT,
  source TEXT,
  adventure_source TEXT,
  type TEXT,
  cr REAL,
  school TEXT,
  rarity TEXT,
  level INT,
  derived_from TEXT,
  payload TEXT NOT NULL
);
CREATE VIRTUAL TABLE IF NOT EXISTS entities_fts USING fts5(
  name, payload, tokenize='porter unicode61', content=''
);
CREATE TABLE IF NOT EXISTS references (
  from_id TEXT NOT NULL,
  to_id TEXT NOT NULL,
  ref_type TEXT NOT NULL,
  PRIMARY KEY (from_id, to_id, ref_type)
);
CREATE INDEX IF NOT EXISTS idx_refs_to ON references(to_id);
CREATE TABLE IF NOT EXISTS unresolved_refs (
  from_id TEXT NOT NULL,
  tag TEXT,
  name TEXT,
  source TEXT,
  reason TEXT,
  attempts INT
);
CREATE TABLE IF NOT EXISTS tags (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  code TEXT,
  name TEXT NOT NULL,
  target_entity_id TEXT
);
CREATE TABLE IF NOT EXISTS entity_tags (
  entity_id TEXT NOT NULL,
  tag_id TEXT NOT NULL,
  PRIMARY KEY (entity_id, tag_id)
);
CREATE INDEX IF NOT EXISTS idx_entity_tags_tag ON entity_tags(tag_id);
"""


def tag_id(kind, code, name, target_entity_id):
    if target_entity_id:
        return target_entity_id
    if kind == "damage_type":
        return "damage-type-" + name.lower().replace(" ", "-")
    if kind == "saving_throw":
        return "saving-throw-" + name.lower()
    if kind == "action_tag":
        return "action-tag-" + name.lower().replace(" ", "-")
    if kind == "misc":
        return "misc-" + (code or "x").lower()
    if kind in ("condition", "skill"):
        return "tag-" + kind + "-" + name.lower().replace(" ", "-")
    return "tag-" + kind + "-" + name.lower().replace(" ", "-")


def extract_tags(ent, condition_ids, skill_ids):
    out = []
    for code in ent.get("damageTags") or []:
        name = DAMAGE_MAP.get(code)
        if name:
            out.append(("damage_type", code, name, None))
    for code in ent.get("miscTags") or []:
        out.append(("misc", code, MISC_MAP.get(code, code), None))
    for cname in ent.get("conditionInflict") or []:
        eid = condition_ids.get(cname)
        out.append(("condition", None, cname.title(), eid))
    for ab in ent.get("savingThrowForced") or []:
        out.append(("saving_throw", None, ab.title(), None))
    for aname in ent.get("actionTags") or []:
        out.append(("action_tag", None, aname, None))
    return out


def _parse_cr(value):
    if value is None:
        return None
    if isinstance(value, dict):
        value = value.get("cr")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        if "/" in value:
            try:
                num, _, den = value.partition("/")
                return float(num) / float(den)
            except (ValueError, ZeroDivisionError):
                return None
        try:
            return float(value)
        except ValueError:
            return None
    return None


def build_db(db_path, all_entities, condition_ids, skill_ids, meta):
    conn = sqlite3.connect(db_path)
    conn.execute("BEGIN")
    for stmt in SCHEMA.split(";"):
        if stmt.strip():
            conn.execute(stmt)

    for key, value in meta.items():
        conn.execute("INSERT INTO meta (key, value) VALUES (?, ?)",
                     (key, json.dumps(value) if not isinstance(value, str) else value))

    for ent in all_entities:
        if not isinstance(ent, dict) or not ent.get("id"):
            continue
        category = ent.get("category", "")
        cr = _parse_cr(ent.get("cr")) if category == "bestiary" else None
        school = SCHOOL_MAP.get(ent.get("school")) if category == "spells" else None
        rarity = ent.get("rarity") if category == "items" else None
        level = ent.get("level") if category == "spells" else None
        payload = json.dumps(ent, ensure_ascii=False, separators=(",", ":"))
        conn.execute(
            "INSERT INTO entities (id, category, name, sort_name, source, "
            "adventure_source, type, cr, school, rarity, level, derived_from, payload) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (ent["id"], category, ent.get("name"), (ent.get("name") or "").lower(),
             ent.get("source"), ent.get("adventureSource"), ent.get("type"),
             cr, school, rarity, level, ent.get("derived_from"), payload))

    for ent in all_entities:
        if not isinstance(ent, dict) or not ent.get("id"):
            continue
        for r in ent.get("references", []):
            if r.get("id"):
                conn.execute("INSERT OR REPLACE INTO references (from_id, to_id, ref_type) VALUES (?, ?, ?)",
                             (ent["id"], r["id"], r.get("type") or ""))
            elif r.get("unresolved"):
                conn.execute(
                    "INSERT INTO unresolved_refs (from_id, tag, name, source, reason, attempts) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (ent["id"], r.get("type"), r.get("name"), r.get("source"),
                     r.get("reason", "no matching entity"), 1))
        for kind, code, name, target in extract_tags(ent, condition_ids, skill_ids):
            tid = tag_id(kind, code, name, target)
            conn.execute("INSERT OR IGNORE INTO tags (id, kind, code, name, target_entity_id) "
                         "VALUES (?, ?, ?, ?, ?)", (tid, kind, code, name, target))
            conn.execute("INSERT OR IGNORE INTO entity_tags (entity_id, tag_id) VALUES (?, ?)",
                         (ent["id"], tid))

    for ent in all_entities:
        if not isinstance(ent, dict) or not ent.get("id"):
            continue
        conn.execute("INSERT INTO entities_fts (rowid, name, payload) VALUES (?, ?, ?)",
                     (ent["rowid"], ent.get("name") or "", json.dumps(ent, ensure_ascii=False)))

    conn.commit()
    conn.close()
```

> **Note:** `build_db` uses `ent["rowid"]` for FTS. The caller (structure) must
> attach the entities.rowid. Because `all_entities` is a flat list, the caller
> inserts the id-to-rowid mapping by inserting a temporary sentinel. To avoid a
> second pass, restructure the FTS step in the plan's Task A5 (see there): the
> caller passes `rowid` on each entity via a pre-query. Implemented as follows
> in Task A5's wiring so `build_db` is called AFTER rows exist. In this task,
> keep the loop but skip FTS when `"rowid" not in ent` — change the final loop
> to:

```python
    for ent in all_entities:
        if isinstance(ent, dict) and ent.get("id") and "rowid" in ent:
            conn.execute("INSERT INTO entities_fts (rowid, name, payload) VALUES (?, ?, ?)",
                         (ent["rowid"], ent.get("name") or "", json.dumps(ent, ensure_ascii=False)))
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_db_writer.py -q`
Expected: PASS.

> **Consistency note:** The FTS insert in `build_db` only fires when the caller
> supplies `rowid` on each entity (Task A5 does this). The test above passes
> `rowid` in `test_build_db_end_to_end` via an inserted column — add
> `"rowid": n` (1,2,3) to the three fixture dicts if the FTS assertion is the
> only failure. See Task A5 Step 3 for the canonical wiring.

---

### Task A5: Wire DB building into `structure_5etools.py` (+ adventure section refs)

**Files:**
- Modify: `structure_5etools.py`
- Test: `tests/test_structure_integration.py` (extend)

- [ ] **Step 1: Extend the failing integration test**

Append to `tests/test_structure_integration.py`:

```python
import sqlite3


def test_db_is_built_and_valid(tmpdir):
    base = {"name": "Orc", "source": "MM", "page": 1, "cr": "1/2",
            "damageTags": ["S"], "conditionInflict": ["grappled"],
            "action": [{"name": "Greataxe", "entries": ["Melee Weapon Attack: +5 to hit, one target. Hit: 9 (1d12 + 3) slashing damage."]}]}
    spell = {"name": "Fireball", "source": "PHB", "level": 3, "school": "V"}
    skill = {"name": "Investigation", "source": "PHB"}
    ents = build(tmpdir, {"bestiary.json": [base], "spells.json": [spell],
                          "skills.json": [skill]})
    db_path = os.path.join(tmpdir, "data_out", "5e.db")
    assert os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    assert conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0] == 3
    assert conn.execute("SELECT COUNT(*) FROM references").fetchone()[0] >= 1
    assert conn.execute("SELECT COUNT(*) FROM tags WHERE kind='damage_type'").fetchone()[0] >= 1
    conn.close()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_structure_integration.py -q`
Expected: FAIL — `5e.db` not created.

- [ ] **Step 3: Modify `structure_5etools.py`**

Add `import db_writer, validate_db` to the imports.

Add a function to attribute refs to adventure sections (walks the processed
adventure tree; the deepest id-bearing dict owns each ref token found in its
subtree):

```python
REF_TOKEN_RE = re.compile(r"\{\{ref:([^{}:]+|[a-z]+:[^}]+)\}\}")


def collect_section_refs(root):
    """Attribute {{ref:...}} tokens to the nearest id-bearing section.
    Returns dict section_id -> list of ref dicts, and injects a deduplicated
    `references` key into each section dict (JSON output keeps it too)."""
    by_id = {}

    def walk(v, owner):
        if isinstance(v, dict):
            if isinstance(v.get("id"), str) and v["id"].startswith("adventure-entry-"):
                owner = v["id"]
            refs = []
            for k, val in v.items():
                if isinstance(val, str):
                    for m in REF_TOKEN_RE.finditer(val):
                        tok = m.group(1)
                        if ":" in tok:
                            tag, _, name = tok.partition(":")
                            refs.append({"type": tag, "name": name, "unresolved": True})
                        else:
                            refs.append({"type": "ref", "id": tok})
                elif isinstance(val, (dict, list)):
                    walk(val, owner)
            if owner and refs:
                by_id.setdefault(owner, []).extend(refs)
        elif isinstance(v, list):
            for x in v:
                walk(x, owner)

    walk(root, None)
    dedup = {}
    for sid, refs in by_id.items():
        seen = set()
        out = []
        for r in refs:
            key = (r.get("type"), r.get("id") or r.get("name"))
            if key not in seen:
                seen.add(key)
                out.append(r)
        dedup[sid] = out

    def inject(v):
        if isinstance(v, dict):
            if isinstance(v.get("id"), str) and v["id"] in dedup and "references" not in v:
                v["references"] = dedup[v["id"]]
            for x in v.values():
                inject(x)
        elif isinstance(v, list):
            for x in v:
                inject(x)

    inject(root)
    return dedup
```

In `main()`, replace the adventure_data processing block:

```python
    print("Processing adventure_data...")
    refs = []
    processed_adventure = process_content(all_data["adventure_data.json"], by_name, by_name_source, refs)
    for r in refs:
        if "id" in r:
            stats["resolved"] += 1
        elif r.get("unresolved"):
            stats["unresolved"] += 1
    section_refs = collect_section_refs(processed_adventure)
    print("  %d adventure sections with references" % len(section_refs))
    with open(os.path.join(OUT, "adventure_data.json"), "w", encoding="utf-8") as f:
        json.dump(processed_adventure, f, ensure_ascii=False, indent=1)
```

At the very end of `main()`, after `metadata.json` is written, add:

```python
    print("Building 5e.db...")
    all_entities = []
    for raw_file, _, collection in ID_CONFIG:
        for ent in all_data[raw_file]:
            if isinstance(ent, dict) and ent.get("id"):
                ent["category"] = collection
                all_entities.append(ent)
    for sid, rlist in section_refs.items():
        all_entities.append({"id": sid, "category": "adventure_data",
                             "name": sid, "source": None,
                             "references": rlist})

    condition_ids = {}
    for ent in all_data["conditionsdiseases.json"]:
        if isinstance(ent, dict) and ent.get("id") and ent.get("name"):
            condition_ids[ent["name"]] = ent["id"]
    skill_ids = {}
    for ent in all_data["skills.json"]:
        if isinstance(ent, dict) and ent.get("id") and ent.get("name"):
            skill_ids[ent["name"]] = ent["id"]

    conn = sqlite3.connect(os.path.join(OUT, "5e.db"))
    rowids = {}
    for ent in all_entities:
        rowids[ent["id"]] = conn.execute(
            "SELECT rowid FROM entities WHERE id=?", (ent["id"],)).fetchone()[0]
    # placeholder to satisfy build_db signature ordering; build_db re-creates schema
    conn.close()

    db_writer.build_db(os.path.join(OUT, "5e.db"), all_entities, condition_ids,
                       skill_ids, {
                           "schemaVersion": SCHEMA_VERSION,
                           "datasetVersion": DATASET_VERSION,
                           "generatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                           "source": {
                               "repo": SOURCE_REPO, "commit": SOURCE_COMMIT,
                               "commitDate": SOURCE_COMMIT_DATE,
                               "version": SOURCE_VERSION,
                               "editions": ["5e (2014)", "5e (2024)"],
                           },
                           "counts": counts,
                           "stats": stats,
                       })

    print("Validating 5e.db...")
    problems = validate_db.validate(os.path.join(OUT, "5e.db"))
    if problems:
        for p in problems:
            print("  !! " + p)
        sys.exit(1)
    print("  5e.db OK: %d entities, %d resolved refs, %d unresolved"
          % (len(all_entities), stats["resolved"], stats["unresolved"]))
    print("Done -> %s" % OUT)
```

> **Wiring fix:** `db_writer.build_db` needs `rowid` on each entity for FTS.
> `build_db` inserts entities first, so `rowid` is unknown before the call. To
> make this work cleanly, change `db_writer.build_db` so it performs TWO passes
> internally: pass 1 inserts entity rows (collecting their rowids), pass 2
> inserts FTS rows from the same list. Replace the final FTS loop in
> `db_writer.py` with this (inside `build_db`, after the reference/tag inserts):

```python
    rowid_of = {}
    for ent in all_entities:
        if isinstance(ent, dict) and ent.get("id"):
            rowid_of[ent["id"]] = conn.execute(
                "SELECT rowid FROM entities WHERE id=?", (ent["id"],)).fetchone()[0]
    for ent in all_entities:
        if isinstance(ent, dict) and ent.get("id"):
            conn.execute("INSERT INTO entities_fts (rowid, name, payload) VALUES (?, ?, ?)",
                         (rowid_of[ent["id"]], ent.get("name") or "",
                          json.dumps(ent, ensure_ascii=False, separators=(",", ":"))))
```

and remove the `"rowid" in ent` guard from Task A4's step-3 note (the rowid is
now computed internally, so the fixture test in Task A4 no longer needs `rowid`
keys — update `tests/test_db_writer.py` to drop the `"rowid": n` fields).

Also `collect_section_refs` needs the refs of adventure sections available in
`main()` for the JSON too — it already injects `references` into the sections.

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_db_writer.py tests/test_structure_integration.py -q`
Expected: all pass.

- [ ] **Step 5: Run the full pipeline**

Run: `python3 structure_5etools.py`
Expected: prints `Building 5e.db...`, `Validating 5e.db...`, `5e.db OK: N entities...` with N ≥ 50,000. If validation reports problems, they are printed with `!!` and the process exits 1 — fix per the message.

---

### Task A6: `validate_db.py`

**Files:**
- Create: `validate_db.py`
- Test: `tests/test_validate_db.py`

- [ ] **Step 1: Write the failing tests**

```python
import os
import sqlite3

import db_writer
import validate_db


def make_db(path):
    monsters = [
        {"id": "monster-a-mm", "category": "bestiary", "name": "A", "source": "MM",
         "references": [{"type": "skill", "id": "skill-x-phb"}]},
        {"id": "skill-x-phb", "category": "skills", "name": "X", "source": "PHB"},
    ]
    db_writer.build_db(path, monsters, {}, {},
                       {"counts": {"bestiary.json": 1, "skills.json": 1}, "stats": {}})
    return monsters


def test_valid_db_no_problems(tmp_path):
    path = os.path.join(str(tmp_path), "5e.db")
    make_db(path)
    assert validate_db.validate(path) == []


def test_dangling_reference_detected(tmp_path):
    path = os.path.join(str(tmp_path), "5e.db")
    monsters = [
        {"id": "monster-a-mm", "category": "bestiary", "name": "A", "source": "MM",
         "references": [{"type": "skill", "id": "skill-missing-phb"}]},
    ]
    db_writer.build_db(path, monsters, {}, {}, {"counts": {"bestiary.json": 1}, "stats": {}})
    problems = validate_db.validate(path)
    assert any("skill-missing-phb" in p for p in problems)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_validate_db.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'validate_db'`

- [ ] **Step 3: Implement `validate_db.py`**

```python
"""Invariant checks against data_out/5e.db. Returns a list of problem strings."""

import json
import sqlite3


def _row(conn, sql, args=()):
    return conn.execute(sql, args).fetchone()


def validate(db_path):
    problems = []
    conn = sqlite3.connect(db_path)

    total = _row(conn, "SELECT COUNT(*) FROM entities")[0]
    distinct = _row(conn, "SELECT COUNT(DISTINCT id) FROM entities")[0]
    if total != distinct:
        problems.append("entity ids not unique: %d rows, %d distinct" % (total, distinct))

    bad_refs = conn.execute(
        "SELECT r.from_id, r.to_id FROM references r "
        "LEFT JOIN entities a ON a.id = r.from_id "
        "LEFT JOIN entities b ON b.id = r.to_id "
        "WHERE a.id IS NULL OR b.id IS NULL").fetchall()
    if bad_refs:
        problems.append("dangling references: %d (e.g. %s)"
                        % (len(bad_refs), bad_refs[0]))

    bad_tags = conn.execute(
        "SELECT et.entity_id, et.tag_id FROM entity_tags et "
        "LEFT JOIN entities e ON e.id = et.entity_id "
        "LEFT JOIN tags t ON t.id = et.tag_id "
        "WHERE e.id IS NULL OR t.id IS NULL").fetchall()
    if bad_tags:
        problems.append("dangling entity_tags: %d (e.g. %s)"
                        % (len(bad_tags), bad_tags[0]))

    dup_tags = conn.execute(
        "SELECT entity_id, tag_id FROM entity_tags GROUP BY entity_id, tag_id "
        "HAVING COUNT(*) > 1").fetchall()
    if dup_tags:
        problems.append("duplicate entity_tags rows: %d" % len(dup_tags))

    counts = json.loads(_row(conn, "SELECT value FROM meta WHERE key='counts'")[0])
    for fname, expected in counts.items():
        category = fname[:-len(".json")]
        actual = _row(conn, "SELECT COUNT(*) FROM entities WHERE category=?", (category,))[0]
        if actual != expected:
            problems.append("count mismatch %s: expected %d, got %d"
                            % (category, expected, actual))

    markup = conn.execute(
        "SELECT id FROM entities WHERE payload LIKE '%{@%' OR payload LIKE '%[[/%' "
        "LIMIT 5").fetchall()
    if markup:
        problems.append("leftover markup in payloads: %d (e.g. %s)"
                        % (len(markup), markup[0]))

    copies = conn.execute("SELECT id FROM entities WHERE payload LIKE '%\"_copy\"%' LIMIT 5").fetchall()
    if copies:
        problems.append("unmaterialized _copy remaining: %d (e.g. %s)"
                        % (len(copies), copies[0]))

    fireball = conn.execute(
        "SELECT e.id FROM entities_fts f JOIN entities e ON e.rowid = f.rowid "
        "WHERE entities_fts MATCH ? LIMIT 1", ['"fireball"*']).fetchone()
    if not fireball:
        problems.append("fts: 'fireball' returned no results")

    dragons = conn.execute(
        "SELECT COUNT(*) FROM entities_fts f JOIN entities e ON e.rowid = f.rowid "
        "WHERE entities_fts MATCH ? AND e.category = 'bestiary'",
        ['"dragon"*']).fetchone()[0]
    if dragons == 0:
        problems.append("fts: 'dragon' returned no bestiary results")

    conn.close()
    return problems
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_validate_db.py -q`
Expected: all pass.

- [ ] **Step 5: Full rebuild + validate**

Run: `python3 structure_5etools.py`
Expected: `5e.db OK` printed (validation runs inside main). Then run the
standalone validator to be safe:
`python3 -c "import validate_db; p=validate_db.validate('data_out/5e.db'); print(p or 'CLEAN')"`
Expected: `CLEAN`.

---

### Task A7: `rebuild.sh`

**Files:**
- Create: `rebuild.sh`

- [ ] **Step 1: Create `rebuild.sh`**

```bash
#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 extract_5etools.py
python3 structure_5etools.py
python3 -c "import validate_db; p=validate_db.validate('data_out/5e.db'); print('\n'.join(p) if p else 'VALIDATION CLEAN')"
```

- [ ] **Step 2: Make executable + run**

Run: `chmod +x rebuild.sh && ./rebuild.sh`
Expected: pipeline runs, ends with `VALIDATION CLEAN`.

---

## PHASE B — BACKEND

### Task B1: Backend scaffold + venv

**Files:**
- Create: `app/backend/requirements.txt`
- Create: `app/backend/run.sh`

- [ ] **Step 1: Create `requirements.txt`**

```
fastapi==0.141.1
uvicorn==0.34.0
httpx==0.28.1
pytest==8.3.4
```

- [ ] **Step 2: Create `run.sh`**

```bash
#!/usr/bin/env bash
cd "$(dirname "$0")"
if [ ! -d .venv ]; then python3 -m venv .venv; fi
. .venv/bin/activate
pip install -q -r requirements.txt
echo "Open http://localhost:8000/"
exec uvicorn main:app --reload --port 8000
```

- [ ] **Step 3: Create venv and verify deps**

Run: `cd app/backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
Expected: installs cleanly; `app/backend/.venv` exists.

---

### Task B2: Backend core — meta, categories, entity, refs, unresolved

**Files:**
- Create: `app/backend/main.py`
- Test: `app/backend/tests/test_api.py` (extended through tasks B2–B5)

- [ ] **Step 1: Write the failing tests**

Create `app/backend/tests/test_api.py`:

```python
import json
import os
import sqlite3

import pytest
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main as app_mod

FIX = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))), "tests", "fixtures")


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_path = os.path.join(str(tmp_path), "5e.db")
    with open(os.path.join(FIX, "mini.json"), encoding="utf-8") as f:
        entities = json.load(f)
    import db_writer
    db_writer.build_db(db_path, entities, {"grappled": "condition-grappled-phb"}, {},
                       {"schemaVersion": "1.0.0", "datasetVersion": "test",
                        "counts": {"bestiary.json": 2, "spells.json": 1,
                                   "skills.json": 1},
                        "stats": {"resolved": 1, "unresolved": 1, "attacks": 1}})
    monkeypatch.setattr(app_mod, "DB_PATH", db_path)
    client = TestClient(app_mod.app)
    yield client
    client.close()


def test_meta(client):
    r = client.get("/api/meta")
    assert r.status_code == 200
    assert r.json()["datasetVersion"] == "test"
    assert r.json()["counts"]["bestiary.json"] == 2


def test_categories(client):
    r = client.get("/api/categories")
    assert r.status_code == 200
    cats = {c["category"]: c["count"] for c in r.json()}
    assert cats["bestiary"] == 2


def test_entity_ok(client):
    r = client.get("/api/entities/monster-ork-mm")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == "monster-ork-mm"
    assert body["name"] == "Ork"
    assert body["payload"]["cr"] == "1/2"


def test_entity_404(client):
    assert client.get("/api/entities/nope").status_code == 404


def test_references_out_and_in(client):
    out = client.get("/api/entities/monster-ork-mm/references?direction=out")
    assert out.status_code == 200
    assert any(x["id"] == "skill-investigation-phb" for x in out.json())
    inn = client.get("/api/entities/skill-investigation-phb/references?direction=in")
    assert any(x["id"] == "monster-ork-mm" for x in inn.json())


def test_unresolved(client):
    r = client.get("/api/entities/monster-ork-mm/unresolved")
    assert r.status_code == 200
    assert any(x["name"] == "Fireball" for x in r.json())
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `app/backend/.venv/bin/python -m pytest app/backend/tests/test_api.py -q`
Expected: FAIL — `ModuleNotFoundError: No module named 'fastapi'` in system python, or `No module named 'main'` once venv is used.

- [ ] **Step 3: Create the fixture `tests/fixtures/mini.json`**

```json
[
  {"id": "monster-ork-mm", "category": "bestiary", "name": "Ork", "source": "MM",
   "type": "humanoid", "cr": "1/2", "damageTags": ["S"],
   "conditionInflict": ["grappled"],
   "references": [
     {"type": "skill", "id": "skill-investigation-phb"},
     {"type": "spell", "name": "Fireball", "source": "PHB", "unresolved": true}]},
  {"id": "monster-dragon-mm", "category": "bestiary", "name": "Dragon", "source": "MM",
   "cr": "17", "damageTags": ["F"],
   "references": [{"type": "skill", "id": "skill-investigation-phb"}]},
  {"id": "spell-fireball-phb", "category": "spells", "name": "Fireball", "source": "PHB",
   "school": "V", "level": 3, "payload_note": "fixture"},
  {"id": "skill-investigation-phb", "category": "skills", "name": "Investigation",
   "source": "PHB"}
]
```

- [ ] **Step 4: Implement `app/backend/main.py` (core endpoints)**

```python
"""FastAPI backend over data_out/5e.db. Also serves the frontend at /."""

import json
import os
import sqlite3

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE, "data_out", "5e.db"))
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

app = FastAPI(title="5e Dataset API")


def connect():
    try:
        conn = sqlite3.connect("file:%s?mode=ro" % DB_PATH, uri=True)
    except sqlite3.Error as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    conn.row_factory = sqlite3.Row
    return conn


@app.exception_handler(sqlite3.Error)
def _sqlite_error(request, exc):
    return JSONResponse(status_code=503, content={"detail": "database error"})


@app.get("/api/meta")
def get_meta():
    with connect() as conn:
        rows = conn.execute("SELECT key, value FROM meta").fetchall()
    out = {}
    for row in rows:
        try:
            out[row["key"]] = json.loads(row["value"])
        except (ValueError, TypeError):
            out[row["key"]] = row["value"]
    return out


@app.get("/api/categories")
def get_categories():
    with connect() as conn:
        rows = conn.execute(
            "SELECT category, COUNT(*) AS count FROM entities "
            "GROUP BY category ORDER BY category").fetchall()
    return [{"category": r["category"], "count": r["count"]} for r in rows]


@app.get("/api/entities/{entity_id}")
def get_entity(entity_id: str):
    with connect() as conn:
        row = conn.execute("SELECT * FROM entities WHERE id=?", (entity_id,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="entity not found")
        tags = conn.execute(
            "SELECT t.id, t.kind, t.code, t.name, t.target_entity_id "
            "FROM entity_tags et JOIN tags t ON et.tag_id=t.id "
            "WHERE et.entity_id=? ORDER BY t.kind, t.name", (entity_id,)).fetchall()
        out_refs = conn.execute(
            "SELECT COUNT(*) AS n FROM references WHERE from_id=?", (entity_id,)).fetchone()["n"]
        in_refs = conn.execute(
            "SELECT COUNT(*) AS n FROM references WHERE to_id=?", (entity_id,)).fetchone()["n"]
        unresolved = conn.execute(
            "SELECT COUNT(*) AS n FROM unresolved_refs WHERE from_id=?", (entity_id,)).fetchone()["n"]
    return {
        "id": row["id"], "category": row["category"], "name": row["name"],
        "source": row["source"], "type": row["type"],
        "derived_from": row["derived_from"],
        "tags": [{"id": t["id"], "kind": t["kind"], "code": t["code"],
                  "name": t["name"], "target_entity_id": t["target_entity_id"]} for t in tags],
        "references_out": out_refs, "references_in": in_refs,
        "unresolved": unresolved,
        "payload": json.loads(row["payload"]),
    }


@app.get("/api/entities/{entity_id}/references")
def get_references(entity_id: str, direction: str = Query("out", pattern="^(in|out)$")):
    with connect() as conn:
        if conn.execute("SELECT 1 FROM entities WHERE id=?", (entity_id,)).fetchone() is None:
            raise HTTPException(status_code=404, detail="entity not found")
        if direction == "out":
            rows = conn.execute(
                "SELECT r.to_id AS id, r.ref_type, e.name, e.category "
                "FROM references r JOIN entities e ON e.id=r.to_id "
                "WHERE r.from_id=? ORDER BY e.category, e.name", (entity_id,)).fetchall()
        else:
            rows = conn.execute(
                "SELECT r.from_id AS id, r.ref_type, e.name, e.category "
                "FROM references r JOIN entities e ON e.id=r.from_id "
                "WHERE r.to_id=? ORDER BY e.category, e.name", (entity_id,)).fetchall()
    return [{"id": r["id"], "ref_type": r["ref_type"],
             "name": r["name"], "category": r["category"]} for r in rows]


@app.get("/api/entities/{entity_id}/unresolved")
def get_unresolved(entity_id: str):
    with connect() as conn:
        if conn.execute("SELECT 1 FROM entities WHERE id=?", (entity_id,)).fetchone() is None:
            raise HTTPException(status_code=404, detail="entity not found")
        rows = conn.execute(
            "SELECT tag, name, source, reason FROM unresolved_refs "
            "WHERE from_id=?", (entity_id,)).fetchall()
    return [{"tag": r["tag"], "name": r["name"], "source": r["source"],
             "reason": r["reason"]} for r in rows]
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `app/backend/.venv/bin/python -m pytest app/backend/tests/test_api.py -q`
Expected: all pass.

---

### Task B3: Search endpoint (FTS + facet filters)

**Files:**
- Modify: `app/backend/main.py`
- Test: `app/backend/tests/test_api.py`

- [ ] **Step 1: Append the failing tests**

```python
def test_search_fireball(client):
    r = client.get("/api/search", params={"q": "fireball"})
    assert r.status_code == 200
    body = r.json()
    assert body["total"] >= 1
    assert any(x["id"] == "spell-fireball-phb" for x in body["results"])


def test_search_category_filter(client):
    r = client.get("/api/search", params={"q": "dragon", "category": "bestiary"})
    ids = [x["id"] for x in r.json()["results"]]
    assert "monster-dragon-mm" in ids


def test_search_damage_type_filter(client):
    r = client.get("/api/search", params={"damage_type": "slashing"})
    assert any(x["id"] == "monster-ork-mm" for x in r.json()["results"])


def test_search_condition_filter(client):
    r = client.get("/api/search", params={"condition": "condition-grappled-phb"})
    assert any(x["id"] == "monster-ork-mm" for x in r.json()["results"])


def test_search_no_q_returns_all(client):
    r = client.get("/api/search", params={"category": "skills"})
    assert r.json()["total"] == 1


def test_search_bad_param_400(client):
    assert client.get("/api/search", params={"cr_min": "abc"}).status_code == 400
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `app/backend/.venv/bin/python -m pytest app/backend/tests/test_api.py -q`
Expected: FAIL on the new tests (endpoint missing → 404).

- [ ] **Step 3: Implement the search endpoint**

Append to `app/backend/main.py`:

```python
from fastapi import HTTPException, Query
from pydantic import BaseModel


def _fts_query(q):
    import re as _re
    tokens = [t for t in _re.split(r"[^0-9a-zA-Z]+", q) if t]
    return " ".join('"%s"*' % t for t in tokens)


def _tag_exists(conn, tag_id):
    return conn.execute("SELECT 1 FROM tags WHERE id=?", (tag_id,)).fetchone() is not None


@app.get("/api/search")
def search(
    q: str = Query(""),
    category: str | None = Query(None),
    source: str | None = Query(None),
    damage_type: str | None = Query(None),
    condition: str | None = Query(None),
    save: str | None = Query(None),
    school: str | None = Query(None),
    rarity: str | None = Query(None),
    cr_min: float | None = Query(None),
    cr_max: float | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    where = []
    args = []
    tag_filters = [("damage_type", damage_type), ("condition", condition), ("saving_throw", save)]
    for kind, value in tag_filters:
        if value:
            where.append(
                "EXISTS (SELECT 1 FROM entity_tags et2 JOIN tags t2 ON et2.tag_id=t2.id "
                "WHERE et2.entity_id=e.id AND t2.kind=? AND t2.id=?)")
            args += [kind, value]
    if category:
        where.append("e.category = ?")
        args.append(category)
    if source:
        where.append("e.source = ?")
        args.append(source)
    if school:
        where.append("e.school = ?")
        args.append(school)
    if rarity:
        where.append("e.rarity = ?")
        args.append(rarity)
    if cr_min is not None:
        where.append("e.cr >= ?")
        args.append(cr_min)
    if cr_max is not None:
        where.append("e.cr <= ?")
        args.append(cr_max)

    fts = _fts_query(q) if q else None
    if fts:
        where.append("e.id IN (SELECT e2.id FROM entities_fts f2 "
                     "JOIN entities e2 ON e2.rowid=f2.rowid WHERE entities_fts MATCH ?)")
        args.insert(0, fts)

    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    count_sql = "SELECT COUNT(*) FROM entities e" + where_sql
    sel_sql = ("SELECT e.id, e.name, e.category, e.source, e.cr, e.school "
               "FROM entities e" + where_sql +
               " ORDER BY e.sort_name LIMIT ? OFFSET ?")

    with connect() as conn:
        total = conn.execute(count_sql, args).fetchone()[0]
        rows = conn.execute(sel_sql, args + [limit, offset]).fetchall()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "results": [dict(r) for r in rows],
    }
```

> Note: the unused `BaseModel` import can be dropped; keep imports minimal.

- [ ] **Step 4: Run tests to verify they pass**

Run: `app/backend/.venv/bin/python -m pytest app/backend/tests/test_api.py -q`
Expected: all pass.

---

### Task B4: Filters endpoint

**Files:**
- Modify: `app/backend/main.py`
- Test: `app/backend/tests/test_api.py`

- [ ] **Step 1: Append the failing test**

```python
def test_filters(client):
    r = client.get("/api/filters")
    assert r.status_code == 200
    body = r.json()
    assert any(t["name"] == "Slashing" for t in body["damage_types"])
    assert any(t["id"] == "condition-grappled-phb" for t in body["conditions"])
    assert any(s["school"] == "Evocation" for s in body["schools"])
    assert body["cr"]["min"] == 0.5 and body["cr"]["max"] == 17.0
```

- [ ] **Step 2: Run tests to verify it fails**

Run: `app/backend/.venv/bin/python -m pytest app/backend/tests/test_api.py::test_filters -q`
Expected: FAIL.

- [ ] **Step 3: Implement the filters endpoint**

Append to `app/backend/main.py`:

```python
@app.get("/api/filters")
def get_filters():
    with connect() as conn:
        tags = conn.execute(
            "SELECT id, kind, name, code FROM tags ORDER BY kind, name").fetchall()
        schools = conn.execute(
            "SELECT DISTINCT school FROM entities WHERE school IS NOT NULL "
            "ORDER BY school").fetchall()
        rarities = conn.execute(
            "SELECT DISTINCT rarity FROM entities WHERE rarity IS NOT NULL "
            "ORDER BY rarity").fetchall()
        sources = conn.execute(
            "SELECT source, COUNT(*) AS count FROM entities "
            "WHERE source IS NOT NULL GROUP BY source ORDER BY source").fetchall()
        cr = conn.execute(
            "SELECT MIN(cr) AS mn, MAX(cr) AS mx FROM entities "
            "WHERE category='bestiary'").fetchone()
        categories = conn.execute(
            "SELECT category, COUNT(*) AS count FROM entities "
            "GROUP BY category ORDER BY category").fetchall()
    return {
        "categories": [{"category": c["category"], "count": c["count"]} for c in categories],
        "sources": [{"source": s["source"], "count": s["count"]} for s in sources],
        "damage_types": [{"id": t["id"], "name": t["name"]}
                         for t in tags if t["kind"] == "damage_type"],
        "conditions": [{"id": t["id"], "name": t["name"]}
                       for t in tags if t["kind"] == "condition"],
        "saves": [{"id": t["id"], "name": t["name"]}
                  for t in tags if t["kind"] == "saving_throw"],
        "misc_tags": [{"id": t["id"], "name": t["name"]}
                      for t in tags if t["kind"] == "misc"],
        "schools": [s["school"] for s in schools],
        "rarities": [r["rarity"] for r in rarities],
        "cr": {"min": cr["mn"], "max": cr["mx"]},
    }
```

- [ ] **Step 4: Run tests to verify it passes**

Run: `app/backend/.venv/bin/python -m pytest app/backend/tests/test_api.py -q`
Expected: all pass.

---

### Task B5: Analytics endpoints + static mount + run

**Files:**
- Modify: `app/backend/main.py`
- Test: `app/backend/tests/test_api.py`

- [ ] **Step 1: Append the failing tests**

```python
def test_analytics_damage_types(client):
    r = client.get("/api/analytics/damage-types")
    body = r.json()
    assert any(x["name"] == "Slashing" and x["count"] >= 1 for x in body)


def test_analytics_monsters_by_cr(client):
    r = client.get("/api/analytics/monsters-by-cr")
    body = r.json()
    assert any(x["cr"] == 0.5 and x["count"] == 1 for x in body)


def test_analytics_spells_by_school(client):
    r = client.get("/api/analytics/spells-by-school")
    assert any(x["school"] == "Evocation" and x["count"] == 1 for x in r.json())


def test_static_index_served(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "<!doctype html" in r.text.lower() or "<html" in r.text.lower()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `app/backend/.venv/bin/python -m pytest app/backend/tests/test_api.py -q`
Expected: FAIL on new tests.

- [ ] **Step 3: Implement analytics endpoints + static mount**

Append to `app/backend/main.py`:

```python
@app.get("/api/analytics/damage-types")
def analytics_damage_types():
    with connect() as conn:
        rows = conn.execute(
            "SELECT t.name, COUNT(*) AS count FROM entity_tags et "
            "JOIN tags t ON et.tag_id=t.id WHERE t.kind='damage_type' "
            "GROUP BY t.id ORDER BY count DESC, t.name").fetchall()
    return [{"name": r["name"], "count": r["count"]} for r in rows]


@app.get("/api/analytics/monsters-by-cr")
def analytics_monsters_by_cr():
    with connect() as conn:
        rows = conn.execute(
            "SELECT cr, COUNT(*) AS count FROM entities "
            "WHERE category='bestiary' AND cr IS NOT NULL "
            "GROUP BY cr ORDER BY cr").fetchall()
    return [{"cr": r["cr"], "count": r["count"]} for r in rows]


@app.get("/api/analytics/spells-by-school")
def analytics_spells_by_school():
    with connect() as conn:
        rows = conn.execute(
            "SELECT school, COUNT(*) AS count FROM entities "
            "WHERE category='spells' AND school IS NOT NULL "
            "GROUP BY school ORDER BY count DESC, school").fetchall()
    return [{"school": r["school"], "count": r["count"]} for r in rows]


@app.get("/api/analytics")
def analytics_index():
    return {"analytics": ["damage-types", "monsters-by-cr", "spells-by-school"]}


if os.path.isdir(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `app/backend/.venv/bin/python -m pytest app/backend/tests/test_api.py -q`
Expected: all pass.

- [ ] **Step 5: Verify the whole API against the real DB**

Run:
`cd app/backend && .venv/bin/python -c "import main; c=main.connect(); print('entities', c.execute('select count(*) from entities').fetchone()[0])"`
Expected: prints `entities 53031`.

---

## PHASE C — FRONTEND

### Task C1: Frontend shell + theme

**Files:**
- Create: `app/frontend/index.html`
- Create: `app/frontend/style.css`

- [ ] **Step 1: Create `app/frontend/index.html`**

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>5e Data</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header>
  <a class="brand" href="#/">5e<span class="accent">Data</span></a>
  <form id="globalSearch" class="gsearch">
    <input id="q" type="search" placeholder="Search all data…" autocomplete="off">
  </form>
  <div class="lookup">
    <input id="idInput" type="text" placeholder="entity id…" autocomplete="off">
    <button id="lookupBtn" title="Jump to entity id">Go</button>
  </div>
</header>
<div class="layout">
  <aside class="sidebar" id="sidebar"></aside>
  <main id="main" class="main"></main>
</div>
<script type="module" src="js/app.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create `app/frontend/style.css`**

```css
:root {
  --bg:#16110d; --panel:#211a14; --panel2:#2a2119; --border:#3b2f22;
  --ink:#d9c9a3; --ink-dim:#9a8a6b; --accent:#e0b45a; --accent-dim:#a8843c;
  --danger:#c96a4b;
}
* { box-sizing: border-box; }
body { margin:0; font-family:Georgia,"Times New Roman",serif; background:var(--bg); color:var(--ink); min-height:100vh; }
a { color:var(--accent); text-decoration:none; }
a:hover { text-decoration:underline; }
header { display:flex; align-items:center; gap:14px; padding:10px 18px; background:var(--panel); border-bottom:1px solid var(--border); position:sticky; top:0; z-index:10; }
.brand { font-size:20px; letter-spacing:1px; }
.brand .accent { color:var(--accent); margin-left:4px; }
.gsearch { flex:1; max-width:520px; }
.gsearch input, .lookup input { width:100%; padding:6px 10px; background:var(--panel2); color:var(--ink); border:1px solid var(--border); border-radius:4px; }
.lookup { display:flex; gap:6px; width:280px; }
.lookup button { padding:6px 14px; background:var(--accent-dim); color:#1a1408; border:none; border-radius:4px; cursor:pointer; font-weight:bold; }
.layout { display:flex; align-items:stretch; }
.sidebar { width:250px; flex-shrink:0; padding:10px; background:var(--panel); border-right:1px solid var(--border); position:sticky; top:50px; height:calc(100vh - 50px); overflow-y:auto; }
.sidebar h3 { color:var(--accent-dim); font-size:12px; text-transform:uppercase; letter-spacing:1px; margin:10px 0 4px; }
.cat { display:flex; justify-content:space-between; padding:4px 8px; border-radius:4px; color:var(--ink); font-size:14px; cursor:pointer; }
.cat:hover { background:var(--panel2); text-decoration:none; }
.cat.active { background:var(--panel2); color:var(--accent); }
.cat-count { color:var(--ink-dim); font-size:12px; }
.main { flex:1; padding:18px; min-width:0; }
.panel { background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:16px; }
h2 { margin:0 0 10px; color:var(--accent); border-bottom:1px solid var(--border); padding-bottom:8px; }
.muted { color:var(--ink-dim); }
.mono { font-family:"Courier New",monospace; font-size:12px; }
.small { font-size:12px; }
code { background:var(--panel2); padding:1px 5px; border-radius:3px; }
.toolbar { display:flex; gap:8px; align-items:center; margin-bottom:10px; flex-wrap:wrap; }
.toolbar select, .toolbar input[type=search] { padding:6px 10px; background:var(--panel2); color:var(--ink); border:1px solid var(--border); border-radius:4px; }
table.list, table.data { width:100%; border-collapse:collapse; font-size:14px; }
table.list th, table.list td { text-align:left; padding:5px 8px; border-bottom:1px solid var(--border); }
table.list th { color:var(--accent-dim); font-size:12px; text-transform:uppercase; letter-spacing:1px; }
table.list tbody tr:hover { background:var(--panel2); }
table.data th, table.data td { border:1px solid var(--border); padding:4px 8px; text-align:left; }
table.data th { background:var(--panel2); color:var(--accent-dim); }
table.data caption { text-align:left; font-style:italic; color:var(--ink-dim); }
.badge { display:inline-block; padding:2px 8px; border-radius:10px; background:var(--panel2); border:1px solid var(--border); font-size:12px; margin:1px 3px 1px 0; }
.badge.src { background:#2b2416; color:var(--accent); }
.badge.dmg { background:#2c1b14; color:#d98e6a; }
.badge.res { color:var(--accent); }
.chip { display:inline-block; padding:2px 8px; border-radius:10px; background:#2a2120; border:1px solid #4a3636; color:#c99; font-size:12px; margin:1px 3px 1px 0; }
.card { background:var(--panel2); border:1px solid var(--border); border-radius:6px; padding:10px 12px; margin:10px 0; }
.card h4 { margin:0 0 6px; color:var(--accent); font-size:15px; }
.field { margin:4px 0; }
.flabel { color:var(--accent-dim); font-size:12px; text-transform:uppercase; letter-spacing:1px; display:inline-block; min-width:130px; }
ul.plain { margin:4px 0; padding-left:18px; }
.filters { display:flex; flex-wrap:wrap; gap:6px; }
.filters .chip { cursor:pointer; }
.filters .chip.active { border-color:var(--accent); color:var(--accent); }
.bar-row { display:flex; align-items:center; gap:8px; margin:3px 0; font-size:14px; }
.bar { background:var(--panel2); border:1px solid var(--border); height:16px; border-radius:3px; }
.bar-fill { display:block; height:100%; background:var(--accent-dim); }
.tabs { display:flex; gap:6px; margin:10px 0; }
.tab { padding:5px 12px; border:1px solid var(--border); border-radius:4px; cursor:pointer; color:var(--ink-dim); }
.tab.active { background:var(--panel2); color:var(--accent); }
.error { color:var(--danger); border:1px solid var(--danger); border-radius:6px; padding:12px; background:#2a1812; }
.empty { color:var(--ink-dim); font-style:italic; padding:8px 0; }
```

- [ ] **Step 3: Check served over API**

Run: start backend (`app/backend/run.sh`) then `curl -s http://localhost:8000/ | head -5`
Expected: HTML shell.

---

### Task C2: `js/api.js`

**Files:**
- Create: `app/frontend/js/api.js`

- [ ] **Step 1: Create `js/api.js`**

```javascript
export async function get(path) {
  const res = await fetch('/api' + path);
  if (!res.ok) {
    let detail = 'HTTP ' + res.status;
    try { detail = (await res.json()).detail || detail; } catch (e) {}
    throw new Error(detail);
  }
  return res.json();
}

export const api = {
  meta: () => get('/meta'),
  categories: () => get('/categories'),
  search: (p) => get('/search?' + new URLSearchParams(p)),
  entity: (id) => get('/entities/' + encodeURIComponent(id)),
  refs: (id, dir) => get('/entities/' + encodeURIComponent(id) + '/references?direction=' + dir),
  unresolved: (id) => get('/entities/' + encodeURIComponent(id) + '/unresolved'),
  filters: () => get('/filters'),
  analytics: (name) => get('/analytics/' + name),
};
```

- [ ] **Step 2: Verify import works**

Run: `node --check app/frontend/js/api.js`
Expected: exit 0.

---

### Task C3: `js/render.js` — ported rendering logic

**Files:**
- Create: `app/frontend/js/render.js`

- [ ] **Step 1: Create `js/render.js`**

This is the port of the proven rendering logic from `navigator/app.js`.

```javascript
export function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

export function renderText(s) {
  const safe = esc(s);
  return safe
    .replace(/\{\{ref:([a-z]+):([^}]*)\}\}/g, (m, tag, name) =>
      '<span class="chip" title="unresolved ' + tag + ' ref">' + tag + ': ' + name + '</span>')
    .replace(/\{\{ref:([^{}]+)\}\}/g, (m, id) =>
      '<a class="ref" href="#/e/' + encodeURIComponent(id) + '" title="' + id + '">[' +
      id.split('-').pop() + ']</a>');
}

export function renderValue(v) {
  if (v === null || v === undefined) return '<span class="muted">—</span>';
  if (typeof v === 'string') return renderText(v);
  if (typeof v === 'number' || typeof v === 'boolean') return esc(v);
  if (Array.isArray(v)) {
    if (!v.length) return '<span class="muted">[]</span>';
    if (v.every((x) => typeof x === 'string' || typeof x === 'number')) {
      return '<ul class="plain">' + v.map((x) => '<li>' + renderText(String(x)) + '</li>').join('') + '</ul>';
    }
    return v.map(renderValue).join('');
  }
  if (v.type === 'attack') return renderAttack(v);
  if (v.type === 'table') return renderTable(v);
  if (v.type === 'list') return '<ul class="plain">' +
    (v.items || []).map((i) => '<li>' + (typeof i === 'string' ? renderText(i) : renderValue(i)) + '</li>').join('') + '</ul>';
  if (v.type === 'entries') return '<div class="entries">' +
    (v.entries || []).map(renderValue).join('') + '</div>';
  const name = v.name;
  const inner = Object.entries(v)
    .filter(([k]) => k !== 'name' && k !== 'type')
    .map(([k, x]) => '<div class="field"><span class="flabel">' + esc(k) + '</span>' +
      '<span class="fval">' + renderValue(x) + '</span></div>').join('');
  return '<div class="card">' + (name ? '<h4>' + esc(name) + '</h4>' : '') + inner + '</div>';
}

export function renderAttack(a) {
  const badges = [];
  if (a.kind) badges.push(esc(a.kind));
  if (a.toHit !== null && a.toHit !== undefined) badges.push((a.toHit >= 0 ? '+' : '') + a.toHit + ' to hit');
  if (a.reach) badges.push('reach ' + esc(a.reach));
  if (a.range) badges.push('range ' + esc(a.range));
  if (a.targets) badges.push(esc(a.targets));
  const dmg = (a.damage || []).map((d) =>
    '<span class="badge dmg">' + esc(d.average) + ' (' + esc(d.dice) + ') ' + esc(d.type || '') + '</span>').join('');
  return '<div class="card attack"><h4>Attack</h4>' +
    '<div class="badges">' + badges.map((b) => '<span class="badge">' + b + '</span>').join('') + '</div>' +
    dmg +
    (a.hit ? '<div class="field"><span class="flabel">hit</span><span class="fval">' + renderText(a.hit) + '</span></div>' : '') +
    '<div class="mono muted small">' + esc(a.rawText || '') + '</div></div>';
}

export function renderTable(t) {
  return '<table class="data">' +
    (t.caption ? '<caption>' + esc(t.caption) + '</caption>' : '') +
    (t.colLabels ? '<thead><tr>' + t.colLabels.map((c) => '<th>' + esc(c) + '</th>').join('') + '</tr></thead>' : '') +
    '<tbody>' + (t.rows || []).map((r) => '<tr>' +
      (Array.isArray(r) ? r : []).map((c) => '<td>' + renderText(String(c)) + '</td>').join('') + '</tr>').join('') +
    '</tbody></table>';
}
```

- [ ] **Step 2: Verify syntax**

Run: `node --check app/frontend/js/render.js`
Expected: exit 0.

---

### Task C4: `js/app.js` — routing, views, search, filters, detail, analytics

**Files:**
- Create: `app/frontend/js/app.js`

- [ ] **Step 1: Create `js/app.js`**

```javascript
import { api } from './api.js';
import { esc, renderText, renderValue } from './render.js';

const PRETTY = {
  bestiary: 'Bestiary', spells: 'Spells', items: 'Items', races: 'Races',
  classes: 'Classes', subclasses: 'Subclasses', class_features: 'Class Features',
  subclass_features: 'Subclass Features', feats: 'Feats', backgrounds: 'Backgrounds',
  actions: 'Actions', optionalfeatures: 'Optional Features',
  conditionsdiseases: 'Conditions & Diseases', deities: 'Deities', cultsboons: 'Cults & Boons',
  languages: 'Languages', objects: 'Objects', psionics: 'Psionics', rewards: 'Rewards',
  skills: 'Skills', tables: 'Tables', trapshazards: 'Traps & Hazards',
  variantrules: 'Variant Rules', vehicles: 'Vehicles', encounters: 'Encounters',
  senses: 'Senses', charcreationoptions: 'Char Creation Options', books: 'Books',
  adventures: 'Adventures', book_tables: 'Book Tables', adventure_data: 'Adventure Data',
};

const $ = (s) => document.querySelector(s);
const main = () => $('#main');
let filtersCache = null;

function errPanel(e) {
  return '<div class="panel"><h2>Error</h2><div class="error">' + esc(e.message || e) + '</div>' +
    '<p><a href="#/">← home</a></p></div>';
}

async function route() {
  const h = location.hash;
  document.querySelectorAll('.cat').forEach((a) =>
    a.classList.toggle('active', a.getAttribute('href') === h));
  if (h.startsWith('#/e/')) return showEntity(decodeURIComponent(h.slice(4)));
  if (h.startsWith('#/c/')) return showList(decodeURIComponent(h.slice(4)), {});
  if (h.startsWith('#/s/')) {
    let params = {};
    try { params = JSON.parse(decodeURIComponent(h.slice(4))); } catch (e) {}
    return showSearch(params);
  }
  if (h.startsWith('#/a/')) return showAnalytics(decodeURIComponent(h.slice(4)));
  return showHome();
}

async function showHome() {
  try {
    const [meta, cats] = await Promise.all([api.meta(), api.categories()]);
    const total = cats.reduce((a, c) => a + c.count, 0);
    const s = meta.stats || {};
    main().innerHTML = '<div class="panel"><h2>5e Dataset</h2>' +
      '<p class="muted">' + esc(total) + ' entities · ' + esc(s.resolved) + ' resolved refs · ' +
      esc(s.unresolved) + ' unresolved · ' + esc(s.attacks) + ' typed attacks</p>' +
      '<p><a href="#/c/bestiary">Browse the Bestiary →</a> · ' +
      '<a href="#/a/damage-types">Damage types</a> · <a href="#/a/monsters-by-cr">Monsters by CR</a> · ' +
      '<a href="#/a/spells-by-school">Spells by school</a></p></div>';
  } catch (e) {
    main().innerHTML = errPanel(e);
  }
}

async function buildSidebar(active) {
  try {
    const cats = await api.categories();
    const html = cats.map((c) =>
      '<a class="cat' + (c.category === active ? ' active' : '') + '" href="#/c/' + c.category + '">' +
      '<span>' + esc(PRETTY[c.category] || c.category) + '</span><span class="cat-count">' + c.count + '</span></a>'
    ).join('');
    $('#sidebar').innerHTML = '<h3>Categories</h3>' + html;
  } catch (e) {
    $('#sidebar').innerHTML = '<div class="muted small">' + esc(e.message) + '</div>';
  }
}

function filterChips(params) {
  const defs = [['category', 'Category'], ['source', 'Source'], ['damage_type', 'Damage'],
    ['condition', 'Condition'], ['save', 'Save'], ['school', 'School'], ['rarity', 'Rarity']];
  const chips = defs.filter(([k]) => params[k]).map(([k, label]) =>
    '<span class="chip" data-k="' + k + '" title="remove filter">' + esc(label) + ': ' +
    esc(params[k]) + ' ✕</span>');
  return chips.join('');
}

async function showSearch(params) {
  await buildSidebar(params.category);
  const mainEl = main();
  mainEl.innerHTML = '<div class="panel"><h2>Search</h2>' +
    '<div class="toolbar">' +
      '<input id="q" type="search" placeholder="Search…" value="' + esc(params.q || '') + '">' +
      '<select id="catSel"><option value="">all categories</option></select>' +
      '<select id="srcSel"><option value="">all sources</option></select>' +
      '<span class="muted" id="count"></span>' +
    '</div>' +
    '<div class="filters" id="chipbar">' + filterChips(params) + '</div>' +
    '<table class="list"><thead><tr><th>Name</th><th>Category</th><th>Source</th></tr></thead>' +
    '<tbody></tbody></table></div>';

  if (!filtersCache) filtersCache = await api.filters();
  const catSel = $('#catSel');
  filtersCache.categories.forEach((c) => {
    const o = document.createElement('option');
    o.value = c.category; o.textContent = PRETTY[c.category] || c.category;
    if (params.category === c.category) o.selected = true;
    catSel.appendChild(o);
  });
  const srcSel = $('#srcSel');
  filtersCache.sources.forEach((s) => {
    const o = document.createElement('option');
    o.value = s.source; o.textContent = s.source;
    if (params.source === s.source) o.selected = true;
    srcSel.appendChild(o);
  });

  const render = async () => {
    const p = Object.assign({}, params, {
      q: $('#q').value.trim(), category: catSel.value || undefined,
      source: srcSel.value || undefined,
    });
    Object.keys(p).forEach((k) => p[k] === undefined && delete p[k]);
    const body = await api.search(p);
    $('#count').textContent = body.total + ' results';
    $('#main tbody').innerHTML = body.results.map((r) =>
      '<tr><td><a href="#/e/' + encodeURIComponent(r.id) + '">' + esc(r.name) + '</a></td>' +
      '<td>' + esc(PRETTY[r.category] || r.category) + '</td><td>' + esc(r.source || '—') + '</td></tr>'
    ).join('');
  };

  $('#q').addEventListener('input', () => render().catch((e) => { $('#count').textContent = e.message; }));
  catSel.addEventListener('change', () => render().catch((e) => { $('#count').textContent = e.message; }));
  srcSel.addEventListener('change', () => render().catch((e) => { $('#count').textContent = e.message; }));
  $('#chipbar').addEventListener('click', (ev) => {
    const chip = ev.target.closest('.chip[data-k]');
    if (!chip) return;
    const k = chip.dataset.k;
    const p = Object.assign({}, params);
    delete p[k];
    location.hash = '#/s/' + encodeURIComponent(JSON.stringify(p));
  });
  render().catch((e) => { $('#count').textContent = e.message; });
}

async function showList(cat, params) {
  await buildSidebar(cat);
  return showSearch(Object.assign({ category: cat }, params));
}

async function showEntity(id) {
  main().innerHTML = '<h2>Loading…</h2>';
  let ent;
  try {
    ent = await api.entity(id);
  } catch (e) {
    main().innerHTML = errPanel(e);
    return;
  }
  const name = ent.name || ent.id;
  const skip = new Set(['id', 'references', 'name', 'caption', 'source',
    'adventureSource', 'type', 'category', 'tags', 'references_out',
    'references_in', 'unresolved', 'payload', 'derived_from']);
  let body = '';
  const walk = (v) => {
    if (typeof v === 'string') return renderText(v);
    if (typeof v === 'object' && v !== null) return renderValue(v);
    return esc(v);
  };
  for (const [k, v] of Object.entries(ent.payload)) {
    if (skip.has(k)) continue;
    if (v === undefined) continue;
    body += '<div class="field"><span class="flabel">' + esc(k) + '</span>' +
      '<span class="fval">' + walk(v) + '</span></div>';
  }
  const chips = (ent.tags || []).map((t) => {
    if (t.kind === 'condition' && t.target_entity_id) {
      return '<a class="badge res" href="#/e/' + encodeURIComponent(t.target_entity_id) + '">' +
        esc(t.name) + '</a>';
    }
    if (t.kind === 'damage_type' || t.kind === 'misc' || t.kind === 'saving_throw' || t.kind === 'action_tag') {
      const f = t.kind === 'damage_type' ? 'damage_type' : t.kind === 'saving_throw' ? 'save' : t.kind;
      return '<a class="badge" href="#/s/' + encodeURIComponent(JSON.stringify({ [f]: t.id })) + '">' +
        esc(t.name) + '</a>';
    }
    return '<span class="badge">' + esc(t.name) + '</span>';
  }).join('');

  main().innerHTML = '<div class="panel"><h2>' + esc(name) + '</h2>' +
    '<div>' + chips + '</div>' +
    '<div class="tabs">' +
      '<span class="tab active" data-tab="body">Body</span>' +
      '<span class="tab" data-tab="refs">References (' + (ent.references_out + ent.references_in) + ')</span>' +
      '<span class="tab" data-tab="unresolved">Unresolved (' + ent.unresolved + ')</span>' +
    '</div>' +
    '<div id="tab-body">' + body + '</div>' +
    '<div id="tab-refs" hidden></div>' +
    '<div id="tab-unresolved" hidden></div>' +
    '<p class="muted small"><a href="#/c/' + ent.category + '">← ' +
    esc(PRETTY[ent.category] || ent.category) + '</a> · <span class="mono">' +
    esc(ent.id) + '</span>' + (ent.derived_from ? ' · derived from <a href="#/e/' +
    encodeURIComponent(ent.derived_from) + '">' + esc(ent.derived_from) + '</a>' : '') + '</p></div>';

  main().querySelectorAll('.tab').forEach((tab) => {
    tab.addEventListener('click', () => {
      main().querySelectorAll('.tab').forEach((t) => t.classList.toggle('active', t === tab));
      main().querySelector('#tab-body').hidden = tab.dataset.tab !== 'body';
      main().querySelector('#tab-refs').hidden = tab.dataset.tab !== 'refs';
      main().querySelector('#tab-unresolved').hidden = tab.dataset.tab !== 'unresolved';
    });
  });

  if (ent.references_out + ent.references_in > 0) {
    try {
      const [outRefs, inRefs] = await Promise.all([api.refs(id, 'out'), api.refs(id, 'in')]);
      const renderRefs = (label, list) => {
        if (!list.length) return '';
        return '<div class="card"><h4>' + label + ' (' + list.length + ')</h4>' +
          list.map((r) => '<div><a href="#/e/' + encodeURIComponent(r.id) + '">' + esc(r.name || r.id) +
            '</a> <span class="muted small">' + esc(PRETTY[r.category] || r.category) +
            ' · ' + esc(r.ref_type || '') + '</span></div>').join('') + '</div>';
      };
      const el = main().querySelector('#tab-refs');
      el.innerHTML = renderRefs('References out', outRefs) + renderRefs('References in', inRefs);
    } catch (e) {
      main().querySelector('#tab-refs').innerHTML = errPanel(e);
    }
  }
  if (ent.unresolved > 0) {
    try {
      const un = await api.unresolved(id);
      main().querySelector('#tab-unresolved').innerHTML =
        '<div class="card"><h4>Unresolved (' + un.length + ')</h4>' +
        un.map((u) => '<div><span class="chip">' + esc(u.tag) + ': ' + esc(u.name) +
          '</span> <span class="muted small">' + esc(u.reason || '') + '</span></div>').join('') + '</div>';
    } catch (e) {
      main().querySelector('#tab-unresolved').innerHTML = errPanel(e);
    }
  }
}

function histogram(items, key, label) {
  const max = Math.max(...items.map((x) => x.count));
  return '<div class="panel"><h2>' + label + '</h2>' + items.map((x) =>
    '<div class="bar-row"><span style="width:200px" class="muted small">' +
    (x[key] === null || x[key] === undefined ? '—' : esc(String(x[key]))) + '</span>' +
    '<span class="bar" style="width:300px"><span class="bar-fill" style="width:' +
    Math.round((x.count / max) * 100) + '%"></span></span>' +
    '<span class="small">' + x.count + '</span></div>').join('') + '</div>';
}

async function showAnalytics(name) {
  await buildSidebar();
  const views = {
    'damage-types': ['name', 'Damage types'],
    'monsters-by-cr': ['cr', 'Monsters by CR'],
    'spells-by-school': ['school', 'Spells by school'],
  };
  if (!views[name]) {
    main().innerHTML = '<div class="panel"><h2>Not found</h2><p><a href="#/">← home</a></p></div>';
    return;
  }
  try {
    const data = await api.analytics(name);
    main().innerHTML = histogram(data, views[name][0], views[name][1]);
  } catch (e) {
    main().innerHTML = errPanel(e);
  }
}

function lookup() {
  const id = $('#idInput').value.trim();
  if (!id) return;
  location.hash = '#/e/' + encodeURIComponent(id);
}

window.addEventListener('hashchange', route);
$('#globalSearch').addEventListener('submit', (e) => {
  e.preventDefault();
  const q = $('#q').value.trim();
  if (!q) return;
  location.hash = '#/s/' + encodeURIComponent(JSON.stringify({ q }));
});
$('#lookupBtn').addEventListener('click', lookup);
$('#idInput').addEventListener('keydown', (e) => { if (e.key === 'Enter') lookup(); });

route();
```

- [ ] **Step 2: Verify syntax**

Run: `node --check app/frontend/js/app.js`
Expected: exit 0.

- [ ] **Step 3: Manual click-through against the real DB**

Run: `app/backend/run.sh`, open `http://localhost:8000/`.
Checklist:
1. Home shows counts/stats.
2. Sidebar lists categories; Bestiary opens with 4,539 monsters.
3. Global search "fireball" → Fireball spell; search "dragon" with category filter Bestiary.
4. Open Adult Red Dragon → body renders attacks with damage badges; conditions are linked chips → clicking "Grappled" opens the condition entity.
5. References tab: "references out" (Bite → Grappled condition) and "references in" (which monsters reference the dragon).
6. Damage-type chip "Fire" → search filtered by `damage_type=damage-type-fire` returns all fire-dealing monsters.
7. Unresolved tab shows muted chips with reasons.
8. Analytics pages render histograms.

---

### Task C5: Frontend smoke script + retire JSON

**Files:**
- Create: `app/frontend/smoke.sh`
- Modify: `structure_5etools.py` (remove JSON output, keep db)

- [ ] **Step 1: Create `app/frontend/smoke.sh`**

```bash
#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
for f in js/app.js js/render.js js/api.js; do node --check "$f" >/dev/null || { echo "FAIL: $f"; exit 1; }; done
echo "syntax ok"
BASE=${BASE_URL:-http://localhost:8000}
for p in /api/meta /api/categories "/api/search?q=fireball" "/api/entities/monster-ork-mm"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "$BASE$p")
  echo "  $p -> $code"
  [ "$code" = "200" ] || { echo "FAIL: $p"; exit 1; }
done
echo "ALL OK"
```

- [ ] **Step 2: Run the smoke script**

Start the backend, then:
Run: `app/frontend/smoke.sh`
Expected: `ALL OK`.

- [ ] **Step 3: Remove JSON output from `structure_5etools.py` (final step)**

In `main()`, delete:
- the `out_file = collection + ".json"` write inside the per-category loop
- the `adventure_data.json` write
- the `_index.json` write
- the `metadata.json` write

and keep `counts`/`stats` for the DB meta table. Then:

Run: `./rebuild.sh`
Expected: builds `data_out/5e.db` only; `data_out/*.json` category files and `_index.json`/`metadata.json` no longer regenerated.

- [ ] **Step 4: Retire the static navigator**

Delete the `navigator/` directory (its data source no longer exists).

- [ ] **Step 5: Final end-to-end acceptance**

Run: `app/backend/run.sh`, click through the Task C4 Step 3 checklist once more on the DB-only build.

---

## Self-Review

**Spec coverage**
- Schema (entities, FTS, references, unresolved_refs, tags, entity_tags, meta) → A4/A5. ✓
- `_copy` materialization → A1/A3. ✓
- Tag decode (`damageTags`/`miscTags`/`conditionInflict`/`savingThrowForced`/`actionTags`) → A4. ✓
- Fuzzy pass → A2/A3. ✓
- Adventure section ref attribution → A5 (`collect_section_refs`). ✓
- Validation invariants → A6. ✓
- Backend endpoints (meta/categories/search/entity/refs/unresolved/filters/analytics) → B2–B5. ✓
- Frontend views + tag chips + refs in/out + analytics → C4. ✓
- Error handling (404/400/503, fetch-error banner, empty states) → B2/B3, C4. ✓
- Staging (JSON removed last) → C5. ✓

**Placeholder scan:** none — every code step contains its full implementation. The only cross-task references are to `db_writer.build_db` and `validate_db.validate`, defined in the tasks that own them.

**Type consistency**
- `db_writer.build_db(db_path, all_entities, condition_ids, skill_ids, meta)` used identically in A4/A5/A6/B2 fixtures. ✓
- `validate_db.validate(db_path) -> list[str]` used identically in A5/A6/A7. ✓
- `materialize.materialize_category(entities) -> list` and `materialize_entity(ent, lookup)` used in A1/A3. ✓
- `fuzzy.fuzzy_resolve(tag, name, source, name_index, collections) -> (id, rule) | None` used in A2/A3. ✓
- API param names (`q`, `category`, `source`, `damage_type`, `condition`, `save`, `school`, `rarity`, `cr_min`, `cr_max`, `limit`, `offset`) consistent between B3 and C4. ✓
- `renderText`/`renderValue`/`renderAttack`/`renderTable`/`esc` exports match imports in C3/C4. ✓