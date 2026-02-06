"""
Recipe Intelligence Chatbot - Streamlit Frontend.
Modern chat interface with recipe display and Local/OpenAI mode toggle.
"""

import os
import requests
import streamlit as st

# API URL (default 8001 to avoid port 8000 conflict; set RECIPE_API_BASE to override)
API_BASE = os.environ.get("RECIPE_API_BASE", "http://127.0.0.1:8001")


def render_recipe(recipe: dict) -> None:
    """Display recipe with bold headers, numbered steps, and nutrition sidebar."""
    with st.container():
        st.markdown(f"## {recipe.get('name', 'Recipe')}")
        col_main, col_nutrition = st.columns([3, 1])
        with col_main:
            st.markdown("### Ingredients")
            for ing in recipe.get("ingredients", []):
                st.markdown(f"- {ing}")
            st.markdown("### Steps")
            for i, step in enumerate(recipe.get("steps", []), 1):
                st.markdown(f"**{i}.** {step}")
        with col_nutrition:
            st.markdown("#### Nutrition Facts")
            st.metric("Prep Time", f"{recipe.get('prep_time_minutes', 0)} min")
            st.metric("Calories", f"{recipe.get('calories', 0)}")


def generate_recipe(ingredients: list[str], mode: str) -> dict | None:
    """Call FastAPI /generate-recipe and return parsed JSON."""
    try:
        r = requests.post(
            f"{API_BASE}/generate-recipe",
            json={"ingredients": ingredients, "mode": mode},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        detail = ""
        if hasattr(e, "response") and e.response is not None:
            try:
                body = e.response.json()
                detail = body.get("detail", str(body))
            except Exception:
                detail = e.response.text or str(e)
        # User-friendly messages for common cases (works for 401, 500 wrapping OpenAI errors, 503, connection errors)
        if e.response is not None:
            code = e.response.status_code
            detail_str = str(detail)
            detail_lower = detail_str.lower()
            if code == 401 or "invalid_api_key" in detail_lower or "incorrect api key" in detail_lower or ("api key" in detail_lower and "401" in detail_str):
                st.error("**OpenAI API key is invalid or expired.** Switch to **Local (Ollama)** in the sidebar (works with no API key), or set a valid `OPENAI_API_KEY` and restart the API.")
            elif code == 503 or "openai_api_key" in detail_lower:
                st.error("**OpenAI mode requires an API key.** Set `OPENAI_API_KEY` in your environment and restart the API, or switch to **Local (Ollama)** mode.")
            elif "connection" in detail_lower or "refused" in detail_lower:
                st.error("**Cannot reach Ollama.** Ensure Ollama is running and you have run `ollama pull llama3.1`. Then try again.")
            elif "with_structured_output" in detail_lower:
                st.error("**API needs a restart.** Stop the API (Ctrl+C in its terminal), then run: `python -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8001`")
            else:
                st.error(f"**API error:** {detail}")
        else:
            st.error(f"Request failed: {e}")
        return None


def main():
    st.set_page_config(
        page_title="Recipe Intelligence Chatbot",
        page_icon="",
        layout="wide",
    )
    st.title("Recipe Intelligence Chatbot")
    st.caption("Enter ingredients and get a professionally formatted recipe.")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "mode" not in st.session_state:
        st.session_state.mode = "local"

    mode = st.sidebar.radio(
        "LLM Mode",
        options=["local", "openai"],
        format_func=lambda x: "Local (Ollama Llama 3.1)" if x == "local" else "OpenAI (GPT-4o)",
        index=0 if st.session_state.mode == "local" else 1,
    )
    st.session_state.mode = mode
    st.sidebar.caption("Local works without any API key. OpenAI requires OPENAI_API_KEY in the API server environment.")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg.get("recipe"):
                render_recipe(msg["recipe"])
            else:
                st.markdown(msg["content"])

    if prompt := st.chat_input("Enter ingredients (e.g. Egg, Onions)"):
        ingredients = [x.strip() for x in prompt.split(",") if x.strip()]
        if not ingredients:
            st.warning("Please enter at least one ingredient.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Generating recipe..."):
                recipe = generate_recipe(ingredients, st.session_state.mode)
            if recipe:
                render_recipe(recipe)
                st.session_state.messages.append(
                    {"role": "assistant", "content": None, "recipe": recipe}
                )
            else:
                st.session_state.messages.append(
                    {"role": "assistant", "content": "Failed to generate recipe.", "recipe": None}
                )


if __name__ == "__main__":
    main()
