# RAG Research Assistant

> Ingest a folder of PDFs into a local vector index. Query it with
> grounded answers that cite their sources. Runs offline — no data
> leaves the machine.

## What it does

This workflow implements a Retrieval-Augmented Generation (RAG) pipeline
for research assistance. The `ingest` subcommand extracts text from PDFs,
splits it into overlapping chunks, embeds the chunks using
sentence-transformers (all-MiniLM-L6-v2), and stores them in a local
ChromaDB vector index. The `query` subcommand retrieves the most relevant
chunks for a question, prompts a local LLM via Ollama with those chunks as
context, and returns a cited answer. All processing happens locally — no
data leaves the machine.

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
```text
ollama serve
```

2. Ingest a corpus:
```text
python workflows/text/rag-research-assistant/workflow.py ingest \
  --source path/to/pdfs
```

3. Query:
```text
python workflows/text/rag-research-assistant/workflow.py query \
  --question "What are the main critiques of RAG systems?"
```

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