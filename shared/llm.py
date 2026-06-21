"""Provider-flexible LLM helpers for the 90-Day Agentic AI course.

One small module so every exercise can call a model the same way,
whether you use OpenAI, Azure OpenAI, or a free local model via Ollama.
Configure your choice in `.env` (copy from `.env.example`).

    from shared.llm import chat
    print(chat([{"role": "user", "content": "Hello!"}]))

Nothing here runs until you call a function, so importing is cheap and
won't fail just because a provider isn't configured yet.
"""
from __future__ import annotations

import os
from typing import Any

try:
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:  # dotenv is optional for days 1–3
    pass


def _provider() -> str:
    return os.getenv("LLM_PROVIDER", "ollama").lower().strip()


def _client_and_model() -> tuple[Any, str]:
    """Build an OpenAI-compatible client + model name for the chosen provider."""
    provider = _provider()

    # Azure uses a dedicated client class.
    if provider == "azure":
        from openai import AzureOpenAI
        client = AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        )
        return client, os.environ["AZURE_OPENAI_DEPLOYMENT"]

    # OpenAI and Ollama both speak the standard OpenAI client.
    from openai import OpenAI

    if provider == "openai":
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        return client, os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if provider == "ollama":
        client = OpenAI(
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key="ollama",  # Ollama ignores this but the SDK requires a value
        )
        return client, os.getenv("OLLAMA_MODEL", "llama3.1")

    raise ValueError(
        f"Unknown LLM_PROVIDER={provider!r}. Use 'openai', 'azure', or 'ollama'."
    )


def chat(messages: list[dict], temperature: float = 0.7, model: str | None = None, **kwargs) -> str:
    """Send chat `messages` and return the assistant's text reply.

    `messages` is a list like:
        [{"role": "system", "content": "..."},
         {"role": "user",   "content": "..."}]

    Pass `model=` to override the provider's default model (used by the
    model-routing lesson in the Advanced Track). On Azure this is a deployment name.
    """
    client, default_model = _client_and_model()
    resp = client.chat.completions.create(
        model=model or default_model, messages=messages, temperature=temperature, **kwargs
    )
    return resp.choices[0].message.content or ""


def chat_with_tools(messages: list[dict], tools: list[dict], temperature: float = 0.2):
    """Return the full assistant message so callers can read `.tool_calls`.

    Used from Day 8 onward for native function/tool calling.
    """
    client, model = _client_and_model()
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=temperature,
    )
    return resp.choices[0].message


def embed(texts):
    """Return embedding vector(s) for text — used from the embeddings lesson onward.

    Pass a string or a list of strings; always returns a list of vectors.
    Configure an embedding model per provider:
      - OpenAI : OPENAI_EMBED_MODEL          (default text-embedding-3-small)
      - Azure  : AZURE_OPENAI_EMBED_DEPLOYMENT
      - Ollama : OLLAMA_EMBED_MODEL           (default nomic-embed-text;
                 first run `ollama pull nomic-embed-text`)
    """
    provider = _provider()

    if provider == "azure":
        from openai import AzureOpenAI
        client = AzureOpenAI(
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        )
        model = os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT", "text-embedding-3-small")
    else:
        from openai import OpenAI
        if provider == "openai":
            client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
            model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small")
        else:  # ollama
            client = OpenAI(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key="ollama",
            )
            model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

    if isinstance(texts, str):
        texts = [texts]
    resp = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in resp.data]


if __name__ == "__main__":  # quick smoke test:  python shared/llm.py
    print(f"Provider: {_provider()}")
    print(chat([{"role": "user", "content": "Say hello in 5 words."}]))
