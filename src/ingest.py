import os
import sys
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

import provedores

caminho_pdf = os.getenv("PDF_PATH")


def ingerir_pdf():
    variaveis_obrigatorias = {
        "PDF_PATH": caminho_pdf,
        "DATABASE_URL": provedores.url_banco_dados,
        "PG_VECTOR_COLLECTION_NAME": provedores.nome_colecao,
    }
    ausentes = [nome for nome, valor in variaveis_obrigatorias.items() if not valor]
    if ausentes:
        raise RuntimeError(
            f"Variaveis de ambiente ausentes no .env: {', '.join(ausentes)}"
        )

    embeddings = provedores.obter_embeddings()

    loader = PyPDFLoader(caminho_pdf)
    documentos = loader.load()

    divisor = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    pedacos = divisor.split_documents(documentos)

    prefixo_id = Path(caminho_pdf).stem
    ids = [f"{prefixo_id}-{indice}" for indice in range(len(pedacos))]

    PGVector.from_documents(
        documents=pedacos,
        embedding=embeddings,
        connection=provedores.montar_string_conexao(),
        collection_name=provedores.nome_colecao,
        ids=ids,
        use_jsonb=True,
    )

    print(
        f"Ingestao concluida: {len(pedacos)} pedacos armazenados na colecao '{provedores.nome_colecao}'."
    )


if __name__ == "__main__":
    try:
        ingerir_pdf()
    except Exception as erro:
        print(f"Erro na ingestao: {erro}", file=sys.stderr)
        sys.exit(1)
