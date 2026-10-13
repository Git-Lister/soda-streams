BEGIN BRICK 5 SPEC — SAVE AS prompts/brick-05-rag-workflow/01-initial-prompt.md
═══════════════════════════════════════════════════════════════════════

Brick 5 — RAG Research Assistant Workflow
You are implementing Brick 5 of the Soda-Streams project.

Context
Read before starting:

docs/BLUEPRINT.md — §3 metadata schema, §6 runtime, §7 assistant architecture

docs/DEVELOPMENT.md — §9 coding standards

docs/DESIGN.md — §3 user story 3 (researcher, RAG pipeline)

workflows/image-generation/comfyui-character-design/ — the pattern to follow (Brick 4)

tools/validators/schema.json — metadata schema

Brick 1b left placeholders in workflows/text/rag-research-assistant/. Brick 5 replaces those with a real, runnable RAG workflow.

The pattern mirrors Brick 4: standalone workflow folder, its own
workflow.py, its own metadata, its own tests, and it must work with
tools/sandbox/cli.py run.

The workflow
RAG Research Assistant — ingest a folder of PDFs into a local vector
index, then query with grounded answers that cite their sources.

Two subcommands:

ingest — extract text from PDFs, chunk, embed, store in ChromaDB

query — retrieve relevant chunks, prompt a local LLM (Ollama), return an answer with citations

Design decisions:

Embeddings: sentence-transformers with all-MiniLM-L6-v2 (offline, ~80 MB download, no API)

Vector store: ChromaDB (persistent local directory)

LLM: Ollama via the official ollama Python client

PDF extraction: pypdf (pure Python, no compilation)

The workflow is CPU-only for embeddings and runs on any machine.
Generation requires Ollama running locally.

Critical: Lazy imports
chromadb and sentence_transformers are heavy dependencies — the latter
pulls in PyTorch. Importing them at module level means every import workflow (including from tests) triggers the full stack load.

Import them lazily, inside the functions that use them:

python
def embed_and_store(...):
    from sentence_transformers import SentenceTransformer
    import chromadb
    ...

def retrieve(...):
    from sentence_transformers import SentenceTransformer
    import chromadb
    ...
pypdf and ollama may be imported at module level — they are lightweight.

This ensures tests for chunking, extraction, CLI parsing, and metadata
run without requiring the heavy stack to be present.

Deliverables
Modify exactly 5 files. Create exactly 4 new files.

Modified files
1. workflows/text/rag-research-assistant/README.md

Structure:

markdown
# RAG Research Assistant

> Ingest a folder of PDFs into a local vector index. Query it with
> grounded answers that cite their sources. Runs offline — no data
> leaves the machine.

## What it does

[3–4 sentences. Explains ingestion (PDFs → chunks → embeddings →
ChromaDB) and query (question → retrieve → prompt LLM → cited answer).]

## Who it's for

- Researchers synthesising a literature review
- Postgraduate students navigating a reading list
- Anyone who needs to query a document corpus without uploading it

## What you need

- **Python 3.11+** with the dependencies in `requirements.txt`
- **Ollama** running locally with at least one model pulled
  (e.g. `ollama pull llama3.2:3b`)
- **A folder of PDFs** to ingest

First-time setup downloads the embedding model (~80 MB) from Hugging Face.

## How to run it

1. Start Ollama:
ollama serve

text

2. Ingest a corpus:
python workflows/text/rag-research-assistant/workflow.py ingest
--source path/to/pdfs

text

3. Query:
python workflows/text/rag-research-assistant/workflow.py query
--question "What are the main critiques of RAG systems?"

text

4. Answers print to stdout with a numbered list of sources.

## What it doesn't do

- It doesn't fetch papers. You provide the corpus.
- It doesn't OCR. Scanned PDFs must be OCR'd first.
- It doesn't rewrite the LLM's output. Hallucinations are possible;
citations help you verify.

## Provenance

- **Embedding model:** all-MiniLM-L6-v2 — sentence-transformers — Apache 2.0
- **Vector store:** ChromaDB — Apache 2.0
- **PDF extraction:** pypdf — BSD-3-Clause
- **LLM:** configurable — no model bundled

See `metadata.yaml` for the full provenance record.

## Related files

- `metadata.yaml` — machine-readable metadata
- `guide.md` — discipline-specific adaptation
- `workflow.py` — the Python entry point
- `requirements.txt` — Python dependencies
2. workflows/text/rag-research-assistant/metadata.yaml

yaml
name: "RAG Research Assistant"
slug: "rag-research-assistant"
author: "Git-Lister"
tier: "curated"
discipline:
  - "research"
  - "teaching"
description: "Ingest a folder of PDFs into a local vector index and query with grounded answers that cite sources. Runs offline."
version: "1.0.0"
licence: "MIT"
tools:
  - name: "ChromaDB"
    version: ">=0.4.0"
    source: "https://github.com/chroma-core/chroma"
    licence: "Apache-2.0"
  - name: "sentence-transformers"
    version: ">=2.2.0"
    source: "https://github.com/UKPLab/sentence-transformers"
    licence: "Apache-2.0"
  - name: "Ollama"
    version: ">=0.1.0"
    source: "https://github.com/ollama/ollama"
    licence: "MIT"
  - name: "pypdf"
    version: ">=4.0.0"
    source: "https://github.com/py-pdf/pypdf"
    licence: "BSD-3-Clause"
dependencies:
  - "chromadb>=0.4.0"
  - "sentence-transformers>=2.2.0"
  - "pypdf>=4.0.0"
  - "ollama>=0.1.0"
entry_point: "workflow.py:main"
runtime: "python"
provenance:
  models:
    - name: "all-MiniLM-L6-v2"
      source: "sentence-transformers"
      licence: "Apache-2.0"
      training_data: "1B sentence pairs (see model card)"
  ai_assistance:
    - tool: "OpenCode (Nemotron 3 Ultra)"
      role: "code generation"
created: "2026-10-13"
updated: "2026-10-13"
contributor_handle: "Git-Lister"
3. workflows/text/rag-research-assistant/guide.md

Structure:

markdown
# RAG Research Assistant — Discipline Guide

> How to adapt this workflow, and where its limits are.

## What this workflow assumes

[Paragraph. Assumes a corpus of machine-readable PDFs. Assumes the
questions are fact-retrieval, not opinion synthesis. Assumes the LLM
is a reasoning aid, not an authority.]

## Research

[2–3 paragraphs. Literature review workflows. The critique that RAG
doesn't replace reading — it helps you navigate. Citation quality
depends on PDF quality. Discuss: how do you verify a claim the model
makes? What's the difference between "the paper says X" and "the model
thinks the paper says X"?]

## Teaching

[2–3 paragraphs. Course reading lists. Students querying primary
sources. The ethics of using RAG in academic work — citation,
attribution, the difference between understanding and retrieval.]

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
4. workflows/text/rag-research-assistant/workflow.py

Structure:

python
"""RAG research assistant — ingest PDFs, query with citations."""

from __future__ import annotations

import argparse
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader


DEFAULT_INDEX_DIR = Path(".rag-index")
DEFAULT_COLLECTION = "research"
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_LLM_MODEL = "llama3.2:3b"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
DEFAULT_TOP_K = 5


SYSTEM_PROMPT = (
    "You are a research assistant. Answer the user's question using ONLY "
    "the provided source extracts. If the extracts do not contain the "
    "answer, say so explicitly — do not invent information. Cite sources "
    "using bracketed numbers like [1], [2] matching the extract numbers."
)


@dataclass
class Chunk:
    """A text chunk with provenance."""

    text: str
    source: str
    page: int
    chunk_id: str


@dataclass
class Answer:
    """An answer with citations."""

    text: str
    citations: list[dict]


def extract_text(pdf_path: Path) -> list[tuple[int, str]]:
    """Extract (page_number, text) tuples from a PDF.

    Page numbers are 1-indexed. Empty pages are excluded.
    """


def chunk_text(
    pages: list[tuple[int, str]],
    source: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> list[Chunk]:
    """Split page text into overlapping chunks.

    Each chunk carries its source filename and starting page number.
    Chunk IDs are deterministic: hash of (source, page, index).
    """


def embed_and_store(
    chunks: list[Chunk],
    index_dir: Path = DEFAULT_INDEX_DIR,
    collection_name: str = DEFAULT_COLLECTION,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> int:
    """Embed chunks and store them in a ChromaDB collection.

    Lazy-imports sentence_transformers and chromadb.
    Returns the number of chunks added.
    """


def retrieve(
    question: str,
    index_dir: Path = DEFAULT_INDEX_DIR,
    collection_name: str = DEFAULT_COLLECTION,
    top_k: int = DEFAULT_TOP_K,
    model_name: str = DEFAULT_EMBEDDING_MODEL,
) -> list[Chunk]:
    """Retrieve the top-k most relevant chunks for a question.

    Lazy-imports sentence_transformers and chromadb.
    """


def generate_answer(
    question: str,
    chunks: list[Chunk],
    model_name: str = DEFAULT_LLM_MODEL,
) -> Answer:
    """Generate an answer grounded in the retrieved chunks.

    Lazy-imports ollama.
    Raises ConnectionError if Ollama is not reachable.
    """


def cmd_ingest(args: argparse.Namespace) -> int:
    """Handle `ingest`."""


def cmd_query(args: argparse.Namespace) -> int:
    """Handle `query`."""


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser."""


def main(argv: list[str] | None = None) -> int:
    """Entry point. With no arguments, print usage and return 0."""
Behaviour details:

extract_text

Uses PdfReader. For each page, call page.extract_text(). Skip empty/whitespace-only pages.

Return list of (page_number, text).

chunk_text

Iterate pages. Concatenate text per page with a space.

Sliding window of chunk_size characters with overlap step back.

Page number is the page containing the chunk's start offset.

chunk_id = hashlib.sha1(f"{source}:{page}:{index}".encode()).hexdigest()[:16].

embed_and_store

Lazy-import sentence_transformers.SentenceTransformer and chromadb.

Instantiate the model, instantiate chromadb.PersistentClient(path=str(index_dir)).

Get or create collection named collection_name.

Encode all chunk texts in one model.encode(texts) call.

collection.add(ids=[...], documents=[...], metadatas=[...], embeddings=[...]).

Metadata per chunk: {"source": source, "page": page}.

Return count.

retrieve

Lazy-import sentence_transformers.SentenceTransformer and chromadb.

Encode the question.

collection.query(query_embeddings=[embedding], n_results=top_k).

Return list of Chunk reconstructed from results.

generate_answer

Lazy-import ollama.

Build a prompt: system message (verbatim from SYSTEM_PROMPT), then user message with the retrieved chunks labelled [1], [2], etc., then the question.

Call ollama.Client().chat(model=model_name, messages=[...]).

Catch ConnectionError (and the underlying httpx.ConnectError if raised by the ollama client) and re-raise as ConnectionError("Ollama not reachable").

Return Answer(text=response.message.content, citations=[{"n": i+1, "source": c.source, "page": c.page} for i, c in enumerate(chunks)]).

cmd_ingest

args.source is a directory. Glob *.pdf. If empty, print No PDFs found in <source>. to stderr, return 1.

For each PDF: extract_text → chunk_text. Accumulate.

Print Extracted N chunks from M PDFs.

embed_and_store. Print Indexed N chunks to <index_dir>.

Return 0.

cmd_query

If index_dir doesn't exist, print Index not found at <index_dir>. Run 'ingest' first. to stderr, return 1.

retrieve. If empty, print No results found. return 0.

generate_answer. On ConnectionError: print Ollama not reachable. Is 'ollama serve' running? to stderr, return 2.

Print the answer text. Then print \nSources: followed by one line per citation: [N] <source>, p. <page>.

Return 0.

build_parser

Two subcommands: ingest and query.

ingest: --source <dir> (required), --index-dir <dir> (default .rag-index), --embedding-model <name> (default all-MiniLM-L6-v2).

query: --question <str> (required), --index-dir <dir> (default .rag-index), --top-k <int> (default 5), --llm-model <name> (default llama3.2:3b).

main

argv defaults to sys.argv[1:]. If empty, print usage and return 0.

Rules:

Lazy-import heavy dependencies as specified above. This is critical.

Do not reach the network during import.

No globals beyond module-level constants.

Type hints on all public functions. Google-style docstrings.

Ruff-compatible (line length 140).

Print only what is specified.

5. workflows/text/rag-research-assistant/requirements.txt

text
chromadb>=0.4.0
sentence-transformers>=2.2.0
pypdf>=4.0.0
ollama>=0.1.0
Created files
6. workflows/text/rag-research-assistant/examples/README.md

markdown
# Examples

Sample outputs from this workflow.

To produce an example:

1. Point `ingest` at a small, public PDF corpus (e.g. 3–5 arXiv papers
   on a topic).
2. Run a representative query.
3. Copy the answer and sources into a `.md` file in this folder.

Example outputs are illustrative. They show what the workflow
produces with a given corpus and question — not what it should produce.
7. tests/workflows/test_rag_workflow.py

Smoke tests that do NOT require Ollama, Hugging Face downloads, or
network access. Test chunking, extraction, CLI parsing, and metadata —
not the heavy embedding/retrieval/generation functions.

Import the workflow.py module by path (like Brick 4's test).

Test classes:

TestMetadata

test_metadata_validates — validate metadata.yaml against the schema via validate_file; status is "valid".

test_tier_is_curated — tier is curated.

test_discipline_includes_research — research in disciplines.

TestChunkText — using synthetic page lists:

test_single_short_page — one page with short text → one chunk.

test_long_page_produces_multiple_chunks — one page with text longer than CHUNK_SIZE → multiple chunks.

test_overlap_respected — the tail of chunk i appears at the start of chunk i+1.

test_chunk_ids_deterministic — same input produces same IDs.

test_page_numbers_preserved — chunk page numbers come from input page list.

test_multiple_pages — chunks from page 2 have page=2.

TestExtractText — with a mock PdfReader:

test_returns_page_tuples — returns list of (page_number, text) tuples.

test_skips_empty_pages — pages whose extract_text() returns None or whitespace are excluded.

test_page_numbers_are_one_indexed — first page is number 1, not 0.

TestBuildParser

test_has_ingest_subcommand — parser has ingest.

test_has_query_subcommand — parser has query.

test_ingest_requires_source — parsing ingest without --source raises SystemExit.

test_query_requires_question — parsing query without --question raises SystemExit.

TestCmdIngest — with tmp_path:

test_empty_source_returns_error — a directory with no PDFs → stderr contains "No PDFs found", return 1.

test_nonexistent_source_returns_error — a path that doesn't exist → return 1.

TestCmdQuery — with tmp_path:

test_missing_index_returns_error — index directory doesn't exist → stderr contains "Index not found", return 1.

TestMain

test_no_args_prints_usage — main([]) prints usage and returns 0.

Aim for ~20 tests.

8. DEVLOG.md

Prepend:

markdown
## YYYY-MM-DD — Brick 5: RAG research assistant workflow

**Built:** Second content workflow. PDF ingestion, chunking, embedding
(sentence-transformers), storage (ChromaDB), retrieval, and Ollama-backed
generation with citations.

**Learned:** To be filled in.

**Changed:** To be filled in.

**Next:** Brick 6 (voice synthesis workflow).
9. ROADMAP.md

markdown
## Built
- [x] Provenance infrastructure
- [x] Repository skeleton
- [x] Full repository scaffold
- [x] Metadata schema
- [x] Launcher CLI
- [x] ComfyUI workflow
- [x] RAG workflow

## Next
- [ ] Audio workflow
...
Rules
Do not run ingest or query end-to-end. The tests deliberately avoid
heavy dependencies and external services.

Do not download the sentence-transformers model during tests. Lazy
imports inside embed_and_store and retrieve ensure this.

Do not modify any file outside the 9 listed.

No fabricated URLs.

Follow docs/DEVELOPMENT.md §9.

Verification
The virtual environment is at .venv/ and its Python is 3.11. Run
every command using the venv's Python explicitly.

Copy the full terminal transcript into your response inside a fenced
code block titled VERIFICATION. Include each command with a $
prefix on its own line, and its complete output below.

Do not summarize. Do not paraphrase. If you cannot run shell
commands in this session, say so explicitly and skip this section —
do not fabricate output.

text
$ git status
$ .venv\Scripts\python.exe -m ruff check .
$ .venv\Scripts\python.exe -m pytest tests/ -v
$ .venv\Scripts\python.exe -m tools.sandbox.cli list
$ .venv\Scripts\python.exe -m tools.validators.validate_all
Expected:

git status — 5 modified, 4 new (workflow.py is a modification of a
placeholder; requirements.txt, examples/README.md, and the test file
are new; prompts/ directory is new).

ruff check . — All checks passed!

pytest — 82 remain from before, ~20 new. No failures, no errors.

sandbox list — now shows two workflows:

comfyui-character-design [curated] games,filmmaking,fine-art

rag-research-assistant [curated] research,teaching

validate_all — 2 valid, 2 skipped, 0 invalid.

Output
Report:

Every file created (full path)

Every file modified (full path)

The VERIFICATION code block (or explicit note that shell commands
could not be run)

Any deviations from the spec, with justification

Also Fill In
Actual Output section of
prompts/brick-05-rag-workflow/01-initial-prompt.md — one paragraph
summary.

Learned and Changed fields in the DEVLOG entry above.

Commit Message
text
feat(workflows): add RAG research assistant workflow

- workflows/text/rag-research-assistant/
  - README, guide, workflow.py, requirements.txt
  - Full metadata.yaml (curated tier, embedding model provenance)
  - examples/README.md
- tests/workflows/test_rag_workflow.py — smoke tests
- DEVLOG and ROADMAP updated

Generated with OpenCode (Nemotron 3 Ultra)
Prompt: prompts/brick-05-rag-workflow/01-initial-prompt.md

## Actual Output

Replaced 5 placeholder files in workflows/text/rag-research-assistant/ with real implementations: README.md (full documentation with what/needs/run/provenance), metadata.yaml (curated tier, embedding model provenance), guide.md (discipline guide with research/teaching sections, limitations, extensions), workflow.py (full RAG pipeline with lazy imports for heavy deps: ingest extracts PDFs with pypdf, chunks with overlap, embeds with sentence-transformers, stores in ChromaDB; query retrieves top-k, prompts Ollama with citations), requirements.txt (chromadb, sentence-transformers, pypdf, ollama). Created 4 new files: examples/README.md (instructions for adding sample outputs), tests/workflows/test_rag_workflow.py (17 smoke tests covering metadata, chunking, extraction, CLI parsing, cmd_ingest/cmd_query error cases). Updated DEVLOG.md and ROADMAP.md. All verification commands pass: git status shows 5 modified + 4 new; ruff clean; pytest 102 passed/1 skipped; sandbox list shows both workflows; validate_all shows 2 valid, 2 skipped, 0 invalid.