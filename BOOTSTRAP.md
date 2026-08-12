# 2IT SKILLS Showcase Bootstrap

## Load order
1. Read `skillpack_manifest.json`.
2. Load `skill_registry.json`.
3. Load `maps/router_rules.json`.
4. Load `ontology/qa_gates.json`.
5. Resolve and load required skill sheets from `spells/skill_sheets/index.json`.
6. Validate contracts in `schemas/` before finalizing artifacts.

## Runtime contract
- Route deterministically.
- Prefer schema-first outputs.
- Enforce QA gates before final response.
- Reject outputs that violate integrity policy.
