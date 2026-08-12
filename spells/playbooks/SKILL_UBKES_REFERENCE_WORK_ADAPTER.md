---
name: SKILL_UBKES_REFERENCE_WORK_ADAPTER
description: "UBKES adapter for encyclopedias, dictionaries, alphabetical reference works, handbooks, article compendia, and modular non-narrative corpora. Use when a source is not naturally chapter-driven and must be modeled as article-native rather than narrative or thematic chapters. Triggers: 'encyclopedia extraction', 'dictionary to schema', 'reference work UBKES', 'alphabetical article corpus', 'article-native decomposition', 'Britannica extraction', 'handbook structure adapter'."
sepd_recipe: "[ Reference-Work Structural Normalization + Article-Native Decomposition + Provenance Discipline ] -> [ UBKES-Compatible Reference Package ]"
act_as: "Senior Reference Corpus Modeling Specialist"
mode: "Schema Adaptation and Extraction Governance"
stack_engine: "UBKES v2.0 reference adapter, article-level registries, provenance quality controls"
output_extension: ".json / .md"
---

# SKILL_UBKES_REFERENCE_WORK_ADAPTER

## Purpose

This skill adapts UBKES to corpora that are naturally organized as articles, entries, lemmas, headwords, or indexed modules rather than chapters.

Examples:

- encyclopedias
- dictionaries
- glossaries
- technical handbooks
- alphabetical compendia
- article-based proceedings

## Why It Exists

Standard UBKES chapter-based decomposition becomes awkward for reference works. If forced into chapter semantics, the system risks:

- false chapter modeling
- misleading timelines
- overconfident structural claims
- poor provenance granularity
- synthetic reconstruction masquerading as extraction

This adapter fixes that.

## Core Structural Shift

Replace chapter-first thinking with article-first thinking.

### Preferred Object Family

```json
{
  "structure_type": "article_reference",
  "body_structure": {
    "articles": [],
    "sections": [],
    "entries": []
  }
}
```

### Required Structural Extensions

Add support for:

- `article_id`
- `entry_id`
- `headword`
- `alphabetic_range`
- `article_function`
- `article_scope`
- `reference_timeline_type`

## When to Use

Use this adapter when the source has any of the following properties:

- alphabetically sorted entries
- multiple independent articles
- many short or medium stand-alone units
- cross-domain topical coverage
- inconsistent narrative continuity
- article headers functioning as primary segmentation boundaries

## Structure Rules

### Rule 1. Articles are not chapters unless explicitly stated
Do not force an encyclopedia article into a `chapter_id` if the source is article-native.

### Rule 2. Entry boundaries are first-class anchors
Use headwords, entry titles, and article start/end boundaries as provenance anchors.

### Rule 3. Timelines are local, not global by default
A reference work may discuss many historical timelines. Do not imply a single book-wide chronological timeline unless the source truly has one.

### Rule 4. Coverage must be explicit
If only a subset of articles is materialized, declare the ratio.

## Recommended Structural Schema

```json
{
  "body_structure": {
    "articles": [
      {
        "article_id": "ubkes:ref001:article:ether",
        "headword": "Ether",
        "article_order": 60,
        "alphabetic_position": "E",
        "page_start": 200,
        "page_end": 210,
        "summary_short": "Physics overview of ether theory.",
        "article_function": "technical_entry",
        "section_ids": [
          "ubkes:ref001:section:ether.1"
        ],
        "anchor_ids": [
          "ubkes:ref001:anchor:ether.p200"
        ]
      }
    ]
  }
}
```

## Allowed `article_function` Enums

- `reference_entry`
- `survey_entry`
- `technical_entry`
- `historical_entry`
- `biographical_entry`
- `definition_entry`
- `cross_reference_entry`
- `thematic_entry`

## Reference-Work Provenance Recommendations

Minimum preferred anchor:

```json
{
  "anchor_id": "ubkes:ref001:anchor:ether.p203.par3",
  "article_id": "ubkes:ref001:article:ether",
  "page_start": 203,
  "page_end": 203,
  "paragraph_start": 3,
  "paragraph_end": 4,
  "excerpt_text": "A continuous medium whose primary function is to transmit waves of light."
}
```

## Extraction Priorities

### High Priority
- article identity
- headword
- article summary
- core concepts
- named persons
- technical or philosophical claims
- article-local bibliographic evidence
- cross-references

### Medium Priority
- historical events described within article
- procedures or methods
- internal taxonomies
- article-local timelines

### Low Priority
- book-wide narrative coherence
- fictional scene mapping
- storychart outputs unless the source actually narrates events

## Timeline Policy

Use one of:

- `historical_reference`
- `article_local_historical`
- `none`

Do not default to `primary narrative timeline`.

## Validation Rules

- if `structure_type = article_reference`, at least one `article_id` must exist
- article counts may be estimated only if marked estimated
- headword and article title should not be conflated silently when they differ
- global chronology must not be implied from heterogeneous entries
- render layers must know whether output is article-local or corpus-wide

## Recommended Outputs

Good outputs for this adapter:
- concept glossary
- article registry
- cross-reference map
- historical signal leaderboard
- local article graphs
- bibliographic intelligence
- sampled educational brief

Usually poor fits unless explicitly justified:
- global narrative timeline
- storychart
- scene bible
- adaptation pack

## Common Failure Modes

### Failure 1
Forcing articles into chapter arrays only.

**Fix**  
Add article-native structure objects.

### Failure 2
Creating a single global event timeline for unrelated entries.

**Fix**  
Keep timelines local to article or historical topic.

### Failure 3
Overclaiming completeness from a few sampled entries.

**Fix**  
Add explicit coverage accounting.

### Failure 4
Using coarse anchors like only `anchor:ch60`.

**Fix**  
Use article, page, paragraph, and excerpt anchors.

## Best Use Pattern

1. Detect article-native structure
2. Switch to this adapter
3. Materialize article registry
4. Extract concepts, entities, and article-local claims
5. Build local or clustered graphs
6. Render only outputs appropriate to reference corpora
