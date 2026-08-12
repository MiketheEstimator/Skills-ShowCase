# SKILL_SHEET_PROMPT_CONTRACT

## Track
prompt_contracts

## Intent
Reusable showcase workflow for prompt contracts artifacts.

## Primary References
- Playbook: `./spells/playbooks/SKILL_LLM_SESSION_STATE.md`
- Registry: `./skill_registry.json`
- QA gates: `./ontology/qa_gates.json`

## Execution Contract
1. Resolve intent and route to selected skill.
2. Execute transformation using declared playbook.
3. Validate against schema and QA gate.
4. Return artifact with validation status.

## Focus Code
`PROMPT-PIPE-001`
