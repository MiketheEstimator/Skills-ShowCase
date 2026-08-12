# SKILL_SHEET_CODE_PYTHON

## Track
code_generation

## Intent
Reusable showcase workflow for code generation artifacts.

## Primary References
- Playbook: `./spells/playbooks/SKILL_CODE_PYTHON_GENERAL.md`
- Registry: `./skill_registry.json`
- QA gates: `./ontology/qa_gates.json`

## Execution Contract
1. Resolve intent and route to selected skill.
2. Execute transformation using declared playbook.
3. Validate against schema and QA gate.
4. Return artifact with validation status.

## Focus Code
`CODE-PIPE-001`
