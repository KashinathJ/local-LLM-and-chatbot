# Recipe Intelligence Chatbot

A high-performance chatbot that suggests meals based on user ingredients. It supports **Local LLMs** (Ollama with Llama 3.1) and **Cloud LLMs** (OpenAI GPT-4o), with a FastAPI backend and Streamlit frontend.

## Architecture

- **Backend**: FastAPI (`src/api.py`) – POST `/generate-recipe`, Chef Persona system prompt, structured JSON output.
- **Frontend**: Streamlit (`src/bot.py`) – Chat UI with `st.chat_message`, recipe display (bold headers, numbered steps, Nutrition Facts sidebar), Local/OpenAI mode toggle.
- **Logic**: LangChain (`ChatOllama` / `ChatOpenAI`). OpenAI uses `with_structured_output`; Local (Ollama) uses JSON parsing from LLM text for compatibility.
- **Utils**: `src/utils.py` – Few-shot prompting dataset (10+ recipes) to guide LLM style.

## Modes (dynamic – works in all cases)

- **Local (default)** – Uses Ollama (Llama 3.1). No API key needed. Works as long as Ollama is running.
- **OpenAI** – Uses GPT-4o. Requires a valid `OPENAI_API_KEY` in the **API server’s** environment (not the browser). If the key is missing or invalid, the app shows a clear message and suggests using Local mode.

The UI defaults to **Local** so the app works without any key. Recipe generation remains **dynamic** (LLM-generated from your ingredients) in both modes.

## Ollama Setup (Local Mode)

1. Install [Ollama](https://ollama.ai).
2. Pull the model:

```bash
ollama pull llama3.1
```

## OpenAI (optional)

To use OpenAI mode, set your API key in the environment **before** starting the API server:

```powershell
$env:OPENAI_API_KEY = "sk-your-valid-key-here"
python -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8001
```

## Environment Setup

**Option A – Virtual environment (recommended):**

```powershell
cd task2
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Option B – Use system Python (if venv fails):**

```powershell
cd task2
pip install -r requirements.txt
```

On macOS/Linux use `source venv/bin/activate` and `uvicorn` / `streamlit` directly if they are on PATH.

## Run Instructions

Run from the **task2** folder. Use two terminals.

**Terminal 1 – Start the FastAPI server:**

```powershell
cd "C:\Users\Kashinath\Desktop\AI Assignment\Task2 Local LLM & chatbot\task2"
# If using venv: .\venv\Scripts\Activate.ps1
python -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8001
```

Or double-click **run_api.bat** (from within the task2 folder).

**Terminal 2 – Start the Streamlit chatbot:**

```powershell
cd "C:\Users\Kashinath\Desktop\AI Assignment\Task2 Local LLM & chatbot\task2"
# If using venv: .\venv\Scripts\Activate.ps1
python -m streamlit run src/bot.py
```

Or double-click **run_bot.bat**.

Then open the URL shown by Streamlit (e.g. `http://localhost:8501`).

**Important:** If you see *"500 Internal Server Error"* or *"OpenAI API key is invalid"* when using the chatbot:
1. **Use Local mode** – In the Streamlit sidebar, select **Local (Ollama Llama 3.1)**. No API key needed.
2. **Restart the API** – Stop the running API (Ctrl+C in Terminal 1), then start it again with the command above so the latest code (including Ollama JSON fallback) is loaded.
3. **OpenAI only with a valid key** – If you want OpenAI, set `OPENAI_API_KEY` to a valid key in the API server’s environment and restart the API.

## Sample Input / Output (Verification)

- **Input**: `Egg, Onions`
- **Expected**: A valid recipe JSON with `name`, `ingredients`, `steps`, `prep_time_minutes`, `calories` (e.g. "Caramelized Onion and Egg Scramble" or similar).
- **Verify**: In the chat, type `Egg, Onions` and confirm the recipe appears with bold headers, numbered steps, and Nutrition Facts in the sidebar.

## API

- **POST** `/generate-recipe`  
  Body: `{ "ingredients": ["Egg", "Onions"], "mode": "openai" }` or `"mode": "local"`  
  Response: Recipe object (name, ingredients, steps, prep_time_minutes, calories).

- **GET** `/health`  
  Returns `{"status": "ok", "service": "recipe-intelligence-api"}`.

## Project Layout

```
task2/
  src/
    __init__.py
    api.py      # FastAPI server
    bot.py      # Streamlit chat UI
    models.py   # Pydantic Recipe schema
    utils.py    # Few-shot dataset & Chef prompt
  requirements.txt
  README.md
```
