# SKILL_SHEET_DOCUMENT_PDF

## Track
documents

## Intent
Reusable showcase workflow for documents artifacts.

## Primary References
- Playbook: `./spells/playbooks/SKILL_AUTOMATED_PRECISION_PDF.md`
- Registry: `./skill_registry.json`
- QA gates: `./ontology/qa_gates.json`

## Execution Contract
1. Resolve intent and route to selected skill.
2. Execute transformation using declared playbook.
3. Validate against schema and QA gate.
4. Return artifact with validation status.

## Focus Code
`DOC-TRANSFORM-003`
