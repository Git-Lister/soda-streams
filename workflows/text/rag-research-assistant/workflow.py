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
    reader = PdfReader(pdf_path)
    results = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            results.append((i + 1, text))
    return results


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
    chunks = []
    for page_num, text in pages:
        text = text.strip()
        if not text:
            continue
        start = 0
        index = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end]
            if chunk_text.strip():
                chunk_id = hashlib.sha1(
                    f"{source}:{page_num}:{index}".encode()
                ).hexdigest()[:16]
                chunks.append(
                    Chunk(
                        text=chunk_text,
                        source=source,
                        page=page_num,
                        chunk_id=chunk_id,
                    )
                )
                index += 1
            if end == len(text):
                break
            start = end - overlap
    return chunks


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
    import chromadb
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    client = chromadb.PersistentClient(path=str(index_dir))
    collection = client.get_or_create_collection(name=collection_name)

    texts = [chunk.text for chunk in chunks]
    embeddings = model.encode(texts).tolist()

    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=texts,
        metadatas=[
            {"source": chunk.source, "page": chunk.page} for chunk in chunks
        ],
        embeddings=embeddings,
    )
    return len(chunks)


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
    import chromadb
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    client = chromadb.PersistentClient(path=str(index_dir))

    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        return []

    embedding = model.encode([question])[0].tolist()
    results = collection.query(
        query_embeddings=[embedding], n_results=top_k
    )

    chunks = []
    if results["ids"] and results["ids"][0]:
        for i, chunk_id in enumerate(results["ids"][0]):
            metadata = results["metadatas"][0][i]
            text = results["documents"][0][i]
            chunks.append(
                Chunk(
                    text=text,
                    source=metadata["source"],
                    page=metadata["page"],
                    chunk_id=chunk_id,
                )
            )
    return chunks


def generate_answer(
    question: str,
    chunks: list[Chunk],
    model_name: str = DEFAULT_LLM_MODEL,
) -> Answer:
    """Generate an answer grounded in the retrieved chunks.

    Lazy-imports ollama.
    Raises ConnectionError if Ollama is not reachable.
    """
    import httpx
    import ollama

    client = ollama.Client()
    try:
        client.list()
    except (ConnectionError, httpx.ConnectError) as err:
        raise ConnectionError("Ollama not reachable") from err

    source_text = "\n\n".join(
        f"[{i + 1}] (Source: {c.source}, p. {c.page})\n{c.text}"
        for i, c in enumerate(chunks)
    )
    user_prompt = (
        f"Source extracts:\n{source_text}\n\n"
        f"Question: {question}\n\n"
        f"Answer with citations using [1], [2], etc.:"
    )

    response = client.chat(
        model=model_name,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    answer_text = response.message.content
    citations = [
        {"n": i + 1, "source": c.source, "page": c.page}
        for i, c in enumerate(chunks)
    ]
    return Answer(text=answer_text, citations=citations)


def cmd_ingest(args: argparse.Namespace) -> int:
    """Handle `ingest`."""
    source_dir = Path(args.source)
    if not source_dir.exists():
        print(f"Source directory does not exist: {source_dir}", file=sys.stderr)
        return 1

    pdf_files = list(source_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {source_dir}", file=sys.stderr)
        return 1

    all_chunks = []
    for pdf_file in pdf_files:
        pages = extract_text(pdf_file)
        chunks = chunk_text(pages, source=pdf_file.name)
        all_chunks.extend(chunks)

    print(f"Extracted {len(all_chunks)} chunks from {len(pdf_files)} PDFs.")

    count = embed_and_store(
        all_chunks,
        index_dir=Path(args.index_dir),
        collection_name=args.collection,
        model_name=args.embedding_model,
    )
    print(f"Indexed {count} chunks to {args.index_dir}.")
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    """Handle `query`."""
    index_dir = Path(args.index_dir)
    if not index_dir.exists():
        print(
            f"Index not found at {index_dir}. Run 'ingest' first.",
            file=sys.stderr,
        )
        return 1

    chunks = retrieve(
        args.question,
        index_dir=index_dir,
        collection_name=args.collection,
        top_k=args.top_k,
        model_name=args.embedding_model,
    )

    if not chunks:
        print("No results found.")
        return 0

    try:
        answer = generate_answer(
            args.question, chunks, model_name=args.llm_model
        )
    except ConnectionError:
        print(
            "Ollama not reachable. Is 'ollama serve' running?",
            file=sys.stderr,
        )
        return 2

    print(answer.text)
    print("\nSources:")
    for c in answer.citations:
        print(f"[{c['n']}] {c['source']}, p. {c['page']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser."""
    parser = argparse.ArgumentParser(prog="rag-research-assistant")
    subparsers = parser.add_subparsers(dest="command", required=False)

    # ingest subcommand
    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument(
        "--source", required=True, help="Directory containing PDFs"
    )
    ingest_parser.add_argument(
        "--index-dir",
        default=str(DEFAULT_INDEX_DIR),
        help="Directory for ChromaDB index",
    )
    ingest_parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION,
        help="ChromaDB collection name",
    )
    ingest_parser.add_argument(
        "--embedding-model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="sentence-transformers model name",
    )

    # query subcommand
    query_parser = subparsers.add_parser("query")
    query_parser.add_argument(
        "--question", required=True, help="Question to ask"
    )
    query_parser.add_argument(
        "--index-dir",
        default=str(DEFAULT_INDEX_DIR),
        help="Directory for ChromaDB index",
    )
    query_parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION,
        help="ChromaDB collection name",
    )
    query_parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Number of chunks to retrieve",
    )
    query_parser.add_argument(
        "--embedding-model",
        default=DEFAULT_EMBEDDING_MODEL,
        help="sentence-transformers model name",
    )
    query_parser.add_argument(
        "--llm-model",
        default=DEFAULT_LLM_MODEL,
        help="Ollama model name",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry point. With no arguments, print usage and return 0."""
    if argv is None:
        argv = sys.argv[1:]
    parser = build_parser()
    if not argv:
        parser.print_help()
        return 0
    args = parser.parse_args(argv)

    if args.command == "ingest":
        return cmd_ingest(args)
    if args.command == "query":
        return cmd_query(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())