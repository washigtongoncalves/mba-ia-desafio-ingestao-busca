import pytest

import apagar_colecao
import provedores


def test_apagar_colecao_variaveis_ausentes_levanta_erro(monkeypatch):
    monkeypatch.setattr(provedores, "url_banco_dados", None)
    monkeypatch.setattr(provedores, "nome_colecao", "colecao-teste")

    with pytest.raises(RuntimeError, match="DATABASE_URL"):
        apagar_colecao.apagar_colecao()


def test_apagar_colecao_chama_delete_collection(monkeypatch):
    monkeypatch.setattr(provedores, "url_banco_dados", "postgresql://usuario:senha@localhost:5432/rag")
    monkeypatch.setattr(provedores, "nome_colecao", "colecao-teste")

    embeddings_falso = object()
    monkeypatch.setattr(provedores, "obter_embeddings", lambda: embeddings_falso)

    chamada_pgvector = {}
    chamada_delete = {"executada": False}

    class PGVectorFalso:
        def __init__(self, **kwargs):
            chamada_pgvector.update(kwargs)

        def delete_collection(self):
            chamada_delete["executada"] = True

    monkeypatch.setattr(apagar_colecao, "PGVector", PGVectorFalso)

    apagar_colecao.apagar_colecao()

    assert chamada_pgvector["embeddings"] is embeddings_falso
    assert chamada_pgvector["collection_name"] == "colecao-teste"
    assert chamada_pgvector["connection"] == "postgresql+psycopg://usuario:senha@localhost:5432/rag"
    assert chamada_pgvector["use_jsonb"] is True
    assert chamada_delete["executada"] is True
