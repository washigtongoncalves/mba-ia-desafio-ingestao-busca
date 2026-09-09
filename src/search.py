from langchain_postgres import PGVector

import provedores

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""


def search_prompt(question=None):
    if not question:
        raise RuntimeError("Informe uma pergunta para realizar a busca.")

    variaveis_obrigatorias = {
        "DATABASE_URL": provedores.url_banco_dados,
        "PG_VECTOR_COLLECTION_NAME": provedores.nome_colecao,
    }
    ausentes = [nome for nome, valor in variaveis_obrigatorias.items() if not valor]
    if ausentes:
        raise RuntimeError(
            f"Variaveis de ambiente ausentes no .env: {', '.join(ausentes)}"
        )

    armazenamento_vetorial = PGVector(
        embeddings=provedores.obter_embeddings(),
        collection_name=provedores.nome_colecao,
        connection=provedores.montar_string_conexao(),
        use_jsonb=True,
    )

    resultados = armazenamento_vetorial.similarity_search_with_score(question, k=10)
    contexto = "\n\n".join(documento.page_content for documento, _pontuacao in resultados)

    prompt = PROMPT_TEMPLATE.format(contexto=contexto, pergunta=question)

    resposta = provedores.obter_llm().invoke(prompt)

    return resposta.content
