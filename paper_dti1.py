"""
DTI/dMRI Preprocessing Pipeline Extractor
Fully local RAG pipeline — Ollama only, zero OpenAI calls.

HOW IT WORKS:
  1. Extract text from each PDF using pypdf
  2. Split into sentence-aware overlapping chunks
  3. Embed every chunk via Ollama (qwen3-embedding)
  4. For each paper, run MULTIPLE retrieval queries and union the results
     so we don't miss the preprocessing section if it uses different terminology
  5. Send retrieved chunks to qwen3:8b with an open-ended extraction prompt
  6. Save each paper's result immediately (checkpoint) — safe to re-run
  7. Run a batched cross-paper synthesis pass
  8. Save final Markdown + JSON

REQUIREMENTS:
  pip install pypdf ollama numpy

OLLAMA MODELS NEEDED:
  ollama pull qwen3:8b
  ollama pull qwen3-embedding:latest

RE-RUNNING:
  If interrupted, just re-run — already-processed papers are skipped.
  Delete the checkpoint file to reprocess everything from scratch.
"""

import json
import re
import time
import threading
from pathlib import Path
from datetime import datetime

import ollama
import numpy as np
from pypdf import PdfReader

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
PAPERS_DIR      = r"E:\adni-processing-pipeline\Week2\Papers1"
OUTPUT_MD       = r"E:\adni-processing-pipeline\Week2\dti_pipeline_results1.md"
OUTPUT_JSON     = r"E:\adni-processing-pipeline\Week2\dti_pipeline_results1.json"
CHECKPOINT_FILE = r"E:\adni-processing-pipeline\Week2\dti_checkpoint1.json"

GEN_MODEL   = "qwen3:8b"
EMBED_MODEL = "qwen3-embedding:latest"

CHUNK_SIZE    = 900
CHUNK_OVERLAP = 200

# Multi-query retrieval: each query retrieves TOP_K_PER_QUERY chunks.
# Results are unioned and deduplicated, so the model sees the best coverage
# of all the different ways a preprocessing section might be written.
TOP_K_PER_QUERY = 4

NUM_CTX        = 8192
NUM_PREDICT    = 2000
OLLAMA_TIMEOUT = 1800

SYNTHESIS_BATCH_SIZE = 8

# ─────────────────────────────────────────────────────────────────────────────
# RETRIEVAL QUERIES
#
# These cover the different ways preprocessing sections are described in papers.
# Using multiple queries dramatically reduces the chance of missing the section.
# ─────────────────────────────────────────────────────────────────────────────
RETRIEVAL_QUERIES = [
    # Direct DTI/dMRI terminology
    "diffusion tensor imaging preprocessing pipeline processing steps",
    # Methods section language
    "MRI data processing image processing pipeline methods",
    # Software-focused
    "FSL MRtrix ANTs FreeSurfer DiPy SPM diffusion",
    # Step-focused — these words appear in actual methods sections
    "eddy current correction motion correction brain extraction registration",
    # Acquisition + processing together (common in methods sections)
    "diffusion weighted images acquired processed voxel b-value gradient directions",
    # QC and fitting language
    "tensor fitting fractional anisotropy quality control tractography",
]

# ─────────────────────────────────────────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────────────────────────────────────────

DTI_PROMPT_TEMPLATE = """\
You are a systematic review assistant extracting diffusion MRI processing information \
from research paper excerpts.

Paper: "{title}"

RULES — follow these strictly:
- ONLY use information explicitly present in the EXCERPTS below.
- Do NOT infer, assume, or add steps that are not directly stated.
- Use the paper's own wording whenever possible.
- If the excerpts do not contain enough detail to answer a question, say exactly: \
"Not reported in available text."
- If the excerpts clearly contain no diffusion MRI content at all, say: \
"NO DIFFUSION MRI PROCESSING FOUND" and stop.

Answer these questions based strictly on the excerpts:

1. Was diffusion MRI (DTI, dMRI, DWI, or similar) used in this paper?

2. What processing steps were applied to the diffusion images? \
Describe only what is explicitly stated, in the order described.

3. What software or tools are explicitly named for processing?

4. What acquisition or processing parameters are explicitly reported? \
(b-values, number of directions, voxel size, thresholds, etc.)

5. Copy the exact sentences from the excerpts that describe the processing. \
Quote them precisely — do not paraphrase.

6. Is the processing description complete, or does it appear incomplete/missing?

--- EXCERPTS ---
{context}
--- END EXCERPTS ---
"""

SYNTHESIS_BATCH_PROMPT = """\
You are a systematic review assistant. Below are diffusion MRI preprocessing summaries \
extracted from {n} research papers (batch {batch_num} of {total_batches}).

Write a concise structured summary covering:
1. Which processing steps appear across these papers
2. Which software tools are used and how often
3. Notable parameter choices
4. Any papers with unusual or incomplete reporting

Name specific papers when making comparisons.

--- PAPER SUMMARIES ---
{summaries}
--- END ---
"""

SYNTHESIS_FINAL_PROMPT = """\
You are a systematic review assistant. Below are batch summaries covering diffusion MRI \
preprocessing from {n} total papers.

Write a final comparative synthesis covering:
1. The most commonly used preprocessing steps (ranked by frequency)
2. The most commonly used tools (ranked by frequency)
3. Parameter ranges and disagreements across papers
4. Papers with notably different, minimal, or incomplete pipeline reporting
5. Gaps in reporting (e.g. steps that are likely done but rarely described)

--- BATCH SUMMARIES ---
{summaries}
--- END ---
"""

# ─────────────────────────────────────────────────────────────────────────────
# DTI KEYWORDS — for quick pre-screening only
# ─────────────────────────────────────────────────────────────────────────────
DTI_KEYWORDS = [
    "diffusion", "DTI", "dMRI", "DWI", "diffusion tensor",
    "tractography", "white matter", "eddy", "topup", "MRtrix",
    "b-value", "b-shell", "gradient direction", "diffusion weighted",
    "fractional anisotropy", " FA ", " MD ", " RD ", " AD ",
]


# ─────────────────────────────────────────────────────────────────────────────
# CHECKPOINTING
# ─────────────────────────────────────────────────────────────────────────────

def load_checkpoint() -> dict:
    path = Path(CHECKPOINT_FILE)
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            print(f"  Checkpoint loaded: {len(data)} previously processed paper(s).")
            return data
        except Exception as e:
            print(f"  Could not read checkpoint: {e} — starting fresh.")
    return {}


def save_checkpoint(checkpoint: dict):
    Path(CHECKPOINT_FILE).write_text(
        json.dumps(checkpoint, indent=2, ensure_ascii=False), encoding="utf-8"
    )


# ─────────────────────────────────────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────────────────────────────────────

def check_ollama_models() -> bool:
    print("  Checking Ollama models...")
    try:
        available = [m.model for m in ollama.list().models]
    except Exception as e:
        print(f"  Cannot reach Ollama: {e}")
        print("  Make sure Ollama is running: ollama serve")
        return False
    missing = [m for m in [GEN_MODEL, EMBED_MODEL] if not any(m in a for a in available)]
    if missing:
        print(f"  Missing models: {missing}")
        for m in missing:
            print(f"    ollama pull {m}")
        return False
    print(f"    OK  {GEN_MODEL}")
    print(f"    OK  {EMBED_MODEL}")
    return True


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pass
    return "\n".join(pages)


def chunk_text(text: str) -> list[str]:
    """Sentence-aware chunking — avoids splitting mid-sentence."""
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z\d])', text)
    chunks: list[str] = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) > CHUNK_SIZE and current:
            chunks.append(current.strip())
            current = current[-CHUNK_OVERLAP:] + " " + sentence
        else:
            current += (" " if current else "") + sentence
    if current.strip():
        chunks.append(current.strip())
    return [c for c in chunks if len(c) > 80]


def embed(text: str) -> np.ndarray:
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return np.array(response["embedding"], dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom > 0 else 0.0


def multi_query_retrieve(
    chunks: list[str],
    chunk_vecs: list,
    queries: list[str],
    k_per_query: int,
) -> list[str]:
    """
    Run multiple embedding queries and return the union of top-k results.

    Why: A single query can miss the preprocessing section if it uses
    different terminology than the query. By running many queries covering
    different ways preprocessing might be described, we cast a much wider
    net while keeping the total chunk count reasonable.

    Deduplication preserves order by first appearance (highest-scoring query first).
    """
    seen_indices: set[int] = set()
    selected_chunks: list[str] = []

    valid_pairs = [
        (i, chunk, vec)
        for i, (chunk, vec) in enumerate(zip(chunks, chunk_vecs))
        if vec is not None
    ]

    for query in queries:
        try:
            query_vec = embed(query)
        except Exception:
            continue

        scored = sorted(
            [(cosine_similarity(query_vec, vec), i, chunk) for i, chunk, vec in valid_pairs],
            reverse=True,
        )

        added = 0
        for _, idx, chunk in scored:
            if idx not in seen_indices:
                seen_indices.add(idx)
                selected_chunks.append(chunk)
                added += 1
            if added >= k_per_query:
                break

    return selected_chunks


def generate_with_timeout(prompt: str) -> str:
    """Run ollama.generate() in a thread with a hard timeout."""
    result_container = [None]
    error_container  = [None]

    def _call():
        try:
            response = ollama.generate(
                model=GEN_MODEL,
                prompt=prompt,
                options={
                    "temperature": 0.1,
                    "num_ctx": NUM_CTX,
                    "num_predict": NUM_PREDICT,
                },
            )
            result_container[0] = response["response"].strip()
        except Exception as e:
            error_container[0] = e

    thread = threading.Thread(target=_call, daemon=True)
    thread.start()
    thread.join(timeout=OLLAMA_TIMEOUT)

    if thread.is_alive():
        raise TimeoutError(
            f"Ollama timed out after {OLLAMA_TIMEOUT}s. Try: ollama serve"
        )
    if error_container[0]:
        raise error_container[0]
    return result_container[0]


def filename_to_title(filename: str) -> str:
    stem = Path(filename).stem
    stem = re.sub(r"_\d{8,}$", "", stem)
    m = re.match(r"^(.+?)\s*-\s*(\d{4})\s*-\s*(.+)$", stem)
    if m:
        return f"{m.group(1).strip()} ({m.group(2)}) — {m.group(3).strip()}"
    return stem


def estimate_time(n: int) -> str:
    total = (80 * 0.3 + 30) * n  # qwen3:8b on GPU is fast
    return f"~{int(total // 60)} min for {n} paper(s)"


# ─────────────────────────────────────────────────────────────────────────────
# CORE PROCESSING
# ─────────────────────────────────────────────────────────────────────────────

def process_paper(pdf_path: Path) -> dict:
    title = filename_to_title(pdf_path.name)

    # 1. Extract
    print("  [1/4] Extracting text...")
    text = extract_pdf_text(pdf_path)
    if len(text) < 200:
        return {
            "title": title, "file": pdf_path.name,
            "error": "PDF text extraction failed or empty",
            "result": "", "top_passages": [],
        }

    has_dti = any(kw.lower() in text.lower() for kw in DTI_KEYWORDS)
    if not has_dti:
        print("  ⚠️   No diffusion MRI keywords found.")

    # 2. Chunk
    print(f"  [2/4] Chunking ({len(text):,} chars)...")
    chunks = chunk_text(text)
    print(f"        {len(chunks)} chunks.")

    # 3. Embed all chunks
    print(f"  [3/4] Embedding {len(chunks)} chunks...")
    t0 = time.time()
    chunk_vecs = []
    failed = 0
    for i, chunk in enumerate(chunks):
        if (i + 1) % 30 == 0:
            elapsed   = time.time() - t0
            remaining = (len(chunks) - i - 1) * (elapsed / (i + 1))
            print(f"        ... {i+1}/{len(chunks)}  ({remaining:.0f}s left)")
        try:
            chunk_vecs.append(embed(chunk))
        except Exception:
            chunk_vecs.append(None)
            failed += 1
    if failed:
        print(f"  ⚠️   {failed} chunks failed embedding.")

    # 4. Multi-query retrieval + generate
    print(f"  [4/4] Multi-query retrieval ({len(RETRIEVAL_QUERIES)} queries) & generating...")
    top_chunks = multi_query_retrieve(
        chunks, chunk_vecs, RETRIEVAL_QUERIES, k_per_query=TOP_K_PER_QUERY
    )
    print(f"        {len(top_chunks)} unique chunks retrieved across all queries.")

    # Warn if context is large
    approx_tokens = sum(len(c) for c in top_chunks) // 4
    if approx_tokens > NUM_CTX * 0.75:
        print(f"  ⚠️   Context ~{approx_tokens} tokens — approaching limit. "
              "Reduce TOP_K_PER_QUERY if output is truncated.")

    context = "\n\n---\n\n".join(top_chunks)
    prompt  = DTI_PROMPT_TEMPLATE.format(title=title, context=context)

    try:
        result = generate_with_timeout(prompt)
    except TimeoutError as e:
        print(f"  ⏱️   {e}")
        result = f"TIMEOUT: {e}"
    except Exception as e:
        result = f"Generation failed: {e}"

    return {
        "title": title,
        "file": pdf_path.name,
        "has_dti_keywords": has_dti,
        "chunks_total": len(chunks),
        "chunks_retrieved": len(top_chunks),
        "result": result,
        "top_passages": top_chunks,
    }


# ─────────────────────────────────────────────────────────────────────────────
# BATCHED SYNTHESIS
# ─────────────────────────────────────────────────────────────────────────────

def run_batched_synthesis(results: list[dict]) -> str:
    dti_results = [
        r for r in results
        if r.get("result")
        and "NO DIFFUSION MRI PROCESSING FOUND" not in r.get("result", "").upper()
        and not r.get("error")
        and "TIMEOUT" not in r.get("result", "")
    ]
    if len(dti_results) < 2:
        return ""

    batches       = [dti_results[i : i + SYNTHESIS_BATCH_SIZE]
                     for i in range(0, len(dti_results), SYNTHESIS_BATCH_SIZE)]
    total_batches = len(batches)
    print(f"\n  Synthesis: {len(dti_results)} papers in {total_batches} batch(es).")

    batch_summaries = []
    for batch_num, batch in enumerate(batches, 1):
        print(f"  Batch {batch_num}/{total_batches} ({len(batch)} papers)...")
        summaries = "\n\n===\n\n".join(
            f"Paper: {r['title']}\n\n{r['result']}" for r in batch
        )
        prompt = SYNTHESIS_BATCH_PROMPT.format(
            n=len(batch),
            batch_num=batch_num,
            total_batches=total_batches,
            summaries=summaries,
        )
        try:
            s = generate_with_timeout(prompt)
            batch_summaries.append(f"[Batch {batch_num} — {len(batch)} papers]\n\n{s}")
        except Exception as e:
            batch_summaries.append(f"[Batch {batch_num}] — failed: {e}")

    if len(batch_summaries) == 1:
        return batch_summaries[0]

    print("  Final synthesis across all batches...")
    try:
        return generate_with_timeout(SYNTHESIS_FINAL_PROMPT.format(
            n=len(dti_results),
            summaries="\n\n===\n\n".join(batch_summaries),
        ))
    except Exception:
        return "\n\n---\n\n".join(batch_summaries)


# ─────────────────────────────────────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────────────────────────────────────

def save_results(results: list[dict], synthesis: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    md = [
        "# DTI/dMRI Preprocessing Pipeline Extraction",
        f"_Generated: {ts}_",
        f"_Papers: {PAPERS_DIR}_",
        f"_Gen model: {GEN_MODEL}  |  Embed model: {EMBED_MODEL}_",
        f"_Retrieval: {len(RETRIEVAL_QUERIES)} queries × top-{TOP_K_PER_QUERY} chunks each_",
        "", "---", "",
    ]

    if synthesis:
        md += [
            "## Cross-Paper Synthesis",
            "", synthesis, "", "---", "",
        ]

    for r in results:
        md += [f"## {r['title']}", f"_File: `{r['file']}`_", ""]
        if r.get("error"):
            md += [f"> Error: {r['error']}", ""]
        else:
            md += [r.get("result", ""), ""]
            if r.get("top_passages"):
                md += [
                    "<details>",
                    f"<summary>Retrieved passages ({r.get('chunks_retrieved', '?')} chunks "
                    f"from {len(RETRIEVAL_QUERIES)} queries — click to expand)</summary>",
                    "",
                ]
                for i, passage in enumerate(r["top_passages"], 1):
                    md += [f"**Passage {i}:**", "", f"> {passage.strip()}", ""]
                md += ["</details>", ""]
        md += ["---", ""]

    Path(OUTPUT_MD).write_text("\n".join(md), encoding="utf-8")
    print(f"  Markdown  -> {OUTPUT_MD}")

    output = {
        "generated": datetime.now().isoformat(),
        "gen_model": GEN_MODEL,
        "embed_model": EMBED_MODEL,
        "retrieval_queries": RETRIEVAL_QUERIES,
        "papers_dir": PAPERS_DIR,
        "synthesis": synthesis,
        "papers": [{k: v for k, v in r.items() if k != "top_passages"} for r in results],
    }
    Path(OUTPUT_JSON).write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  JSON      -> {OUTPUT_JSON}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    print("=" * 64)
    print("  DTI/dMRI Pipeline Extractor  |  Fully Local Ollama RAG")
    print("=" * 64)
    print(f"  Papers dir  : {PAPERS_DIR}")
    print(f"  Gen model   : {GEN_MODEL}")
    print(f"  Embed model : {EMBED_MODEL}")
    print(f"  Retrieval   : {len(RETRIEVAL_QUERIES)} queries x top-{TOP_K_PER_QUERY} each")
    print(f"  Checkpoint  : {CHECKPOINT_FILE}")
    print("=" * 64)

    papers_path = Path(PAPERS_DIR)
    if not papers_path.is_dir():
        print(f"  Directory not found: {PAPERS_DIR}")
        return

    if not check_ollama_models():
        return

    # Find and deduplicate PDFs
    pdf_files = sorted(papers_path.glob("*.pdf"))
    seen_stems: dict[str, Path] = {}
    deduped: list[Path] = []
    for p in pdf_files:
        clean_stem = re.sub(r"_\d{8,}$", "", p.stem)
        if clean_stem not in seen_stems:
            seen_stems[clean_stem] = p
            deduped.append(p)
        else:
            print(f"  Skipping duplicate: {p.name}")
    pdf_files = deduped

    if not pdf_files:
        print(f"  No PDFs found in {PAPERS_DIR}")
        return

    checkpoint = load_checkpoint()
    remaining  = [p for p in pdf_files if p.name not in checkpoint]
    skipped    = len(pdf_files) - len(remaining)

    print(f"\n  Total PDFs   : {len(pdf_files)}")
    print(f"  Already done : {skipped}  (from checkpoint)")
    print(f"  To process   : {len(remaining)}")
    if remaining:
        print(f"  Time estimate: {estimate_time(len(remaining))}")
    print()

    results_dict = dict(checkpoint)

    for i, pdf in enumerate(remaining, 1):
        print(f"\n[{i}/{len(remaining)}]  {'─'*56}")
        print(f"  Paper: {filename_to_title(pdf.name)[:70]}")
        try:
            result = process_paper(pdf)
        except Exception as e:
            print(f"  Fatal error: {e}")
            result = {
                "title": filename_to_title(pdf.name),
                "file": pdf.name,
                "error": str(e),
                "result": "",
                "top_passages": [],
            }

        results_dict[pdf.name] = result
        checkpoint[pdf.name] = {k: v for k, v in result.items() if k != "top_passages"}
        save_checkpoint(checkpoint)
        print(f"  Checkpoint saved. ({i}/{len(remaining)} this session)")

    results = [results_dict[p.name] for p in pdf_files if p.name in results_dict]

    print("\n\n" + "=" * 64)
    print("  CROSS-PAPER SYNTHESIS")
    print("=" * 64)
    synthesis = run_batched_synthesis(results)
    if not synthesis:
        print("  Skipped — fewer than 2 papers with diffusion MRI content.")

    print("\n" + "=" * 64)
    print("  SAVING RESULTS")
    print("=" * 64)
    save_results(results, synthesis)

    print("\n" + "=" * 64)
    print("  SUMMARY")
    print("=" * 64)
    dti_count = 0
    for r in results:
        status = "OK " if r.get("result") and not r.get("error") else "ERR"
        dti    = "DTI" if r.get("has_dti_keywords") else "   "
        if r.get("has_dti_keywords"):
            dti_count += 1
        retrieved = r.get("chunks_retrieved", "?")
        print(f"  [{status}] [{dti}]  chunks={retrieved:<3}  {r['title'][:52]}")

    print(f"\n  {dti_count}/{len(results)} papers had diffusion MRI keywords.")
    print(f"\n  Done.")
    print(f"    Markdown  -> {OUTPUT_MD}")
    print(f"    JSON      -> {OUTPUT_JSON}")
    print(f"\n  To reprocess from scratch: delete {CHECKPOINT_FILE}")


if __name__ == "__main__":
    main()