import chat


def test_chat_faz_pergunta_e_imprime_resposta(monkeypatch, capsys):
    entradas = iter(["Qual o faturamento da empresa?", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(entradas))
    monkeypatch.setattr(chat, "search_prompt", lambda pergunta: "resposta falsa")

    chat.main()

    saida = capsys.readouterr().out
    assert "RESPOSTA: resposta falsa" in saida


def test_chat_encerra_com_linha_vazia_sem_chamar_busca(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda prompt="": "")

    chamadas = []
    monkeypatch.setattr(chat, "search_prompt", lambda pergunta: chamadas.append(pergunta))

    chat.main()

    assert chamadas == []


def test_chat_trata_erro_da_busca_e_continua(monkeypatch, capsys):
    entradas = iter(["pergunta invalida", ""])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(entradas))

    def search_prompt_falso(pergunta):
        raise RuntimeError("falha simulada")

    monkeypatch.setattr(chat, "search_prompt", search_prompt_falso)

    chat.main()

    saida_erro = capsys.readouterr().err
    assert "Erro na busca" in saida_erro
    assert "falha simulada" in saida_erro


def test_chat_encerra_ao_receber_eof(monkeypatch, capsys):
    def input_falso(prompt=""):
        raise EOFError

    monkeypatch.setattr("builtins.input", input_falso)

    chamadas = []
    monkeypatch.setattr(chat, "search_prompt", lambda pergunta: chamadas.append(pergunta))

    chat.main()

    assert chamadas == []
