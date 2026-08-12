---
name: SKILL_UBKES_FICTION_NARRATIVE_EXTRACT
description: "UBKES fiction-mode extraction adapter for novels, stories, scripts, epics, speculative fiction, fantasy, science fiction, and narrative corpora. Use when extracting characters, scenes, factions, world rules, technologies, events, timelines, motifs, adaptation assets, and storychart-compatible activity structures from fiction. Triggers: 'fiction UBKES', 'novel extraction', 'character graph', 'scene extraction', 'worldbuilding schema', 'storychart narrative graph', 'fan fiction fidelity pack', 'book to game narrative'."
sepd_recipe: "[ Narrative Decomposition + World Rule Extraction + Character/Event Graphing ] -> [ Fiction-Ready UBKES Package ]"
act_as: "Senior Narrative Intelligence and Story Systems Analyst"
mode: "Fiction Extraction and Narrative Structuring"
stack_engine: "UBKES v2.0 fiction mode, character profiles, scene maps, event registries, world-rule logic"
output_extension: ".json / .md / .jsonl"
---

# SKILL_UBKES_FICTION_NARRATIVE_EXTRACT

## Purpose

This skill adapts UBKES for fiction and narrative corpora. It extracts the architecture of story rather than treating fiction as a weak form of summary.

It is designed for:

- novels
- short stories
- science fiction
- fantasy
- literary fiction
- epics
- scripts
- worldbuilding-heavy series
- adaptation and game-design pipelines

## Core Output Families

### Character Intelligence
- names and aliases
- roles
- affiliations
- goals
- fears
- relationships
- voice profiles
- arc states

### Scene Intelligence
- scene boundaries
- POV
- location
- participants
- event type
- stakes
- state change

### World Intelligence
- social systems
- factions
- technologies
- magic or physical rules
- political structures
- constraints and prohibitions

### Narrative Intelligence
- event graph
- scene graph
- timeline
- motif network
- faction interaction map
- storychart-compatible activity journal

## When to Use

Use when the source is primarily narrative or worldbuilding-driven.

Do not use as the only skill when:
- the task is pure embedding export
- the task is only bibliographic metadata
- the source is article-native and non-narrative
- the task is only graph rendering from an existing validated package

## Fiction-Specific Doctrine

### Rule 1. Scenes are first-class units
A scene is often more meaningful than a chapter for local causality.

### Rule 2. Character state changes matter
Track not just who appears, but how they change.

### Rule 3. World rules are not optional
Speculative fiction often hinges on rules, constraints, technologies, and exceptions.

### Rule 4. Narrative extraction is not fanfic generation
Stay source-grounded during extraction. Adaptation or derivative use comes later.

## Preferred Structural Objects

```json
{
  "scenes": [
    {
      "scene_id": "ubkes:novel01:scene:0001",
      "chapter_id": "ubkes:novel01:chapter:01",
      "scene_order": 1,
      "page_start": 1,
      "page_end": 3,
      "location_primary": "Trantor",
      "time_label": "present_narrative",
      "pov_character_id": "ubkes:novel01:entity:char_gaal_dornick",
      "scene_summary": "Arrival and first exposure to imperial center."
    }
  ]
}
```

## Required Fiction Registries

### Character Registry
Fields:
- `character_id`
- `canonical_name`
- `aliases`
- `roles`
- `affiliations`
- `first_appearance`
- `centrality`
- `voice_profile`
- `motivation_profile`
- `arc_profile`

### World Rule Registry
Fields:
- `world_rule_id`
- `rule_text`
- `rule_type`
- `source_anchor_ids`
- `violations_detected`

### Technology Registry
Fields:
- `technology_entity_id`
- `fictional_capability`
- `narrative_function`
- `real_world_analog`
- `realization_status`

## Storychart Compatibility Layer

When event flow is important, produce an activity journal that can support:

- actor channels
- team channels
- activity connectors
- time columns
- action glyphs such as `progress`, `join`, `disjoin`, `gathering`, `conflict`

Example:

```json
{
  "activity_journal": [
    {
      "activity_id": "ubkes:novel01:activity:0001",
      "actor_ids": [
        "ubkes:novel01:entity:char_gaal_dornick"
      ],
      "action_glyph_type": "progress",
      "time_label": "narrative_present",
      "location_id": "ubkes:novel01:entity:place_trantor",
      "event_name": "Arrival",
      "result_text": "Entry into imperial world",
      "event_id": "ubkes:novel01:event:0001"
    }
  ]
}
```

## Event Types Useful in Fiction

- `arrival`
- `departure`
- `meeting`
- `conversation`
- `discovery`
- `conflict`
- `betrayal`
- `battle`
- `creation`
- `decision`
- `revelation`
- `resolution`
- `join`
- `disjoin`
- `gathering`
- `progress`

## Recommended Derived Deliverables

After extraction and validation, this skill can support:

- character bible
- scene bible
- faction map
- storychart
- adaptation pack
- fan fiction fidelity pack
- game narrative document
- technology forecast matrix
- voice-cast sheet

## Guardrails

### No hidden synthesis
If inferring unstated motivations, mark them as `analyst_inference`.

### No scene invention
Only materialize scenes justified by the source structure.

### No rule inflation
Do not overformalize one-off narrative details into universal world rules without support.

### No adaptation drift during extraction
Do not rewrite the story while supposedly extracting it.

## Common Failure Modes

### Failure 1
Treating chapters as the only units.

**Fix**  
Materialize scenes.

### Failure 2
Extracting characters without relationship arcs.

**Fix**  
Pair character registry with event and relationship layers.

### Failure 3
Ignoring world rules in speculative fiction.

**Fix**  
Always extract constraint logic, technology rules, or system rules.

### Failure 4
Jumping straight from fiction to fan-fiction generation.

**Fix**  
First build a validated canonical package, then route to adaptation or derivative skills.

## Best Use Pattern

1. Detect fiction mode
2. Segment chapters and scenes
3. Build character and world registries
4. Extract relationships and events
5. Build scene and event graphs
6. Validate
7. Route to storychart, adaptation, or vectorization as needed
