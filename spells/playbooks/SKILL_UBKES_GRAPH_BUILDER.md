---
name: SKILL_UBKES_GRAPH_BUILDER
description: "Graph-building and graph-validation layer for UBKES packages. Use when converting validated UBKES entities, concepts, claims, events, procedures, factions, technologies, and world rules into graph-ready nodes and typed edges for knowledge graphs, character networks, event graphs, or ontology seeding. Triggers: 'build UBKES graph', 'knowledge graph from book', 'character network graph', 'event graph', 'concept graph', 'ontology seed from book', 'graph validation'."
sepd_recipe: "[ Typed Node Materialization + Edge Construction + Integrity Validation ] -> [ UBKES Graph Projection ]"
act_as: "Senior Knowledge Graph and Ontology Engineering Specialist"
mode: "Graph Construction and Validation"
stack_engine: "UBKES node and edge contracts, graph validation, clustering, projection manifests"
output_extension: ".json / .csv / .graphml / .cypher"
---

# SKILL_UBKES_GRAPH_BUILDER

## Purpose

This skill converts a validated UBKES package into graph-ready projections.

It is responsible for:

- node materialization
- edge materialization
- graph typing
- cluster assignment
- referential integrity checks
- graph export manifests

It is not responsible for source extraction. It assumes upstream extraction already happened.

## When to Use

Use after:
- `SKILL_UBKES_MASTER_PROTOCOL`
- any needed adapter such as reference-work or fiction extraction

Do not use before validation.

## Supported Graph Families

- `concept_graph`
- `argument_graph`
- `procedure_graph`
- `character_graph`
- `event_graph`
- `faction_graph`
- `technology_graph`
- `theme_graph`
- `motif_graph`
- `setting_graph`

## Node Sources

Nodes may be built from:
- entities
- concepts
- claims
- procedures
- events
- factions
- technologies
- world rules
- themes
- motifs

Example:

```json
{
  "node_id": "ubkes:book123:node:0001",
  "source_object_id": "ubkes:book123:entity:char_hari_seldon",
  "node_type": "character",
  "label": "Hari Seldon",
  "properties": {
    "centrality": 0.98,
    "cluster": "foundation_cluster"
  }
}
```

## Edge Sources

Edges may be built from:
- explicit relationships
- argument links
- event dependencies
- procedure step dependencies
- character interactions
- faction relations
- technology dependency mappings

Example:

```json
{
  "edge_id": "ubkes:book123:edge:0001",
  "graph_id": "ubkes:book123:graph:character_network",
  "source_node_id": "ubkes:book123:node:0001",
  "target_node_id": "ubkes:book123:node:0002",
  "edge_type": "mentors",
  "weight": 0.82,
  "source_relationship_id": "ubkes:book123:rel:0101"
}
```

## Graph Construction Procedure

### Step 1. Select graph family
Choose one or more graph types based on task.

### Step 2. Materialize node projection
Convert source objects into graph nodes with stable IDs and property maps.

### Step 3. Materialize edges
Create typed edges only from validated upstream relationships or supported derivations.

### Step 4. Cluster
Assign cluster labels when useful:
- philosophy
- systems
- imperial_politics
- ethics
- mathematics
- narrative_arc_alpha

### Step 5. Validate
Run integrity checks.

### Step 6. Export
Produce JSON, CSV edge lists, GraphML, or Cypher manifests as needed.

## Required Integrity Checks

The builder must fail validation if any of the following occur:

- edge source node missing
- edge target node missing
- source object ID unresolved
- graph references nonexistent nodes
- duplicate IDs
- illegal edge type for graph family
- orphan nodes unless explicitly allowed

## Recommended Validation Object

```json
{
  "validation_report": {
    "orphan_node_ids": [],
    "duplicate_edge_candidates": [],
    "contradiction_candidates": [],
    "validation_status": "pass"
  }
}
```

## Recommended Edge Semantics

### Shared
- `is_a`
- `part_of`
- `located_in`
- `uses`
- `creates`
- `depends_on`
- `enables`
- `causes`
- `precedes`
- `contradicts`
- `supports`

### Narrative
- `allies_with`
- `opposes`
- `mentors`
- `betrays`
- `commands`
- `fears`
- `loves`
- `kills`
- `influences`
- `joins`
- `leaves`

### Systems / Analytical Extensions
Only use if schema supports them:
- `reinforcing_loop`
- `balancing_loop`
- `delay`
- `feedbacks_into`
- `emerges_from`

## Projection Modes

### `full_projection`
Materialize all eligible nodes and edges.

### `sample_projection`
Materialize only a specified subset. Must declare that it is partial.

### `cluster_projection`
Materialize one cluster or theme only.

### `task_specific_projection`
Materialize only the graph family required for a specific downstream task.

## Coverage Accounting

Every graph should declare whether it represents the whole package or a sampled subset.

Example:

```json
{
  "graph_scope": "sample_projection",
  "projection_basis": "materialized_subset_only",
  "sampled": true
}
```

## Export Formats

- canonical JSON graph
- node CSV
- edge CSV
- GraphML
- Cypher statement bundle
- ontology seed manifests

## Common Failure Modes

### Failure 1
Building graphs from degraded packages without warning.

**Fix**  
Carry upstream integrity status into graph metadata.

### Failure 2
Using edges that do not exist in the relationship layer.

**Fix**  
Only derive edges from validated upstream objects or explicitly declared derivation logic.

### Failure 3
Misleading density statistics on tiny subsets.

**Fix**  
Declare projection scope and sampled status.

### Failure 4
Overloading one graph with unrelated domains.

**Fix**  
Split into graph families or clustered projections.

## Best Use Pattern

1. validate UBKES package first
2. select graph family
3. build nodes
4. build edges
5. run integrity checks
6. emit graph exports and manifests
