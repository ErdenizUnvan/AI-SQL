# COLAB INSTALL
# !pip install -q --upgrade pip
# !pip install -q llama-cpp-python huggingface-hub
# !pip install -q llama-index llama-index-core llama-index-llms-llama-cpp
# !pip install -q llama-index-embeddings-huggingface
# !pip install -q --upgrade "llama-cpp-python>=0.3.15"
# !pip install -q faiss-cpu numpy autogen-core autogen-ext
#
# NOTE: For CUDA GPU offload, llama-cpp-python itself must be CUDA-enabled.

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
from pathlib import Path
import faiss
import numpy as np
from autogen_core import CancellationToken
from llama_cpp import Llama
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from autogen_core.code_executor import CodeBlock
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from dotenv import load_dotenv
load_dotenv()
# ============================================================
# CONFIG
# ============================================================
BASE = Path("/content")
DB = BASE / "movies.db"
STORE = BASE / "faiss_store"
INDEX_FILE = STORE / "imdb.index"
CHUNKS_FILE = STORE / "chunks.json"
WORK_DIR = BASE / "autogen_work"

KNOWLEDGE = [
    BASE / "imdb_moviesdb_planner_knowledge.md",
    BASE / "imdb_moviesdb_intent_rules.md",
    BASE / "imdb_moviesdb_query_plan_schema.md",
    BASE / "imdb_moviesdb_examples.md",
]

REPO = os.getenv("GGUF_REPO")
GGUF_FILE = os.getenv("GGUF_FILE")
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME")
TOP_K = 6
MAX_ATTEMPTS = 3

print("[MODEL] loading GGUF model...")
llm_raw = Llama.from_pretrained(
    repo_id=REPO,
    filename=GGUF_FILE,
    n_gpu_layers=-1,
    n_ctx=8192,
    flash_attn=True,
    verbose=False,
)
print("[MODEL] GGUF loaded:", llm_raw.model_path)

print("[EMBED] loading embedding model...")
embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL_NAME)
Settings.embed_model = embed_model
print("[EMBED] loaded:", EMBED_MODEL_NAME)

# ============================================================
# LOCAL GPT-OSS CHAT + EMBEDDING
# ============================================================
def llm(prompt, json_mode=False, max_tokens=2048):
    kwargs = {
        "messages": [
            {"role": "system", "content": "You are a precise local assistant. Follow the requested output format exactly."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
        "top_p": 0.9,
        "top_k": 20,
        "stop": ["<|end|>", "<|start|>"],
        "max_tokens": max_tokens,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    out = llm_raw.create_chat_completion(**kwargs)
    return out["choices"][0]["message"]["content"].strip()


def embed(texts):
    # LlamaIndex HuggingFaceEmbedding -> list[list[float]]
    vectors = embed_model.get_text_embedding_batch(texts)
    x = np.asarray(vectors, dtype="float32")
    faiss.normalize_L2(x)
    return x

# ============================================================
# PERSISTENT LOCAL FAISS
# ============================================================
def source_hash():
    h = hashlib.sha256(EMBED_MODEL_NAME.encode())
    for p in KNOWLEDGE:
        if not p.exists():
            raise FileNotFoundError(p)
        h.update(p.read_bytes())
    return h.hexdigest()


def make_chunks():
    chunks = []
    for p in KNOWLEDGE:
        text = p.read_text(encoding="utf-8")
        sections = re.split(r"(?=^#{1,4}\s+)", text, flags=re.M)
        for section in sections:
            section = section.strip()
            if not section:
                continue
            # Long sections are split into ~1800-char blocks.
            for i in range(0, len(section), 1800):
                part = section[i:i + 1800].strip()
                if part:
                    chunks.append({"source": p.name, "text": part})
    return chunks


def load_faiss():
    STORE.mkdir(exist_ok=True)
    current_hash = source_hash()

    if INDEX_FILE.exists() and CHUNKS_FILE.exists():
        meta = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))
        if meta.get("hash") == current_hash:
            print("[FAISS] local index loaded")
            return faiss.read_index(str(INDEX_FILE)), meta["chunks"]

    print("[FAISS] building local index")
    chunks = make_chunks()
    vectors = embed([c["text"] for c in chunks])
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, str(INDEX_FILE))
    CHUNKS_FILE.write_text(
        json.dumps({"hash": current_hash, "chunks": chunks}, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[FAISS] saved: {len(chunks)} chunks")
    return index, chunks


def rag(question, index, chunks):
    scores, ids = index.search(embed([question]), min(TOP_K, len(chunks)))
    result = []
    for score, idx in zip(scores[0], ids[0]):
        if idx >= 0:
            c = chunks[int(idx)]
            result.append(
                f"SOURCE={c['source']} SCORE={score:.4f}\n{c['text']}"
            )
    return "\n\n---\n\n".join(result)

# ============================================================
# RAG -> IS_RELATED + JSON VARIABLE
# ============================================================
def parse_json(text):
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.I)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return json.loads(text[text.find("{"):text.rfind("}") + 1])


def make_plan(question, context):
    prompt = f"""
You are a planner for Harvard CS50 IMDb movies.db.
Use ONLY the retrieved RAG knowledge.
First decide whether the question is related to movies.db.
If related, return the JSON variable needed to generate Python code containing SQLite SQL.
DO NOT write SQL or Python here.

QUESTION:
{question}

RAG:
{context}

Return JSON only:
{{
  "is_related": true,
  "reason": "...",
  "intent": "...",
  "tables": [],
  "select": [],
  "joins": [],
  "filters": [{{"column":"", "operator":"", "value":null}}],
  "aggregation": null,
  "group_by": [],
  "order_by": [{{"column":"", "direction":"ASC"}}],
  "limit": null,
  "distinct": false,
  "self_join": false,
  "notes": []
}}

Allowed tables: movies, people, stars, directors, ratings.
Use documented joins only. Extract concrete names/titles/years/ratings/limits.
For two-actor/co-star questions, put alias/self-join requirements in notes.
If unrelated, is_related=false and leave plan arrays empty.
"""
    plan = parse_json(llm(prompt, json_mode=True, max_tokens=1024))
    allowed = {"movies", "people", "stars", "directors", "ratings"}
    if plan.get("is_related") and not set(plan.get("tables", [])).issubset(allowed):
        raise ValueError("Planner invented an unknown table")
    return plan

# ============================================================
# JSON VARIABLE -> PYTHON CODE (SQL IS INSIDE PYTHON)
# ============================================================
def clean_code(text):
    return re.sub(r"^```(?:python)?\s*|\s*```$", "", text.strip(), flags=re.I).strip()


def generate_code(plan):
    return clean_code(llm(f"""
Generate ONE complete Python program from this JSON plan:

{json.dumps(plan, ensure_ascii=False, indent=2)}

Rules:
- Python code only.
- import only os and sqlite3.
- db_path = os.environ["IMDB_DB_PATH"]
- connect READ ONLY with: sqlite3.connect(f"file:{{db_path}}?mode=ro", uri=True)
- SQL must be inside the Python program.
- SELECT / WITH...SELECT only.
- use ? parameters for user values.
- obey tables, joins, filters, distinct, aggregation, ordering, limit and self-join notes.
- print the final result.
- close the connection.
""", max_tokens=2048))

# ============================================================
# SMALL SAFETY CHECK
# ============================================================
FORBIDDEN = [
    "subprocess", "socket", "requests", "urllib", "open(", "os.system", "os.popen",
    " insert ", " update ", " delete ", " drop ", " alter ", " create ",
    " attach ", " detach ", " pragma ", " vacuum ",
]


def check_code(code):
    x = " " + code.lower().replace("\n", " ") + " "
    if "mode=ro" not in x:
        raise ValueError("database connection is not read-only")
    for bad in FORBIDDEN:
        if bad in x:
            raise ValueError(f"forbidden generated code: {bad.strip()}")

# ============================================================
# REPAIR
# ============================================================
def repair(question, context, plan, failed_code, error):
    return clean_code(llm(f"""
Fix the failed Python program below.
The task and JSON plan are unchanged.
SQL must remain INSIDE the Python code.

QUESTION:
{question}

RAG KNOWLEDGE:
{context}

JSON PLAN:
{json.dumps(plan, ensure_ascii=False, indent=2)}

FAILED CODE:
{failed_code}

AUTOGEN ERROR/OUTPUT:
{error}

Return corrected complete Python code only.
Only import os, sqlite3.
Use IMDB_DB_PATH and SQLite mode=ro.
Only SELECT / WITH...SELECT.
Use only documented tables/columns/joins.
""", max_tokens=2048))

# ============================================================
# AUTOGEN EXECUTE / REPAIR LOOP
# ============================================================
async def execute_with_autogen(question, context, plan, code):
    WORK_DIR.mkdir(exist_ok=True)
    os.environ["IMDB_DB_PATH"] = str(DB.resolve())

    executor = LocalCommandLineCodeExecutor(
        work_dir=WORK_DIR, timeout=60, cleanup_temp_files=True
    )
    attempts = []

    try:
        await executor.start()
        for n in range(1, MAX_ATTEMPTS + 1):
            try:
                check_code(code)
            except Exception as e:
                error = f"LOCAL VALIDATION ERROR: {e}"
                attempts.append({"attempt": n, "error": error})
                if n == MAX_ATTEMPTS:
                    raise RuntimeError(error)
                code = repair(question, context, plan, code, error)
                continue

            result = await executor.execute_code_blocks(
                [CodeBlock(language="python", code=code)],
                cancellation_token=CancellationToken(),
            )
            attempts.append({
                "attempt": n,
                "exit_code": result.exit_code,
                "output": result.output,
            })

            if result.exit_code == 0:
                return code, result.output.strip(), attempts

            if n < MAX_ATTEMPTS:
                code = repair(question, context, plan, code, result.output)

        raise RuntimeError(attempts[-1]["output"])
    finally:
        await executor.stop()

# ============================================================
# FULL FLOW
# ============================================================
async def ask(question):
    # 1) RAG first
    index, chunks = load_faiss()
    context = rag(question, index, chunks)

    # 2) RAG decides relevance + creates JSON variable
    plan = make_plan(question, context)
    print("\n=== JSON PLAN ===")
    print(json.dumps(plan, ensure_ascii=False, indent=2))

    if not plan.get("is_related"):
        print("\nNot related to movies.db:", plan.get("reason"))
        return

    # 3) JSON variable -> Python code containing SQL
    code = generate_code(plan)

    # 4) AutoGen executes Python; error -> LLM repair -> AutoGen executes again
    final_code, output, attempts = await execute_with_autogen(
        question, context, plan, code
    )

    print("\n=== FINAL PYTHON CODE ===")
    print(final_code)
    print("\n=== RESULT ===")
    print(output)
    print("\n=== EXECUTION ATTEMPTS ===")
    print(json.dumps(attempts, ensure_ascii=False, indent=2))



# ============================================================
# COLAB NOTEBOOK HELPER
# ============================================================
async def run_question(question):
    """Colab/Jupyter: await run_question("your question")"""
    return await ask(question)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("question", nargs="?")
    p.add_argument("--rebuild", action="store_true")
    args, _ = p.parse_known_args()

    if args.rebuild:
        INDEX_FILE.unlink(missing_ok=True)
        CHUNKS_FILE.unlink(missing_ok=True)

    if args.question:
        asyncio.run(ask(args.question))
        return

    while True:
        q = input("\nQuestion> ").strip()
        if q.lower() in {"exit", "quit", "q"}:
            break
        if q:
            try:
                asyncio.run(ask(q))
            except Exception as e:
                print("ERROR:", e)


# In Colab/Jupyter use:
#   await run_question("List the names of all people who starred in Toy Story")
#
# When executed as a normal .py script outside Colab, CLI mode is enabled.
if __name__ == "__main__" and "google.colab" not in sys.modules:
    main()
