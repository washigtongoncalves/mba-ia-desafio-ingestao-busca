import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

caminho_pdf = os.getenv("PDF_PATH")
url_banco_dados = os.getenv("DATABASE_URL")
nome_colecao = os.getenv("PG_VECTOR_COLLECTION_NAME")
chave_openai = os.getenv("OPENAI_API_KEY")
modelo_embedding_openai = os.getenv("OPENAI_EMBEDDING_MODEL")
chave_google = os.getenv("GOOGLE_API_KEY")
modelo_embedding_google = os.getenv("GOOGLE_EMBEDDING_MODEL")


def obter_embeddings():
    if chave_openai:
        return OpenAIEmbeddings(model=modelo_embedding_openai)
    if chave_google:
        return GoogleGenerativeAIEmbeddings(model=modelo_embedding_google)
    raise RuntimeError(
        "Defina OPENAI_API_KEY ou GOOGLE_API_KEY no .env para escolher o provedor de embeddings."
    )


def montar_string_conexao():
    if url_banco_dados.startswith("postgresql://"):
        return url_banco_dados.replace("postgresql://", "postgresql+psycopg://", 1)
    return url_banco_dados


def ingerir_pdf():
    variaveis_obrigatorias = {
        "PDF_PATH": caminho_pdf,
        "DATABASE_URL": url_banco_dados,
        "PG_VECTOR_COLLECTION_NAME": nome_colecao,
    }
    ausentes = [nome for nome, valor in variaveis_obrigatorias.items() if not valor]
    if ausentes:
        raise RuntimeError(
            f"Variaveis de ambiente ausentes no .env: {', '.join(ausentes)}"
        )

    embeddings = obter_embeddings()

    loader = PyPDFLoader(caminho_pdf)
    documentos = loader.load()

    divisor = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    pedacos = divisor.split_documents(documentos)

    prefixo_id = Path(caminho_pdf).stem
    ids = [f"{prefixo_id}-{indice}" for indice in range(len(pedacos))]

    PGVector.from_documents(
        documents=pedacos,
        embedding=embeddings,
        connection=montar_string_conexao(),
        collection_name=nome_colecao,
        ids=ids,
        use_jsonb=True,
    )

    print(
        f"Ingestao concluida: {len(pedacos)} pedacos armazenados na colecao '{nome_colecao}'."
    )


if __name__ == "__main__":
    try:
        ingerir_pdf()
    except Exception as erro:
        print(f"Erro na ingestao: {erro}", file=sys.stderr)
        sys.exit(1)
