"""
Recipe Intelligence Chatbot - FastAPI Server.
Exposes /generate-recipe as a structured JSON service with Chef Persona.
"""

import json
import os
import re
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.models import Recipe
from src.utils import get_chef_system_prompt

# Default OpenAI key (used when OPENAI_API_KEY env is not set or empty). Override with env for production.
DEFAULT_OPENAI_KEY = "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"
_openai_from_env = (os.environ.get("OPENAI_API_KEY") or "").strip()
OPENAI_API_KEY = _openai_from_env or DEFAULT_OPENAI_KEY

app = FastAPI(
    title="Recipe Intelligence API",
    description="Generate recipes from ingredients using Local (Ollama) or Cloud (OpenAI) LLMs.",
    version="1.0.0",
)


class GenerateRecipeRequest(BaseModel):
    """Request body for recipe generation."""

    ingredients: list[str] = Field(
        ...,
        description="List of ingredient names (e.g. ['Egg', 'Onions'])",
        min_length=1,
    )
    mode: Literal["local", "openai"] = Field(
        default="local",
        description="Use 'local' for Ollama (Llama 3.1) or 'openai' for GPT-4o (requires OPENAI_API_KEY).",
    )


def get_llm(mode: Literal["local", "openai"]):
    """Return the appropriate LangChain chat model."""
    if mode == "openai":
        if not OPENAI_API_KEY:
            raise HTTPException(
                status_code=503,
                detail="OpenAI mode requires OPENAI_API_KEY. Set it in your environment or use Local mode (Ollama).",
            )
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o",
            api_key=OPENAI_API_KEY,
            temperature=0.7,
        )
    else:
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            model="llama3.1",
            temperature=0.7,
        )


def _extract_json_from_text(text: str) -> dict:
    """Extract a JSON object from LLM output (handles markdown code blocks or raw JSON)."""
    text = text.strip()
    # Try markdown code block first
    match = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", text)
    if match:
        return json.loads(match.group(1))
    # Try first { to last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return json.loads(text[start : end + 1])
    return json.loads(text)


@app.post("/generate-recipe", response_model=Recipe)
async def generate_recipe(request: GenerateRecipeRequest) -> Recipe:
    """
    Generate a single recipe based on the provided ingredients.
    Uses a Chef Persona system prompt. Both modes: invoke LLM, extract JSON, validate with Pydantic (no with_structured_output).
    """
    from langchain_core.messages import HumanMessage, SystemMessage

    try:
        llm = get_llm(request.mode)  # may raise 503 if openai and no key
        system_prompt = get_chef_system_prompt()
        ingredients_text = ", ".join(request.ingredients)
        user_message = f"Generate one recipe using these ingredients: {ingredients_text}"
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]

        # Same path for both Local and OpenAI: invoke → text → parse JSON → validate (avoids with_structured_output)
        response = llm.invoke(messages)
        content = response.content if hasattr(response, "content") else str(response)
        data = _extract_json_from_text(content)
        return Recipe.model_validate(data)
    except HTTPException:
        raise
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: LLM did not return valid JSON. ({e})")
    except Exception as e:
        err_msg = str(e).lower()
        # OpenAI invalid/expired key → return 401 so UI can suggest Local mode
        if "401" in err_msg or "invalid_api_key" in err_msg or "incorrect api key" in err_msg:
            raise HTTPException(
                status_code=401,
                detail="OpenAI API key is invalid or expired. Use Local (Ollama) mode or set a valid OPENAI_API_KEY.",
            )
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check for load balancers and monitoring."""
    return {"status": "ok", "service": "recipe-intelligence-api"}
