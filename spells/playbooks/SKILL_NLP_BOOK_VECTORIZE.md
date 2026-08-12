---
name: SKILL_NLP_BOOK_VECTORIZE
description: "UBKES-aligned pipeline for ingesting books and long-form documents, cleaning text, preserving provenance, extracting high-signal passages, chunking for semantic coherence, vectorizing into embedding-ready corpora, and exporting datasets for RAG, retrieval, analytics, or fine-tuning. Use after direct-source access is available, or after a validated UBKES package exists. Triggers: 'book vectorization', 'UBKES to embeddings', 'book to FAISS', 'book to Chroma', 'RAG pipeline from book', 'JSONL training data', 'high-signal corpus export', 'knowledge distillation corpus', 'fine-tune on book', 'book embeddings'."
sepd_recipe: "[ Provenance-Aware Text Normalization + Semantic Chunking + Embedding Export ] -> [ UBKES-Compatible Vector Corpus ]"
act_as: "Senior NLP and Knowledge Engineering Specialist"
mode: "Code Generation (Python 3)"
stack_engine: "PyMuPDF, ebooklib, BeautifulSoup, LangChain splitters, SentenceTransformers, FAISS, ChromaDB, tiktoken"
output_extension: ".jsonl / .parquet / .faiss / .json"
---

# SKILL_NLP_BOOK_VECTORIZE

## Purpose

This skill converts books or validated UBKES packages into vectorized corpora suitable for:

- RAG systems
- semantic search
- retrieval pipelines
- fine-tuning corpora
- knowledge distillation datasets
- downstream analytics

It is a companion skill, not the UBKES master protocol.

## Best Position in the UBKES Stack

Use this skill in one of two ways:

### Path A. Raw Source to Vector Corpus
For direct-source workflows where the goal is embeddings, retrieval, or training data.

### Path B. UBKES Package to Vector Corpus
For higher-rigor workflows where source extraction has already been validated and you want to vectorize:
- claims
- concepts
- procedures
- events
- signals
- scene summaries
- world rules

Path B is preferred for trust-sensitive systems.

## Non-Negotiable Rules

1. Never pretend to have direct text access if source fidelity is degraded.
2. Track provenance on every chunk.
3. Track derivation mode on every chunk.
4. Distinguish extracted text from normalized restatements.
5. Do not emit vector stores from metadata-only stubs as if they were full corpora.
6. Deduplicate near-duplicates before storage.
7. Token-count all chunks before embedding.
8. Record source metadata on every chunk.

## Required Metadata Per Chunk

Minimum recommended metadata:

```json
{
  "chunk_id": "ubkes:book123:chunk:0001",
  "book_id": "book123",
  "book_title": "Example Book",
  "chapter_or_article": "Chapter 1",
  "page_start": 12,
  "page_end": 13,
  "paragraph_start": 4,
  "paragraph_end": 8,
  "anchor_ids": [
    "ubkes:book123:anchor:0001"
  ],
  "source_fidelity": "direct_text",
  "derivation_mode": "source_extracted",
  "signal_score": 0.81
}
```

## Recommended Input Modes

### Mode 1. Raw Book Ingestion
Inputs:
- PDF
- EPUB
- TXT
- Markdown

### Mode 2. UBKES Package Ingestion
Inputs:
- `phase_3` entities and concepts
- `phase_4` claims and relationships
- `phase_5` events
- `phase_6` procedures
- `phase_7` signals

## Recommended Chunk Families

### Raw Text Chunks
Best for broad retrieval.

### Claim Chunks
Each chunk centered on one claim plus support.

### Concept Chunks
Definition and related examples.

### Procedure Chunks
Procedure plus ordered steps.

### Event Chunks
Event summary plus participants and state changes.

### Fiction Chunks
- scene chunks
- character profile chunks
- world-rule chunks
- technology chunks

## Source Fidelity Policy

Allowed values:

- `direct_text`
- `partial_text`
- `indirect_metadata_only`
- `synthetic_placeholder`

### Policy Rule
If source fidelity is `indirect_metadata_only` or `synthetic_placeholder`, do not present the output as a canonical retrieval corpus.

## Derivation Mode Policy

Allowed values:

- `source_extracted`
- `normalized_reconstruction`
- `analyst_inference`
- `estimated_placeholder`

These fields must be preserved into JSONL, parquet, and vector sidecar metadata when possible.

## Pipeline Outline

### Step 1. Ingest
- PDF via PyMuPDF
- EPUB via ebooklib and BeautifulSoup
- TXT/Markdown via `pathlib`

### Step 2. Normalize
- Unicode normalization
- dehyphenation
- footer/header removal
- noise-line filtering

### Step 3. Chunk
- recursive semantic-aware split
- or chunk from validated UBKES objects

### Step 4. Score
- lexical density
- type-token ratio
- keyword anchoring
- information density
- or import UBKES `signal_score`

### Step 5. Filter
- remove low-signal fragments
- remove boilerplate
- remove duplicates

### Step 6. Embed
- SentenceTransformers or other embedding model
- normalize vectors

### Step 7. Store
- FAISS
- ChromaDB
- sidecar JSONL / parquet

### Step 8. Validate
- token length checks
- parse checks
- metadata completeness
- provenance completeness
- retrieval spot checks

## Recommended Output Families

- FAISS index
- Chroma collection
- JSONL training corpus
- parquet training corpus
- chunk manifest JSON
- pipeline report JSON

## UBKES Compatibility Extension

When vectorizing from a UBKES package, preserve source object identity.

Example:

```json
{
  "chunk_id": "ubkes:book123:vector_chunk:0001",
  "source_object_type": "claim",
  "source_object_id": "ubkes:book123:claim:0001",
  "text": "Large populations can be modeled probabilistically...",
  "anchor_ids": [
    "ubkes:book123:anchor:0103"
  ],
  "source_fidelity": "direct_text",
  "derivation_mode": "source_extracted"
}
```

## Validation Rules

- every vector chunk must have a stable ID
- every referenced anchor must resolve
- no unresolved source object IDs
- no count mismatch between manifest and materialized chunk set
- no training record with empty text
- no misleading trust status if source fidelity is degraded

## Best Embedding Use Cases

### Non-Fiction
- concept retrieval
- claim retrieval
- procedure search
- training corpus creation

### Fiction
- scene retrieval
- character memory banks
- world-rule retrieval
- adaptation support
- narrative search

## Common Failure Modes

### Failure 1
Embedding raw OCR garbage.

**Fix**  
Run normalization and QA first.

### Failure 2
Losing provenance during chunk export.

**Fix**  
Carry anchor and page metadata on every chunk.

### Failure 3
Mixing extracted text and analyst synthesis without marking them.

**Fix**  
Use `derivation_mode`.

### Failure 4
Vectorizing metadata-only stubs as if they were canonical corpora.

**Fix**  
Downgrade trust and label corpus fidelity explicitly.

## Recommended Companion Skills

- `SKILL_UBKES_MASTER_PROTOCOL`
- `SKILL_UBKES_GRAPH_BUILDER`
- `SKILL_UBKES_FICTION_NARRATIVE_EXTRACT`
- `SKILL_UBKES_REFERENCE_WORK_ADAPTER`
