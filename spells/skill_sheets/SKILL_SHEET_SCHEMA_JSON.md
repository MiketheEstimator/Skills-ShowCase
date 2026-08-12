# SKILL_SHEET_SCHEMA_JSON

## Track
schema_design

## Intent
Reusable showcase workflow for schema design artifacts.

## Primary References
- Playbook: `./spells/playbooks/SKILL_VALIDATED_JSON_EXPORT.md`
- Registry: `./skill_registry.json`
- QA gates: `./ontology/qa_gates.json`

## Execution Contract
1. Resolve intent and route to selected skill.
2. Execute transformation using declared playbook.
3. Validate against schema and QA gate.
4. Return artifact with validation status.

## Focus Code
`SCHEMA-PIPE-002`
