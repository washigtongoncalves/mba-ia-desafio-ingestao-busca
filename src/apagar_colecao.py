import sys

from langchain_postgres import PGVector

import provedores


def apagar_colecao():
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

    armazenamento_vetorial.delete_collection()

    print(f"Colecao '{provedores.nome_colecao}' apagada com sucesso.")


if __name__ == "__main__":
    try:
        apagar_colecao()
    except Exception as erro:
        print(f"Erro ao apagar colecao: {erro}", file=sys.stderr)
        sys.exit(1)
