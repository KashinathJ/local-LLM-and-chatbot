# Commands to Run – Recipe Intelligence Chatbot

**You must restart the API so it loads the latest code** (fixes 401 + "with_structured_output" for Local/Ollama).  
If the API is already running, press **Ctrl+C** in that terminal, then run the commands below.

---

## Step 1: Open two terminals

In both, go to the project folder:

```powershell
cd "C:\Users\Kashinath\Desktop\AI Assignment\Task2 Local LLM & chatbot\task2"
```

(If you use a venv, activate it: `.\venv\Scripts\Activate.ps1`)

---

## Step 2: Terminal 1 – Start the API

Use **port 8001** to avoid "WinError 10013" (port 8000 in use or blocked):

```powershell
python -m uvicorn src.api:app --reload --host 127.0.0.1 --port 8001
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
```

If you see `WinError 10013` or "address already in use", try another port (e.g. `--port 8002`) and set `$env:RECIPE_API_BASE = "http://127.0.0.1:8002"` before starting Streamlit.

Leave this terminal open. The API now has:
- **OpenAI**: your API key configured (use sidebar "OpenAI (GPT-4o)" in the bot).
- **Local (Ollama)**: JSON parsing (no `with_structured_output`); use sidebar "Local (Ollama Llama 3.1)".

---

## Step 3: Terminal 2 – Start the Streamlit chatbot

```powershell
python -m streamlit run src/bot.py
```

**Expected output:**

```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

Open **http://localhost:8501** in your browser.

---

## Step 4: Use the chatbot

- **Local (Ollama)**  
  - In the sidebar, select **Local (Ollama Llama 3.1)**.  
  - Ensure Ollama is running and you have run: `ollama pull llama3.1`  
  - In the chat, type e.g. **Egg, Onions** and send. You should get a generated recipe.

- **OpenAI (GPT-4o)**  
  - In the sidebar, select **OpenAI (GPT-4o)**.  
  - The API uses the configured key. Same input, e.g. **Egg, Onions**.

---

## Optional: Run scripts instead of raw commands

**Terminal 1:**

```powershell
.\run_api.ps1
```

**Terminal 2:**

```powershell
.\run_streamlit.ps1
```

---

## Optional: Test the API from PowerShell

(Use 8001; change if you started the API on another port.)

```powershell
# Health
Invoke-RestMethod -Uri "http://127.0.0.1:8001/health" -Method Get

# Generate recipe (Local – needs Ollama)
$body = '{"ingredients": ["Egg", "Onions"], "mode": "local"}'
Invoke-RestMethod -Uri "http://127.0.0.1:8001/generate-recipe" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 120

# Generate recipe (OpenAI)
$body = '{"ingredients": ["Egg", "Onions"], "mode": "openai"}'
Invoke-RestMethod -Uri "http://127.0.0.1:8001/generate-recipe" -Method Post -Body $body -ContentType "application/json" -TimeoutSec 60
```

---

## If the API runs on a different port (e.g. 8002)

Set the base URL before starting Streamlit:

```powershell
$env:RECIPE_API_BASE = "http://127.0.0.1:8002"
python -m streamlit run src/bot.py
```
