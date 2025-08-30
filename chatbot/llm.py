"""
Model and chain builders.

This module isolates external dependencies (API keys, model selection) so tests and
UI code don't need to know implementation details.
"""

import os
from typing import cast

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI

from .prompts import system_prompt
from .types import Chain


def build_model(
    model: str = "gemini-2.5-flash", temperature: float = 0.7
) -> ChatGoogleGenerativeAI:
    """
    Build the Google Generative AI chat model.

    Args:
        model: Model name to use.
        temperature: Sampling temperature.

    Returns:
        A configured ChatGoogleGenerativeAI instance.

    Raises:
        RuntimeError: If GEMINI_API_KEY is not set.
    """
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not set; create a .env file or set the environment variable."
        )
    return ChatGoogleGenerativeAI(model=model, api_key=api_key, temperature=temperature)


def build_chain(model: ChatGoogleGenerativeAI | None = None) -> Chain:
    """
    Build the end-to-end LC pipeline: Prompt -> Model -> String output.

    Args:
        model: Optional prebuilt model. If None, `build_model()` is used.

    Returns:
        An object implementing the `Chain` protocol with `.invoke(dict) -> str`.
    """
    mdl = model or build_model()
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}"),
        ]
    )
    chain = prompt | mdl | StrOutputParser()
    # The composed object has .invoke(...) -> str at runtime; teach mypy with a cast.
    return cast(Chain, chain)
