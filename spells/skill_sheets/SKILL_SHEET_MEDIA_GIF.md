# SKILL_SHEET_MEDIA_GIF

## Track
media_editing

## Intent
Reusable showcase workflow for media editing artifacts.

## Primary References
- Playbook: `./spells/playbooks/SKILL_IMAGE_GIF_OPTIMIZE.md`
- Registry: `./skill_registry.json`
- QA gates: `./ontology/qa_gates.json`

## Execution Contract
1. Resolve intent and route to selected skill.
2. Execute transformation using declared playbook.
3. Validate against schema and QA gate.
4. Return artifact with validation status.

## Focus Code
`MEDIA-PIPE-003`
