# Configuração da OpenAI

Este guia mostra como obter as credenciais da OpenAI e preencher as variáveis de ambiente usadas por este projeto (`OPENAI_API_KEY`, `OPENAI_EMBEDDING_MODEL` e `OPENAI_CHAT_MODEL`, no arquivo `.env`).

## 1. Criar uma API Key

1. Crie (ou acesse) uma conta na [OpenAI Platform](https://platform.openai.com/).
2. Siga o [quickstart da API OpenAI](https://developers.openai.com/api/docs/quickstart) para gerar uma API Key no painel — ela só é exibida uma vez, guarde-a em local seguro.
3. Copie o valor gerado (começa com `sk-...`).

## 2. Preencher o `.env`

```
OPENAI_API_KEY=sk-sua-chave-aqui
OPENAI_EMBEDDING_MODEL='text-embedding-3-small'
OPENAI_CHAT_MODEL='gpt-5.6-luna'
```

- `OPENAI_API_KEY`: a chave criada no passo 1.
- `OPENAI_EMBEDDING_MODEL`: modelo usado para gerar os embeddings dos chunks do PDF. `text-embedding-3-small` é o modelo mais leve e barato da linha atual (veja o [guia de embeddings](https://developers.openai.com/api/docs/guides/embeddings) para outras opções, como `text-embedding-3-large`).
- `OPENAI_CHAT_MODEL`: modelo usado para gerar a resposta em `src/search.py`. `gpt-5.6-luna` é a variante mais leve e barata da familia GPT-5.6 atual (veja a [visao geral de modelos](https://developers.openai.com/api/docs/models) para outras opções).

## Atenção

- Deixe preenchida **apenas uma** das duas API Keys (`OPENAI_API_KEY` ou `GOOGLE_API_KEY`) — `src/ingest.py` escolhe o provedor automaticamente pela chave que estiver presente no `.env`.
- Trocar `OPENAI_EMBEDDING_MODEL` depois de já ter feito uma ingestão exige apagar a collection (ou o volume do Postgres) e reingerir do zero — a dimensão do vetor muda por modelo (veja o README, seção "Escolha dos modelos").

## Links úteis

- [Quickstart da API OpenAI](https://developers.openai.com/api/docs/quickstart)
- [Guia de Embeddings](https://developers.openai.com/api/docs/guides/embeddings)
- [Referência de modelos de Embeddings](https://developers.openai.com/api/reference/resources/embeddings)
