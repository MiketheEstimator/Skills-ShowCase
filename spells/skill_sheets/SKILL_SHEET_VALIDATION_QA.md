# SKILL_SHEET_VALIDATION_QA

## Track
validation_qa

## Intent
Reusable showcase workflow for validation qa artifacts.

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
`VALIDATE-001`
