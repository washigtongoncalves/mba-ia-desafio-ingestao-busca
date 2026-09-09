import pytest
from langchain_core.documents import Document

import ingest


def test_montar_string_conexao_normaliza_prefixo_postgresql(monkeypatch):
    monkeypatch.setattr(ingest, "url_banco_dados", "postgresql://usuario:senha@localhost:5432/rag")

    resultado = ingest.montar_string_conexao()

    assert resultado == "postgresql+psycopg://usuario:senha@localhost:5432/rag"


def test_montar_string_conexao_mantem_prefixo_ja_normalizado(monkeypatch):
    url = "postgresql+psycopg://usuario:senha@localhost:5432/rag"
    monkeypatch.setattr(ingest, "url_banco_dados", url)

    resultado = ingest.montar_string_conexao()

    assert resultado == url


def test_obter_embeddings_com_chave_openai(monkeypatch):
    chamadas = {}

    class EmbeddingsFalso:
        def __init__(self, model):
            chamadas["model"] = model

    monkeypatch.setattr(ingest, "chave_openai", "chave-falsa")
    monkeypatch.setattr(ingest, "chave_google", None)
    monkeypatch.setattr(ingest, "modelo_embedding_openai", "text-embedding-3-small")
    monkeypatch.setattr(ingest, "OpenAIEmbeddings", EmbeddingsFalso)

    resultado = ingest.obter_embeddings()

    assert isinstance(resultado, EmbeddingsFalso)
    assert chamadas["model"] == "text-embedding-3-small"


def test_obter_embeddings_com_chave_google(monkeypatch):
    chamadas = {}

    class EmbeddingsFalso:
        def __init__(self, model):
            chamadas["model"] = model

    monkeypatch.setattr(ingest, "chave_openai", None)
    monkeypatch.setattr(ingest, "chave_google", "chave-falsa")
    monkeypatch.setattr(ingest, "modelo_embedding_google", "models/gemini-embedding-001")
    monkeypatch.setattr(ingest, "GoogleGenerativeAIEmbeddings", EmbeddingsFalso)

    resultado = ingest.obter_embeddings()

    assert isinstance(resultado, EmbeddingsFalso)
    assert chamadas["model"] == "models/gemini-embedding-001"


def test_obter_embeddings_sem_chaves_levanta_erro(monkeypatch):
    monkeypatch.setattr(ingest, "chave_openai", None)
    monkeypatch.setattr(ingest, "chave_google", None)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        ingest.obter_embeddings()


def test_ingerir_pdf_variaveis_ausentes_levanta_erro(monkeypatch):
    monkeypatch.setattr(ingest, "caminho_pdf", None)
    monkeypatch.setattr(ingest, "url_banco_dados", None)
    monkeypatch.setattr(ingest, "nome_colecao", "colecao-teste")

    with pytest.raises(RuntimeError, match="PDF_PATH"):
        ingest.ingerir_pdf()


def test_ingerir_pdf_grava_pedacos_com_ids_deterministicos(monkeypatch):
    monkeypatch.setattr(ingest, "caminho_pdf", "/tmp/documento-teste.pdf")
    monkeypatch.setattr(ingest, "url_banco_dados", "postgresql://usuario:senha@localhost:5432/rag")
    monkeypatch.setattr(ingest, "nome_colecao", "colecao-teste")

    embeddings_falso = object()
    monkeypatch.setattr(ingest, "obter_embeddings", lambda: embeddings_falso)

    documento_falso = Document(page_content="conteudo de teste " * 200, metadata={})

    class LoaderFalso:
        def __init__(self, caminho):
            self.caminho = caminho

        def load(self):
            return [documento_falso]

    monkeypatch.setattr(ingest, "PyPDFLoader", LoaderFalso)

    chamada = {}

    def from_documents_falso(**kwargs):
        chamada.update(kwargs)

    monkeypatch.setattr(ingest.PGVector, "from_documents", staticmethod(from_documents_falso))

    ingest.ingerir_pdf()

    quantidade_pedacos = len(chamada["documents"])
    assert quantidade_pedacos > 1
    assert chamada["embedding"] is embeddings_falso
    assert chamada["connection"] == "postgresql+psycopg://usuario:senha@localhost:5432/rag"
    assert chamada["collection_name"] == "colecao-teste"
    assert chamada["use_jsonb"] is True
    assert chamada["ids"] == [f"documento-teste-{indice}" for indice in range(quantidade_pedacos)]
