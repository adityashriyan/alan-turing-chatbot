# Alan Turing Chatbot

An AI‑powered chatbot inspired by **Alan Turing**, built with **Gradio** and **LangChain** using **Google Generative AI (Gemini)**. It provides a lightweight, modular codebase and a clean web UI to chat with a Turing‑like persona.

<img src="assets/AlanTuring.jpg" alt="Alan Turing" width="220" />

---

## 🎯 Highlights

- **Turing persona** with a concise, rigorous tone (editable in `chatbot/prompts.py`)
- **Gradio web UI** (`chatbot/ui/gradio_app.py`) for an easy, local chat experience
- **LangChain‑style pipeline** (`chatbot/llm.py`, `chatbot/chat.py`) with clean abstractions
- **Gemini backend** via `langchain-google-genai`
- **Developer tooling**: Makefile targets, pytest + coverage, ruff/black, mypy, pre‑commit, GitHub Actions CI

---

## 🔧 Prerequisites

- **Python**: 3.11 or 3.12 (matches CI matrix)
- A **Google Generative AI** API key (Gemini). You can create one from Google AI Studio.
- macOS/Linux/WSL or Windows (PowerShell): commands shown use a POSIX shell; adapt for PowerShell where needed.

---

## 🚀 Quickstart

```bash
# 1) Clone & enter the project
git clone <your-fork-or-repo-url>.git
cd alan-turing-chatbot

# 2) Create a virtualenv and install dependencies
make venv
make dev        # installs runtime + dev deps and sets up pre-commit

# 3) Set your API key
cp .env.example .env
# edit .env and set: GEMINI_API_KEY=your_google_gemini_api_key_here

# 4) Run the app
make run        # or: python main.py
```

By default, Gradio serves on http://127.0.0.1:7860/. Set `share=True` in `main.py` if you want a public link (not recommended for untrusted environments).

---

## 🧰 Project Structure

```
alan-turing-chatbot/
├─ assets/                    # Static assets (avatar, etc.)
│  └─ AlanTuring.jpg
├─ chatbot/                   # Application code
│  ├─ __init__.py
│  ├─ chat.py                 # Bridges UI message history ↔ LLM chain
│  ├─ llm.py                  # Model + chain builders (Gemini via LangChain)
│  ├─ prompts.py              # Turing persona + system prompt
│  ├─ types.py                # Lightweight typing protocols
│  └─ ui/
│     └─ gradio_app.py        # Gradio Blocks UI
├─ tests/                     # Pytest-based unit tests
│  ├─ test_chat.py
│  └─ test_prompts.py
├─ .pre-commit-config.yaml    # ruff + black + basic hygiene hooks
├─ github/workflows/ci.yml    # GitHub Actions: lint, typecheck, tests + coverage
├─ Makefile                   # Common dev tasks (venv, dev, test, lint, run, etc.)
├─ requirements.txt           # Runtime dependencies
├─ requirements-dev.txt       # Dev/test/tooling dependencies
├─ pyproject.toml             # Tooling configuration: black, ruff, mypy, pytest, coverage
├─ main.py                    # App entrypoint (launches Gradio UI)
├─ LICENSE
└─ README.md (this file)
```

---

## ⚙️ Configuration

The app uses **dotenv** to load environment variables from `.env`:

- `GEMINI_API_KEY` – your Google Generative AI key.

Model/provider configuration lives in `chatbot/llm.py`. To switch models or providers, adjust the builder function(s) there (e.g., change the Gemini model name, or swap in another LangChain chat model).

> **Note:** Unit tests do **not** require an API key (they mock the chain), so you can run the test suite without network access.

---

## 🧪 Tests & Coverage

```bash
# Run tests
make test          # or: pytest -q

# Coverage summary
make cov           # or: pytest -q --cov --cov-report=term-missing

# HTML coverage report (opens at htmlcov/index.html)
make cov-html
```

---

## 🧹 Linting, Formatting, Types

```bash
# Auto-fix style (ruff + black)
make format

# Lint (no writes) and type-check
make lint
make typecheck

# Run pre-commit hooks across the repo
make precommit
```

Tooling is configured in `pyproject.toml` and `.pre-commit-config.yaml`:

- **ruff** (linting, some formatting)
- **black** (code formatting)
- **mypy** (static types)
- **pytest/coverage** (tests)

---

## 🖥️ Running the App

```bash
# Recommended
make run

# Equivalent
python main.py
```

Gradio will start with a chat UI. Messages are routed through `AlanTuringChat` (in `chatbot/chat.py`) to a LangChain chain constructed in `chatbot/llm.py`, which uses the **Turing persona** system prompt from `chatbot/prompts.py` and the **Gemini** backend.

To customize the persona, edit `chatbot/prompts.py`. To adjust the chain (e.g., add tools, memory, or change the prompt), modify `chatbot/llm.py` accordingly.

---

## 🔒 Security & Privacy

- Keep your `.env` out of version control (already ignored by `.gitignore`).
- Never commit real API keys. Use environment variables and example files (`.env.example`).
- Treat publicly shared Gradio links as untrusted: they expose your local app to the internet.

---

## 🧭 Troubleshooting

- **`KeyError` / Authentication**: Ensure `.env` contains a valid `GEMINI_API_KEY` and that it’s exported in your shell if running outside of the repo root.
- **Model‑specific errors**: If Google updates model names or quotas, adjust `chatbot/llm.py` to point at an available model and verify your account quotas.
- **Port already in use (7860)**: Either stop the conflicting app or set `server_port` in Gradio (`launch(server_port=...)`).
- **Import errors**: Re‑install deps with `make dev` (or `pip install -r requirements.txt`).

---

## 🗺️ Roadmap Ideas

- Tool‑augmented answers (search, code execution, etc.) via LangChain tools
- Chat history persistence (local or DB)
- Dockerfile and Compose for containerized deployment
- Optional OpenAI or other providers via feature flags
- Simple evaluation harness for prompts

---

## 📄 License

This project is licensed under the **MIT License**. See `LICENSE` for details.
