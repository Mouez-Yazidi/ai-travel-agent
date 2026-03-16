# AI Travel Agent

A modular **AI-powered travel planner** that, for a given city, suggests must-see attractions, fetches live weather, and generates a short 1-day itinerary. The pipeline is implemented as a **LangGraph** workflow and uses **Groq** for the LLM and **OpenWeather** for weather data.

---

## Table of Contents

- [Solution Overview](#solution-overview)
- [Added Value](#added-value)
- [Key Features](#key-features)
- [Prerequisites](#prerequisites)
- [Technical Guide](#technical-guide)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running the Notebook](#running-the-notebook)
- [Troubleshooting](#troubleshooting)

---

## Solution Overview

The application is a **stateful workflow** that runs in three steps:

1. **Attractions** — The LLM suggests 5 must-see attractions for the chosen city.
2. **Weather** — The OpenWeather API returns current conditions; the LLM turns this into a short traveler-oriented weather summary.
3. **Itinerary** — The LLM produces a 1-day plan that combines the suggested attractions and the weather summary.

Data flows through a shared **state** (city, attractions, weather, itinerary). The graph is defined with **LangGraph** and executed as a single invocation; each node reads from and writes to the state.

---

## Added Value

- **Single input, full plan** — One city name yields attractions, weather context, and a concise itinerary.
- **Live data** — Weather is real-time from OpenWeather, not generic or hard-coded.
- **Traveler-focused** — Prompts are tuned for weekend/short trips and readability.
- **Modular design** — Logic is split into config, state, LLM, tools, nodes, and graph so you can change or extend parts (e.g. add flights, hotels) without rewriting the whole flow.
- **Reproducible** — Same city and env gives a deterministic structure; only LLM and API responses may vary.

---

## Key Features

| Feature | Description |
|--------|-------------|
| **LangGraph workflow** | Linear graph: `attractions → weather → itinerary` with typed state. |
| **Groq LLM** | Uses `qwen/qwen3-32b` for fast, cost-effective text generation. |
| **OpenWeather integration** | Metric units, current conditions, and optional traveler summary. |
| **Typed state** | `State` TypedDict for clear contracts between nodes. |
| **Env-based config** | API keys and settings via `.env` (no hardcoded secrets). |
| **CLI entry point** | `run.py` with optional city argument for quick runs. |
| **Streamlit app** | Web UI with a travel-themed design; run with `streamlit run streamlit_app.py`. |
| **Notebook** | `test.ipynb` for interactive experimentation. |

---

## Prerequisites

- **Python** 3.10 or 3.11+ recommended.
- **API keys** (see [Configuration](#configuration)):
  - **Groq** — [Groq Console](https://console.groq.com/) (for the LLM).
  - **OpenWeather** — [OpenWeather](https://openweathermap.org/api) (for weather).
- **pip** (or another Python package manager) to install dependencies.

---

## Technical Guide

### 1. Clone or download the project

Ensure you have the project folder (e.g. `ai travel agent`) on your machine.

### 2. Create a virtual environment (recommended)

```bash
cd "ai travel agent"
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**  
  `.\.venv\Scripts\Activate.ps1`
- **Windows (CMD):**  
  `.\.venv\Scripts\activate.bat`
- **macOS/Linux:**  
  `source .venv/bin/activate`

### 3. Install dependencies

From the project root:

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and add your keys:

```bash
copy .env.example .env   # Windows
# or: cp .env.example .env   # macOS/Linux
```

Then edit `.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
OPEN_WEATHER_API_KEY=your_openweather_api_key_here
```

The app also accepts `OPENWEATHER_API_KEY` if you prefer that name.  
Do not commit `.env`; keep it in `.gitignore`.

### 5. Run the agent

Default city (Tunis):

```bash
python run.py
```

Another city:

```bash
python run.py Paris
python run.py "New York"
```

Example output:

```
Top Attractions: ['Eiffel Tower', 'Louvre Museum', ...]

Weather Summary: Clear skies, 18°C. Ideal for walking...

Itinerary: Start at the Eiffel Tower in the morning...
```

### 6. Run the Streamlit app (optional)

From the project root:

```bash
streamlit run streamlit_app.py
```

The app opens in your browser: enter a city, click **Generate plan**, and view attractions, weather summary, and itinerary in a travel-themed layout. Use the sidebar for a short description and quick city buttons.

### 7. Use the graph in your own code

```python
from graph import app

result = app.invoke({"city": "Tokyo"})
print(result["attractions"])
print(result["weather"])
print(result["itinerary"])
```

---

## Project Structure

```
ai travel agent/
├── .env                    # API keys (create from .env.example, do not commit)
├── README.md                # This file
├── requirements.txt        # Python dependencies
├── run.py                  # CLI entry point
├── streamlit_app.py        # Streamlit web app
├── state.py                # Shared state TypedDict
├── config.py               # Env loading and API key helpers
├── llm.py                  # Groq ChatGroq client
├── graph.py                # LangGraph workflow definition and compiled app
├── test.ipynb              # Jupyter notebook for experimentation
├── tools/
│   ├── __init__.py
│   └── weather.py          # OpenWeather tool (LangChain @tool)
└── nodes/
    ├── __init__.py
    ├── attractions.py      # Node: suggest attractions
    ├── weather.py          # Node: fetch weather + summarize
    └── itinerary.py       # Node: create 1-day itinerary
```

- **state.py** — Defines the state schema used by the graph.
- **config.py** — Loads `.env` and exposes `GROQ_API_KEY` and `OPENWEATHER_API_KEY`.
- **llm.py** — Builds the Groq LLM instance (used by all nodes that need generation).
- **tools/weather.py** — Calls OpenWeather and returns a formatted string; used by the weather node.
- **nodes/** — Each node takes the current state, returns a partial state update.
- **graph.py** — Builds the `StateGraph`, adds nodes and edges, compiles to `app`.

---

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | Yes | Groq API key for the LLM. |
| `OPEN_WEATHER_API_KEY` or `OPENWEATHER_API_KEY` | Yes for weather | OpenWeather API key; weather node fails gracefully if missing. |

Optional: adjust the model or temperature in `llm.py` (e.g. `model="llama-3.1-70b-versatile"`, `temperature=0.2`).

---

## Usage

- **Streamlit:** `streamlit run streamlit_app.py` — open in browser, enter city, click **Generate plan**.
- **CLI:** `python run.py [city]`
- **Programmatic:** `from graph import app; app.invoke({"city": "CityName"})`
- **Notebook:** Open `test.ipynb`, run cells top to bottom (ensure kernel uses the same env where you installed dependencies).

---

## Running the Notebook

1. Install dependencies and set up `.env` as above.
2. Open `test.ipynb` in Jupyter or VS Code.
3. Select the kernel that uses your project virtual environment.
4. Run all cells in order; the last cell invokes the graph with `{"city": "Tunis"}` and prints attractions, weather summary, and itinerary.

The notebook mirrors the modular flow (state, LLM, tools, nodes, graph) so you can tweak prompts or inputs and re-run without changing the packaged code.

---

## Troubleshooting

| Issue | What to do |
|-------|------------|
| `GROQ_API_KEY is not set` | Add `GROQ_API_KEY=...` to `.env` in the project root and ensure `python-dotenv` is installed. |
| Weather always "not available" | Set `OPEN_WEATHER_API_KEY` or `OPENWEATHER_API_KEY` in `.env`; check key at [OpenWeather](https://openweathermap.org/api). |
| `ModuleNotFoundError` for `state`, `graph`, etc. | Run scripts from the project root (e.g. `python run.py`) so the project directory is on `sys.path`. |
| Import errors in notebook | Set the notebook kernel to the virtual environment where you ran `pip install -r requirements.txt`. |
| Empty or odd attractions list | The LLM may return prose or numbering; the node splits by newline and strips. You can tighten the prompt in `nodes/attractions.py` (e.g. "one per line, no numbering"). |

---

## License and Credits

- **LangGraph** / **LangChain** — workflow and LLM orchestration.
- **Groq** — hosted LLM (Qwen).
- **OpenWeather** — weather data.

This project is for demonstration and learning; use it as a base for your own travel or assistant applications.
