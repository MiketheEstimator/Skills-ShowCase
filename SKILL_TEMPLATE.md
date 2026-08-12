# SKILL_TEMPLATE

## Metadata
- skill_id:
- canonical_name:
- category:
- description:
- artifact_types:
- playbook_ref:
- qa_gate_id:

## Intent Profile
- primary_intents:
- output_types:
- transformation_types:
- fidelity_level:

## Execution Contract
1. Resolve input intent.
2. Apply transformation.
3. Validate against schema.
4. Apply QA gate.
5. Return artifact and validation status.

## Failure Policy
- fail_closed_on_schema_violation: true
- fail_closed_on_integrity_policy_violation: true
