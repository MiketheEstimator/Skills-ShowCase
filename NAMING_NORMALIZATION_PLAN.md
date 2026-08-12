# Naming Normalization Plan

## Rules
- Use `SKILL_<SUBJECT>_<FUNCTION>` for skill ids.
- Use `SKILL_SHEET_<SUBJECT>` for sheet filenames.
- Use uppercase snake case for IDs and file stems.
- Align `sheet_id` with `sheet_ref` basename.
- Keep categories lowercase snake case.

## Migration actions
- Replace numeric list sheet filenames with subject names.
- Replace domain-prefixed categories with general-purpose categories.
- Keep playbook names stable where possible; map via neutral registry names.
