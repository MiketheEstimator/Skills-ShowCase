# 2IT SKILLS Showcase

2IT SKILLS Showcase is a public, general-purpose skillpack repository for deterministic LLM workflows.
It demonstrates how to run registry-driven routing, schema-first artifact generation, and validation gates with clean repository contracts.

## Repository purpose
- Provide reusable skill definitions for document, spreadsheet, slide, media, code, and data workflows.
- Route user requests to skills by output type, transformation type, and fidelity requirements.
- Enforce validation gates before final artifact delivery.
- Keep public-facing surfaces free of narrow domain contamination.

## Core architecture
- `BOOTSTRAP.md`: execution bootstrap and loading order.
- `skill_registry.json`: canonical skill registry.
- `maps/router_rules.json`: intent-to-skill routing table.
- `ontology/qa_gates.json`: quality gates and contamination controls.
- `schemas/`: artifact contract schemas.
- `spells/skill_sheets/`: lightweight skill execution overlays.
- `scripts/validate_integrity.py`: integrity and policy validation.

## Skill organization
Skills are grouped by reusable categories:
- documents
- spreadsheets
- presentations
- data_serialization
- diagrams
- code_generation
- media_editing
- validation_qa
- transformation_pipelines
- prompt_contracts
- skill_authoring
- schema_design
- artifact_routing
- metacognitive_support

See `CATEGORY_MAP.md` for category definitions and mapping rules.

## Routing and QA flow
1. Load bootstrap and registry.
2. Route by modality, output format, and transformation request.
3. Apply the selected skill and related skill sheet.
4. Validate output against schema contracts and QA gates.
5. Block output if integrity policy violations are detected.

## Add a new skill
1. Copy `SKILL_TEMPLATE.md` and fill metadata.
2. Add a registry entry in `skill_registry.json`.
3. Add router intents in `maps/router_rules.json` if discoverability is needed.
4. Add or map QA gates in `ontology/qa_gates.json`.
5. Add/adjust a skill sheet in `spells/skill_sheets/index.json`.
6. Run `python scripts/validate_integrity.py`.

## Supported artifact classes
- docx, pdf, markdown, html
- xlsx, csv, tsv, json, xml, yaml, toml
- pptx, revealjs
- png, gif, svg, video derivatives
- python, bash, docker, notebook
- diagram artifacts (mermaid, plantuml)

## Integrity validation
Run:

```bash
python scripts/validate_integrity.py
```

Validation covers:
- path integrity across manifest, router, registry, and sheets
- schema and gate consistency
- naming normalization
- forbidden-term contamination in public-facing files
- required showcase vocabulary presence

## Suggested public tree
See `DIRECTORY_TREE.md` for the normalized tree used by this showcase.

## Migration notes
See `MIGRATION_NOTES.md` for preservation, renames, abstractions, and removals from the legacy ACES framing.
