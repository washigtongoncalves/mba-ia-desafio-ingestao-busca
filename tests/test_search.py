import pytest
from langchain_core.documents import Document

import provedores
import search


def test_search_prompt_sem_pergunta_levanta_erro():
    with pytest.raises(RuntimeError, match="pergunta"):
        search.search_prompt(None)


def test_search_prompt_variaveis_ausentes_levanta_erro(monkeypatch):
    monkeypatch.setattr(provedores, "url_banco_dados", None)
    monkeypatch.setattr(provedores, "nome_colecao", "colecao-teste")

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        search.search_prompt("Qual o faturamento?")


def test_search_prompt_monta_contexto_e_chama_llm(monkeypatch):
    monkeypatch.setattr(provedores, "url_banco_dados", "postgresql://usuario:senha@localhost:5432/rag")
    monkeypatch.setattr(provedores, "nome_colecao", "colecao-teste")

    embeddings_falso = object()
    monkeypatch.setattr(provedores, "obter_embeddings", lambda: embeddings_falso)

    documentos_falsos = [
        (Document(page_content="Faturamento de 10 milhoes de reais."), 0.1),
        (Document(page_content="Empresa fundada em 2020."), 0.2),
    ]

    chamada_pgvector = {}

    class PGVectorFalso:
        def __init__(self, **kwargs):
            chamada_pgvector.update(kwargs)

        def similarity_search_with_score(self, query, k):
            chamada_pgvector["query"] = query
            chamada_pgvector["k"] = k
            return documentos_falsos

    monkeypatch.setattr(search, "PGVector", PGVectorFalso)

    chamada_llm = {}

    class LlmFalso:
        def invoke(self, prompt):
            chamada_llm["prompt"] = prompt

            class RespostaFalsa:
                content = "O faturamento foi de 10 milhoes de reais."

            return RespostaFalsa()

    monkeypatch.setattr(provedores, "obter_llm", lambda: LlmFalso())

    resultado = search.search_prompt("Qual o faturamento da empresa?")

    assert resultado == "O faturamento foi de 10 milhoes de reais."
    assert chamada_pgvector["embeddings"] is embeddings_falso
    assert chamada_pgvector["collection_name"] == "colecao-teste"
    assert chamada_pgvector["connection"] == "postgresql+psycopg://usuario:senha@localhost:5432/rag"
    assert chamada_pgvector["use_jsonb"] is True
    assert chamada_pgvector["query"] == "Qual o faturamento da empresa?"
    assert chamada_pgvector["k"] == 10
    assert "Faturamento de 10 milhoes de reais." in chamada_llm["prompt"]
    assert "Empresa fundada em 2020." in chamada_llm["prompt"]
    assert "Qual o faturamento da empresa?" in chamada_llm["prompt"]
