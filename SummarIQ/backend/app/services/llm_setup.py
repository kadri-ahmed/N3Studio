"""
LLM setup and initialization for LlamaIndex
Supports both GROQ and OpenAI providers
"""
from llama_index.llms.groq import Groq
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from app.core.config import settings


def get_llm():
    """Get LLM instance based on configured provider"""
    if settings.LLM_PROVIDER.lower() == "groq":
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required when using GROQ provider")
        return Groq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.1,
        )
    else:
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required when using OpenAI provider")
        return OpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=0.1,
        )


def get_embedding_model():
    """Get embedding model (currently using OpenAI embeddings)"""
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required for embeddings")
    return OpenAIEmbedding(
        api_key=settings.OPENAI_API_KEY,
        model=settings.EMBEDDING_MODEL,
    )

