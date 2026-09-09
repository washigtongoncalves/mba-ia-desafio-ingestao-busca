import pytest

import provedores


def test_montar_string_conexao_normaliza_prefixo_postgresql(monkeypatch):
    monkeypatch.setattr(provedores, "url_banco_dados", "postgresql://usuario:senha@localhost:5432/rag")

    resultado = provedores.montar_string_conexao()

    assert resultado == "postgresql+psycopg://usuario:senha@localhost:5432/rag"


def test_montar_string_conexao_mantem_prefixo_ja_normalizado(monkeypatch):
    url = "postgresql+psycopg://usuario:senha@localhost:5432/rag"
    monkeypatch.setattr(provedores, "url_banco_dados", url)

    resultado = provedores.montar_string_conexao()

    assert resultado == url


def test_obter_embeddings_com_chave_openai(monkeypatch):
    chamadas = {}

    class EmbeddingsFalso:
        def __init__(self, model):
            chamadas["model"] = model

    monkeypatch.setattr(provedores, "chave_openai", "chave-falsa")
    monkeypatch.setattr(provedores, "chave_google", None)
    monkeypatch.setattr(provedores, "modelo_embedding_openai", "text-embedding-3-small")
    monkeypatch.setattr(provedores, "OpenAIEmbeddings", EmbeddingsFalso)

    resultado = provedores.obter_embeddings()

    assert isinstance(resultado, EmbeddingsFalso)
    assert chamadas["model"] == "text-embedding-3-small"


def test_obter_embeddings_com_chave_google(monkeypatch):
    chamadas = {}

    class EmbeddingsFalso:
        def __init__(self, model):
            chamadas["model"] = model

    monkeypatch.setattr(provedores, "chave_openai", None)
    monkeypatch.setattr(provedores, "chave_google", "chave-falsa")
    monkeypatch.setattr(provedores, "modelo_embedding_google", "models/gemini-embedding-2-preview")
    monkeypatch.setattr(provedores, "GoogleGenerativeAIEmbeddings", EmbeddingsFalso)

    resultado = provedores.obter_embeddings()

    assert isinstance(resultado, EmbeddingsFalso)
    assert chamadas["model"] == "models/gemini-embedding-2-preview"


def test_obter_embeddings_sem_chaves_levanta_erro(monkeypatch):
    monkeypatch.setattr(provedores, "chave_openai", None)
    monkeypatch.setattr(provedores, "chave_google", None)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        provedores.obter_embeddings()


def test_obter_llm_com_chave_openai(monkeypatch):
    chamadas = {}

    class LlmFalso:
        def __init__(self, model):
            chamadas["model"] = model

    monkeypatch.setattr(provedores, "chave_openai", "chave-falsa")
    monkeypatch.setattr(provedores, "chave_google", None)
    monkeypatch.setattr(provedores, "modelo_chat_openai", "gpt-5.6-luna")
    monkeypatch.setattr(provedores, "ChatOpenAI", LlmFalso)

    resultado = provedores.obter_llm()

    assert isinstance(resultado, LlmFalso)
    assert chamadas["model"] == "gpt-5.6-luna"


def test_obter_llm_com_chave_google(monkeypatch):
    chamadas = {}

    class LlmFalso:
        def __init__(self, model):
            chamadas["model"] = model

    monkeypatch.setattr(provedores, "chave_openai", None)
    monkeypatch.setattr(provedores, "chave_google", "chave-falsa")
    monkeypatch.setattr(provedores, "modelo_chat_google", "gemini-3.5-flash")
    monkeypatch.setattr(provedores, "ChatGoogleGenerativeAI", LlmFalso)

    resultado = provedores.obter_llm()

    assert isinstance(resultado, LlmFalso)
    assert chamadas["model"] == "gemini-3.5-flash"


def test_obter_llm_sem_chaves_levanta_erro(monkeypatch):
    monkeypatch.setattr(provedores, "chave_openai", None)
    monkeypatch.setattr(provedores, "chave_google", None)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        provedores.obter_llm()
