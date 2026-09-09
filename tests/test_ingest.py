import pytest
from langchain_core.documents import Document

import ingest
import provedores


def test_ingerir_pdf_variaveis_ausentes_levanta_erro(monkeypatch):
    monkeypatch.setattr(ingest, "caminho_pdf", None)
    monkeypatch.setattr(provedores, "url_banco_dados", None)
    monkeypatch.setattr(provedores, "nome_colecao", "colecao-teste")

    with pytest.raises(RuntimeError, match="PDF_PATH"):
        ingest.ingerir_pdf()


def test_ingerir_pdf_grava_pedacos_com_ids_deterministicos(monkeypatch):
    monkeypatch.setattr(ingest, "caminho_pdf", "/tmp/documento-teste.pdf")
    monkeypatch.setattr(provedores, "url_banco_dados", "postgresql://usuario:senha@localhost:5432/rag")
    monkeypatch.setattr(provedores, "nome_colecao", "colecao-teste")

    embeddings_falso = object()
    monkeypatch.setattr(provedores, "obter_embeddings", lambda: embeddings_falso)

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
