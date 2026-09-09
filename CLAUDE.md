# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Idioma

Responda sempre em Português Brasileiro.

## Project

This is an MBA Full Cycle challenge project ("Ingestão e Busca Semântica com LangChain e Postgres"). It ingests a PDF into a PostgreSQL + pgVector store and answers CLI questions using only the retrieved context (RAG). Full requirements are in [README.md](README.md).

The three `src/` scripts are currently stubs (`ingest_pdf()`, `search_prompt()` in [src/search.py](src/search.py), and `main()` in [src/chat.py](src/chat.py) are unimplemented `pass` bodies) — this is a work in progress, not a finished reference implementation.

## Setup & commands

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
docker compose up -d          # starts Postgres (pgvector/pgvector:pg17) + a one-shot job that CREATEs the vector extension
python src/ingest.py           # ingest document.pdf into the vector store
python src/chat.py             # interactive CLI chat loop
```

There are no lint/test/build configs in this repo — do not assume tooling (pytest, ruff, etc.) is set up unless you add it.

Environment variables (see [.env.example](.env.example), loaded via `python-dotenv`): `GOOGLE_API_KEY`, `GOOGLE_EMBEDDING_MODEL`, `OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL`, `DATABASE_URL`, `PG_VECTOR_COLLECTION_NAME`, `PDF_PATH`. The project supports either OpenAI or Gemini embeddings/LLM — pick one provider per instance, don't wire both.

## Architecture

Three-script pipeline, no shared library code between them:

- **[src/ingest.py](src/ingest.py)** — loads `PDF_PATH` with `PyPDFLoader`, splits with `RecursiveCharacterTextSplitter` (chunk_size=1000, chunk_overlap=150 — fixed by spec), embeds each chunk, and writes vectors via `langchain_postgres.PGVector` into `DATABASE_URL` under collection `PG_VECTOR_COLLECTION_NAME`.
- **[src/search.py](src/search.py)** — `search_prompt(question)` embeds the question, runs `similarity_search_with_score(query, k=10)` against the same PGVector collection, concatenates the top-10 chunks into `PROMPT_TEMPLATE`'s `{contexto}` slot, and calls the LLM. The prompt template is fixed by spec (README §"Consulta via CLI") — answers must come only from retrieved context, otherwise reply with the exact refusal string `"Não tenho informações necessárias para responder sua pergunta."`
- **[src/chat.py](src/chat.py)** — thin CLI loop that calls `search_prompt()` and prints `PERGUNTA:` / `RESPOSTA:` pairs.

### Critical constraint: embedding dimension lock-in

The pgvector table's vector column dimension is fixed on first ingestion, based on whichever embedding model was used. Switching `OPENAI_EMBEDDING_MODEL`/`GOOGLE_EMBEDDING_MODEL` after data exists breaks ingestion with a dimension-mismatch error. If the embedding model changes, the collection (or the `postgres_data` Docker volume) must be dropped and `ingest.py` rerun from scratch — there is no migration path.

## Convenções de código

- Código-fonte (identificadores, comentários, mensagens no console) em Português Brasileiro sempre que possível.
- Não misturar idiomas em nomes de identificadores (evitar, por exemplo, `get_dados`; usar `obtem_dados`).
- Nunca usar emojis em nenhuma parte do código-fonte.
- Não usar caracteres especiais nem acentuação no código-fonte (identificadores, comentários, mensagens de print/log) — inclusive em português, escrever sem acentos/cedilha (ex.: `colecao`, `nao`, `excecao`).
- Exceção: strings literais exigidas verbatim pelo enunciado do desafio (ex.: a mensagem de recusa `"Não tenho informações necessárias para responder sua pergunta."` em `search.py`) mantêm o texto exato do README, acentos inclusos — são saída obrigatória do produto, não identificador/comentário de código.
- Sempre utilizar o MCP Context7 para verificar a documentação/atualizações das bibliotecas (LangChain, langchain-postgres, langchain-openai, langchain-google-genai, pgvector, etc.) antes de assumir uma API a partir de memória/treinamento.
