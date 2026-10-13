# RAG Research Assistant — Discipline Guide

> How to adapt this workflow, and where its limits are.

## What this workflow assumes

This workflow assumes a corpus of machine-readable PDFs. It assumes the
questions are fact-retrieval, not opinion synthesis. It assumes the LLM
is a reasoning aid, not an authority.

## Research

Literature review workflows benefit from this tool by accelerating the
navigation of a reading list. The critique that RAG doesn't replace
reading — it helps you navigate. Citation quality depends on PDF quality.
Discuss: how do you verify a claim the model makes? What's the
difference between "the paper says X" and "the model thinks the paper
says X"? The workflow gives you the passage; you decide what it means.

## Teaching

Course reading lists become queryable resources. Students querying
primary sources can retrieve relevant passages instantly. The ethics of
using RAG in academic work — citation, attribution, the difference
between understanding and retrieval. This tool makes the distinction
visible: it returns the source text, not an opaque answer.

## Known limitations

- **PDF extraction quality.** Two-column academic papers, tables, and
  equations confuse `pypdf`. Extraction is often lossy.
- **Chunking is crude.** Fixed-size character chunks split mid-sentence.
  Semantic chunking is a known improvement.
- **Embedding model size.** `all-MiniLM-L6-v2` is fast but small. For
  technical domains, a larger model may work better.
- **Retrieval ≠ comprehension.** The system retrieves passages, not
  arguments. It will not synthesise a paper's thesis unless the thesis
  is stated in one passage.
- **Hallucination is possible.** The LLM can produce claims not supported
  by the retrieved chunks. Always verify against the citation.
- **No chunk-level provenance.** Every chunk cites its source file and
  page, but not the paragraph. Fine-grained provenance is future work.

## Extending this workflow

- **Better chunking.** Use the paper's own section headings.
- **Reranking.** Add a cross-encoder reranker after retrieval.
- **Domain embeddings.** Fine-tune on the corpus domain.
- **Multi-query.** Generate variations of the question and merge results.
- **Evaluation.** Add a small test set of question/answer pairs to
  measure retrieval quality.

## Provocation

Retrieval is not understanding. The workflow helps you find the
sentence that says the thing. It does not tell you whether the thing
is true. That distinction is the whole game.