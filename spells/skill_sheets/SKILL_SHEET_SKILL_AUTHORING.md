# SKILL_SHEET_SKILL_AUTHORING

## Track
skill_authoring

## Intent
Reusable showcase workflow for skill authoring artifacts.

## Primary References
- Playbook: `./spells/playbooks/SKILL_STYLE.md`
- Registry: `./skill_registry.json`
- QA gates: `./ontology/qa_gates.json`

## Execution Contract
1. Resolve intent and route to selected skill.
2. Execute transformation using declared playbook.
3. Validate against schema and QA gate.
4. Return artifact with validation status.

## Focus Code
`AUTHOR-001`
