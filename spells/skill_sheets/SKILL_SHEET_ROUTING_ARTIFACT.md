# SKILL_SHEET_ROUTING_ARTIFACT

## Track
artifact_routing

## Intent
Reusable showcase workflow for artifact routing artifacts.

## Primary References
- Playbook: `./spells/playbooks/SKILL_RENDERED_HTML_DOCUMENT.md`
- Registry: `./skill_registry.json`
- QA gates: `./ontology/qa_gates.json`

## Execution Contract
1. Resolve intent and route to selected skill.
2. Execute transformation using declared playbook.
3. Validate against schema and QA gate.
4. Return artifact with validation status.

## Focus Code
`ROUTE-PIPE-001`
