#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_TERMS = [
    "subcontractor",
    "rfi",
    "cpm",
    "masterformat",
    "estimator",
    "trade routing",
    "live construction package",
]
REQUIRED_TERMS = [
    "skill",
    "validation",
    "schema",
    "routing",
    "artifact",
    "transformation",
    "structure",
    "workflow",
    "template",
    "contract",
]
PUBLIC_FILES = [
    "README.md",
    "BOOTSTRAP.md",
    "INJECTION_PROTOCOL.md",
    "skillpack_manifest.json",
    "skill_registry.json",
    "maps/router_rules.json",
    "ontology/qa_gates.json",
    "SKILL_TEMPLATE.md",
    "spells/skill_sheets/index.json",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_exists(label: str, rel: str, errors: list[str]) -> None:
    if not (ROOT / rel).exists():
        errors.append(f"{label}: missing path '{rel}'")


def validate_manifest(errors: list[str]) -> None:
    manifest = load_json(ROOT / "skillpack_manifest.json")
    index = manifest.get("manifest_index", {})
    for key in [
        "bootstrap",
        "router",
        "skills_registry",
        "playbooks_dir",
        "skill_sheets_index",
        "qa_gates",
        "schemas",
    ]:
        if key not in index:
            errors.append(f"manifest_index: missing key '{key}'")
            continue
        check_exists(f"manifest_index.{key}", index[key], errors)


def validate_registry(errors: list[str]) -> set[str]:
    registry = load_json(ROOT / "skill_registry.json")
    skills = registry.get("skills", [])
    ids: set[str] = set()
    for i, s in enumerate(skills, start=1):
        sid = s.get("skill_id")
        if not sid:
            errors.append(f"skills[{i}]: missing skill_id")
            continue
        if sid in ids:
            errors.append(f"skills[{i}]: duplicate skill_id '{sid}'")
        ids.add(sid)
        for key in ["playbook_ref", "qa_gate_id", "category", "artifact_types"]:
            if key not in s:
                errors.append(f"skills[{i}] ({sid}): missing key '{key}'")
        check_exists(f"skills[{i}] ({sid}).playbook_ref", s.get("playbook_ref", ""), errors)
    return ids


def validate_router(skill_ids: set[str], errors: list[str]) -> None:
    router = load_json(ROOT / "maps/router_rules.json")
    for i, node in enumerate(router.get("routing_table", []), start=1):
        check_exists(f"routing_table[{i}].playbook_ref", node.get("playbook_ref", ""), errors)
        for sid in node.get("target_skill_ids", []):
            if sid not in skill_ids:
                errors.append(f"routing_table[{i}]: unknown skill_id '{sid}'")
        for k in ["output_types", "transformation_types", "intent_triggers"]:
            if not node.get(k):
                errors.append(f"routing_table[{i}]: missing or empty '{k}'")


def validate_qa(errors: list[str]) -> set[str]:
    qa = load_json(ROOT / "ontology/qa_gates.json").get("qa_checks", {})
    if "QA_GATE_SHOWCASE_CONTAMINATION" not in qa:
        errors.append("qa_checks: missing QA_GATE_SHOWCASE_CONTAMINATION")
    return set(qa.keys())


def validate_skill_sheets(errors: list[str]) -> None:
    index = load_json(ROOT / "spells/skill_sheets/index.json")
    sheets = index.get("skill_sheets", [])
    if len(sheets) < 12:
        errors.append(f"skill_sheets: expected at least 12 entries, found {len(sheets)}")
    seen = set()
    for i, s in enumerate(sheets, start=1):
        sid = s.get("sheet_id", "")
        ref = s.get("sheet_ref", "")
        if sid in seen:
            errors.append(f"skill_sheets[{i}]: duplicate sheet_id '{sid}'")
        seen.add(sid)
        check_exists(f"skill_sheets[{i}].sheet_ref", ref, errors)
        name = Path(ref).name
        if re.search(r"SKILL_SHEET_\d{3}\.md$", name):
            errors.append(f"skill_sheets[{i}]: numeric list filename forbidden '{name}'")


def validate_language_policy(errors: list[str]) -> None:
    texts = []
    for rel in PUBLIC_FILES:
        path = ROOT / rel
        if path.exists():
            texts.append(path.read_text(encoding="utf-8").lower())
    for p in sorted((ROOT / "spells" / "skill_sheets").glob("*.md")):
        texts.append(p.read_text(encoding="utf-8").lower())
    blob = "\n".join(texts)
    for term in FORBIDDEN_TERMS:
        if term in blob:
            errors.append(f"integrity_policy: forbidden term detected '{term}'")
    for term in REQUIRED_TERMS:
        if term not in blob:
            errors.append(f"integrity_policy: required term missing '{term}'")


def main() -> int:
    errors: list[str] = []
    validate_manifest(errors)
    skill_ids = validate_registry(errors)
    validate_router(skill_ids, errors)
    qa_ids = validate_qa(errors)
    registry = load_json(ROOT / "skill_registry.json").get("skills", [])
    for i, s in enumerate(registry, start=1):
        q = s.get("qa_gate_id")
        if q and q not in qa_ids:
            errors.append(f"skills[{i}] ({s.get('skill_id')}): unknown QA gate '{q}'")
    validate_skill_sheets(errors)
    validate_language_policy(errors)

    if errors:
        print("Integrity validation failed:")
        for e in errors:
            print(f" - {e}")
        return 1
    print("Integrity validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
