---
name: SKILL_UBKES_MASTER_PROTOCOL
description: "Canonical UBKES v2.0 extraction and governance protocol for turning books or long-form documents into source-grounded, machine-usable cognitive assets. Use when running a full UBKES extraction on fiction, non-fiction, hybrid texts, or corpora requiring provenance, validation, graph-ready structure, and renderer-ready outputs. Triggers: 'run UBKES', 'extract book into knowledge graph', 'book decomposition protocol', 'book to structured schema', 'fiction/non-fiction extraction', 'source-grounded book analysis', 'UBKES package generation'."
sepd_recipe: "[ Provenance-Governed Book Decomposition + Typed Phase Routing + Validation Gates ] -> [ Canonical UBKES Package ]"
act_as: "Senior Knowledge Extraction Architect and Protocol Governor"
mode: "Structured Extraction Governance"
stack_engine: "UBKES v2.0 schema, provenance anchors, validation gates, genre routing, derivation-mode policy"
output_extension: ".json / .md / .jsonl"
---

# SKILL_UBKES_MASTER_PROTOCOL

## Purpose

This skill is the master protocol for UBKES v2.0. It governs how a book, article collection, long-form text, or document corpus is converted into a source-grounded, machine-usable package.

It is not a renderer, not a vectorizer, and not a casual summarizer. It is the command layer that determines:

- what the source actually is
- how it should be modeled
- what can be extracted faithfully
- what must be labeled as inference
- what should be validated before downstream use
- what outputs are safe to emit

## Core Doctrine

### Rule 1. Extraction precedes synthesis
Extraction records what the text explicitly says or clearly supports.  
Synthesis records what follows, implies, generalizes, or connects beyond the source.

### Rule 2. Provenance is mandatory
High-value objects must retain anchors. Preferred anchors include:

- page span
- paragraph span
- chapter or article linkage
- scene linkage for fiction
- excerpt text when available

### Rule 3. Source fidelity must be declared
Every run must declare one of:

- `direct_text`
- `partial_text`
- `indirect_metadata_only`
- `synthetic_placeholder`

### Rule 4. Status must match fidelity
No run may be labeled fully verified if direct source access did not occur.

### Rule 5. Derivation mode must be explicit
Every important object should declare one of:

- `source_extracted`
- `normalized_reconstruction`
- `analyst_inference`
- `estimated_placeholder`

### Rule 6. Validation governs trust
A package may be rendered even if degraded, but downstream trust must inherit upstream validation state.

## When to Use

Use this skill when the task is to perform a full UBKES run on:

- books
- reports
- manuals
- anthologies
- reference works
- fiction
- non-fiction
- mixed corpora

Do not use this skill alone for:

- pure embedding export
- pure vector store creation
- stand-alone summarization
- isolated graph rendering without prior extraction

## UBKES Top-Level Package Contract

```json
{
  "package_meta": {},
  "book_identity": {},
  "phase_0_ingestion": {},
  "phase_1_bibliographic_intelligence": {},
  "phase_2_structural_decomposition": {},
  "phase_3_entity_and_concept_extraction": {},
  "phase_4_relationship_and_logic_extraction": {},
  "phase_5_event_and_timeline_extraction": {},
  "phase_6_procedural_and_operational_extraction": {},
  "phase_7_signal_ranking": {},
  "phase_8_graph_construction": {},
  "phase_9_output_rendering": {},
  "validation": {},
  "provenance_index": {},
  "export_index": {}
}
```

## Mandatory Governance Blocks

### Source Fidelity Block

```json
{
  "source_fidelity": "direct_text",
  "source_fidelity_notes": [],
  "text_materialization_status": "materialized"
}
```

### Derivation Mode Block

```json
{
  "derivation_mode": "source_extracted"
}
```

### Coverage Block

```json
{
  "coverage": {
    "estimated_total_objects": 120,
    "materialized_objects": 87,
    "coverage_ratio": 0.725,
    "coverage_status": "substantial_partial"
  }
}
```

## Phase Execution Order

### Phase 0. Ingestion Assessment and Normalization
Tasks:
- identify source type
- evaluate parse quality
- detect OCR or extraction artifacts
- create chunk and segmentation manifests
- declare materialization status

Outputs:
- source file descriptors
- normalization report
- chunk manifest
- segmentation summary
- source fidelity declaration

### Phase 1. Bibliographic Intelligence
Tasks:
- identify title, author, edition, publisher, year
- determine audience
- classify epistemic stance
- record publication context

Outputs:
- book identity object
- audience model
- epistemic profile
- historical context notes

### Phase 2. Structural Decomposition
Tasks:
- map front matter, body, back matter
- identify chapter/article/scene hierarchy
- classify structure type
- attach local summaries

Outputs:
- structural tree
- chapters or articles
- sections
- scenes when applicable

### Phase 3. Entity and Concept Extraction
Tasks:
- build registry of persons, characters, places, technologies, concepts, frameworks, factions, institutions, artifacts
- resolve aliases
- assign centrality

Outputs:
- entity registry
- concept registry
- alias map

### Phase 4. Relationship and Logic Extraction
Tasks:
- extract typed relations
- extract claims and subclaims
- detect dependencies and contradictions
- capture world rules for fiction

Outputs:
- relationship set
- claims
- arguments
- world rules

### Phase 5. Event and Timeline Extraction
Tasks:
- detect events
- attach participants
- model state changes
- construct timelines
- produce activity journals if appropriate

Outputs:
- events
- timelines
- activity journal
- scene-event links

### Phase 6. Procedural and Operational Extraction
Tasks:
- extract methods, procedures, heuristics, algorithms, doctrines, rituals, operational systems
- separate source procedure from normalized modern restatement

Outputs:
- procedures
- procedure steps
- strategies
- normalized procedure overlays if used

### Phase 7. Signal Ranking
Tasks:
- identify high-signal units
- score for centrality, novelty, actionability, adaptation value, cross-book value
- produce ranked list

Outputs:
- ranked signals
- density report

### Phase 8. Graph Construction
Tasks:
- create graph nodes from materialized objects
- create typed edges
- validate graph integrity
- cluster nodes

Outputs:
- graphs
- nodes
- edges
- graph validation report

### Phase 9. Output Rendering Contract
Tasks:
- prepare render manifests only from validated upstream inputs
- declare render trust inheritance

Outputs:
- render targets
- render profiles
- export manifests

### Phase 10. Cross-Book Synthesis
Only run when multiple sources are present.

Tasks:
- compare concepts
- detect contradictions
- align archetypes
- compare technology forecasts
- build consensus or delta outputs

Outputs:
- overlap reports
- contradiction matrices
- archetype maps
- synthesis artifacts

## Status Ladder

Allowed run statuses:

- `complete_verified`
- `complete_with_minor_gaps`
- `degraded_partial`
- `metadata_only_stub`
- `invalid_run`

### Status Rules

`complete_verified`
- requires `source_fidelity = direct_text`
- validator pass
- no unresolved IDs
- materialized anchors exist

`complete_with_minor_gaps`
- direct or partial text available
- minor omissions allowed
- core objects and anchors exist

`degraded_partial`
- usable extraction with major constraints
- incomplete or coarse provenance
- some phases sample-only or partially reconstructed

`metadata_only_stub`
- metadata available but source text inaccessible
- package may only support limited structural or bibliographic operations

`invalid_run`
- broken referential integrity
- contradictory materialization claims
- fabricated extraction posing as source-grounded output

## Output Modes

### `json_strict`
Return only valid JSON conforming to the canonical schema.

### `markdown_audit`
Return schema-mirrored markdown for inspection, especially when the source is large or partial.

### `split_phase_json`
Return one valid JSON object per phase plus a linking manifest.

## Validation Gates

Before finalizing, verify all of the following:

- every referenced ID resolves
- every anchor reference resolves
- no count claims exceed materialized arrays unless marked estimated or deferred
- confidence values obey source-fidelity caps
- derivation modes exist where inference or estimation occurred
- render trust inherits upstream integrity
- status matches fidelity and validation result

## Confidence Caps

Recommended maximums:

| Source Fidelity | Max Confidence |
|---|---:|
| direct_text | 0.98 |
| partial_text | 0.85 |
| indirect_metadata_only | 0.70 |
| synthetic_placeholder | 0.40 |

No `certainty = 1.0` without direct anchored evidence.

## Failure Safety Rules

If source access is blocked or incomplete:

1. downgrade source fidelity
2. downgrade package status
3. prohibit full completion claims
4. mark estimates explicitly
5. do not invent chunk manifests, claims, or entities to satisfy schema aesthetics
6. if needed, emit a metadata-only or degraded partial package

## Recommended Companion Skills

- `SKILL_UBKES_REFERENCE_WORK_ADAPTER`
- `SKILL_UBKES_FICTION_NARRATIVE_EXTRACT`
- `SKILL_UBKES_GRAPH_BUILDER`
- `SKILL_NLP_BOOK_VECTORIZE`

## Best Use Pattern

1. Run this master protocol first
2. Attach a genre or corpus adapter if needed
3. Validate the package
4. Only then route to graph builder, renderer, or vectorizer
