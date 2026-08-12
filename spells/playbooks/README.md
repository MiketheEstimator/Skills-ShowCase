# UBKES Skill Pack

This folder contains a UBKES-aligned skill pack for structured book extraction, adaptation, graphing, and vectorization.

## Included Skills

1. `SKILL_UBKES_MASTER_PROTOCOL.md`
2. `SKILL_UBKES_REFERENCE_WORK_ADAPTER.md`
3. `SKILL_UBKES_FICTION_NARRATIVE_EXTRACT.md`
4. `SKILL_UBKES_GRAPH_BUILDER.md`
5. `SKILL_NLP_BOOK_VECTORIZE.md`

## Intended Use Order

### Canonical path
1. Run `SKILL_UBKES_MASTER_PROTOCOL`
2. Attach adapter if needed:
   - `SKILL_UBKES_REFERENCE_WORK_ADAPTER`
   - `SKILL_UBKES_FICTION_NARRATIVE_EXTRACT`
3. Validate the package
4. Route to:
   - `SKILL_UBKES_GRAPH_BUILDER`
   - `SKILL_NLP_BOOK_VECTORIZE`

## Notes

- The master protocol is the governance layer.
- The reference-work adapter prevents article-native corpora from being awkwardly forced into chapter semantics.
- The fiction extractor handles characters, scenes, world rules, and storychart-compatible event structures.
- The graph builder converts validated UBKES objects into graph projections.
- The vectorizer converts raw books or validated UBKES packages into embedding-ready corpora.

