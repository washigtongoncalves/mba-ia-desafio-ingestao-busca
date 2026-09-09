import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

url_banco_dados = os.getenv("DATABASE_URL")
nome_colecao = os.getenv("PG_VECTOR_COLLECTION_NAME")
chave_openai = os.getenv("OPENAI_API_KEY")
modelo_embedding_openai = os.getenv("OPENAI_EMBEDDING_MODEL")
modelo_chat_openai = os.getenv("OPENAI_CHAT_MODEL")
chave_google = os.getenv("GOOGLE_API_KEY")
modelo_embedding_google = os.getenv("GOOGLE_EMBEDDING_MODEL")
modelo_chat_google = os.getenv("GOOGLE_CHAT_MODEL")


def obter_embeddings():
    if chave_openai:
        return OpenAIEmbeddings(model=modelo_embedding_openai)
    if chave_google:
        return GoogleGenerativeAIEmbeddings(model=modelo_embedding_google)
    raise RuntimeError(
        "Defina OPENAI_API_KEY ou GOOGLE_API_KEY no .env para escolher o provedor de embeddings."
    )


def obter_llm():
    if chave_openai:
        return ChatOpenAI(model=modelo_chat_openai)
    if chave_google:
        return ChatGoogleGenerativeAI(model=modelo_chat_google)
    raise RuntimeError(
        "Defina OPENAI_API_KEY ou GOOGLE_API_KEY no .env para escolher o provedor da LLM."
    )


def montar_string_conexao():
    if url_banco_dados.startswith("postgresql://"):
        return url_banco_dados.replace("postgresql://", "postgresql+psycopg://", 1)
    return url_banco_dados
