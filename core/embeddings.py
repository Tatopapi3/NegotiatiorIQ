from openai import OpenAI
from core.config import OPENAI_API_KEY, EMBEDDING_MODEL

_client = OpenAI(api_key=OPENAI_API_KEY)


def embed(text: str) -> list[float]:
    """Return a 1536-dim embedding for the given text."""
    text = text.replace("\n", " ").strip()
    response = _client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding
