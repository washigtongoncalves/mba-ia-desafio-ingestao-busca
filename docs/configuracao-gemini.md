# Configuração do Gemini (Google AI)

Este guia mostra como obter as credenciais do Gemini e preencher as variáveis de ambiente usadas por este projeto (`GOOGLE_API_KEY` e `GOOGLE_EMBEDDING_MODEL`, no arquivo `.env`).

## 1. Criar uma API Key

1. Acesse o [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key) e siga o passo a passo para gerar uma API Key gratuita.
2. Se for a primeira vez usando a API, veja também o [guia de início rápido do Gemini](https://ai.google.dev/gemini-api/docs/get-started).
3. Copie a chave gerada.

## 2. Preencher o `.env`

```
GOOGLE_API_KEY=sua-chave-aqui
GOOGLE_EMBEDDING_MODEL='models/gemini-embedding-001'
```

- `GOOGLE_API_KEY`: a chave criada no passo 1.
- `GOOGLE_EMBEDDING_MODEL`: modelo usado para gerar os embeddings dos chunks do PDF.

## Atenção: o modelo padrão do `.env.example` está desatualizado

O `.env.example` deste repositório traz `models/embedding-001` como valor padrão, mas esse modelo (e outros da geração anterior, como `text-embedding-004`) já foi descontinuado pelo Google — confira a [página de descontinuações](https://ai.google.dev/gemini-api/docs/deprecations) antes de rodar a ingestão. Use um modelo vigente, por exemplo `models/gemini-embedding-001` (veja o [guia de Embeddings do Gemini](https://ai.google.dev/gemini-api/docs/embeddings) para as opções atuais).

## Demais atenções

- Deixe preenchida **apenas uma** das duas API Keys (`OPENAI_API_KEY` ou `GOOGLE_API_KEY`) — `src/ingest.py` escolhe o provedor automaticamente pela chave que estiver presente no `.env`.
- Trocar `GOOGLE_EMBEDDING_MODEL` depois de já ter feito uma ingestão exige apagar a collection (ou o volume do Postgres) e reingerir do zero — a dimensão do vetor muda por modelo (veja o README, seção "Escolha dos modelos").
- Os limites de requisições gratuitas podem mudar com frequência — consulte sempre a documentação oficial para valores atualizados.

## Links úteis

- [Como obter uma API Key](https://ai.google.dev/gemini-api/docs/api-key)
- [Guia de início rápido](https://ai.google.dev/gemini-api/docs/get-started)
- [Guia de Embeddings do Gemini](https://ai.google.dev/gemini-api/docs/embeddings)
- [Lista de modelos disponíveis](https://ai.google.dev/gemini-api/docs/models)
- [Página de descontinuações de modelos](https://ai.google.dev/gemini-api/docs/deprecations)
