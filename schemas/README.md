# SkillPack Schemas

This directory contains strict, machine-validated contracts used by the ACES SkillPack.

## Purpose
- Provide deterministic output contracts for LLM artifact generation.
- Enable pre-deployment validation in CI.
- Reduce regressions from prompt or playbook drift.

## Current Schemas
- `artifact_envelope.schema.json`: Common envelope for generated outputs.

## Validation
Use the repository validator:

```bash
python scripts/validate_skillpack.py
```

This checks schema directory existence and validates cross-file references.
