# AI Development Instructions — Streamlit Data Dashboard

| 項目 | 内容 |
|---|---|
| 最終更新日 | 2026-06-21 |
| 対象プロジェクト | Streamlit + pandas + Plotly (With PyInstaller EXE & Data Science Guidelines) |
| バージョン | v2.0 |

> **For AI assistants**: GitHub Copilot, Cursor, Claude, ChatGPT, Gemini, and others.
> Follow every rule in this file precisely. If you are unsure, ask the developer before proceeding.
>
> **For beginners**: Every rule includes a "Why?" explanation. Read those before asking the AI to implement anything.

---

## 0. Core Philosophy

This project prioritizes **simplicity**, **maintainability**, **reproducibility**, **robust error handling**, and **security** in that order.

| Priority | Principle | Practical meaning |
|---|---|---|
| 1 | Simplicity | One file per concern. No unnecessary abstraction. |
| 2 | Maintainability | Each module has one job. Logic lives in one place only (strict separation of concerns). |
| 3 | Reproducibility | Data fetching is always explicit. Results can be reproduced by re-running. |
| 4 | Robust Error Handling | Never swallow exceptions. Log tracebacks and propagate errors to the UI layer. |
| 5 | Security | API keys stay in `.env`. Never hardcode secrets. Run vulnerability scans. |

When these conflict, always choose the higher-priority value.

---

## 1. Technology Stack (DO NOT CHANGE)

| Category | Technology | Version | Why this choice |
|---|---|---|---|
| Language | Python | 3.10+ | Modern type hints, match statements, walrus operator |
| UI Framework | Streamlit | 1.40+ | Pure Python UI — no HTML/CSS/JS required |
| Data manipulation | pandas | 2.0+ | Industry-standard DataFrame library for typical data sizes |
| Charting | Plotly | 5.20+ | Interactive charts; works natively in Streamlit |
| HTTP client | requests | 2.31+ | Simple, widely understood; no async complexity needed |
| Config | python-dotenv | 1.0+ | Keeps API keys out of source code |
| Package manager | uv | latest | Faster than pip; reproducible installs via `uv.lock` |
| E2E Testing | Playwright | 1.40+ | Headless browser; captures screenshots for verification |
| Excel parsing | openpyxl | latest | Safety backend engine for reading Excel files |
| Database | sqlite3 | built-in | Lightweight SQL storage for local datasets |
| EXE packaging | PyInstaller | latest | Windows standalone single-folder/EXE compilation |
| Security Check | pip-audit / Bandit | latest | Vulnerability audit for dependencies and static analysis |

### Non-negotiable constraints

- **Package manager**: `uv` only. Never use `pip`, `poetry`, or `pipenv`.
  > Why: `uv` produces a lockfile (`uv.lock`) that guarantees every developer installs the exact same versions.
- **UI**: Streamlit only. Never add React, Vue, Flask, or FastAPI to this project.
  > Why: Streamlit lets you build interactive data apps with pure Python. Adding another framework creates two conflicting web servers.
- **Charting**: Plotly only. Never mix in Matplotlib, Bokeh, or Altair (unless explicit manufacturing visualization exceptions apply).
  > Why: Plotly charts are interactive (zoom, hover, filter) and integrate natively with Streamlit via `st.plotly_chart()`.
- **Data fetching**: `requests` only (synchronous). Never use `aiohttp` or `httpx` async in data modules.
  > Why: Streamlit runs in a synchronous context. Async HTTP calls require extra event-loop management.
- **Caching**: Always use `@st.cache_data` on data-fetching functions.
  > Why: Without caching, every user interaction re-fetches from the source, making the app slow and hitting limits.

---

## 2. Directory Structure

Every file has exactly one responsibility. Do not put logic where it does not belong.

```
project/
├── app.py                  # Entrypoint: page config, tab orchestration, top-level try-except
├── launcher.py             # EXE packaging launcher wrapper (starts server & opens browser)
├── build.bat               # Windows EXE build batch script (PyInstaller definition)
├── config.py               # ONLY: constants, default values, API endpoint URLs, colors
├── logger_config.py        # Central logging setup: outputs to stderr and app.log (UTF-8)
├── generate_dummy_data.py  # Local demo data creation (CSV/Excel/SQLite)
├── pyproject.toml          # Dependency definitions
├── .env                    # NOT committed — contains API keys
├── .env.example            # Committed — template file for dotenv configurations
├── .gitignore              # Defines git ignore rules (includes .env, logs, pycaches)
│
├── data/                   # ONLY: fetch/read data from sources, return DataFrames (no st.*)
│   ├── __init__.py         # Re-export fetch functions
│   ├── worldbank.py        # World Bank GDP / IMF GDP growth
│   ├── fred.py             # FRED (Federal Reserve) API
│   ├── estat.py            # e-Stat (Japan government statistics) API
│   ├── local_csv.py        # Local CSV file reader
│   ├── local_excel.py      # Local Excel file reader
│   ├── local_sqlite.py     # Local SQLite database reader
│   └── dummy/              # Generated local dummy datasets (not committed)
│       ├── gdp_data.csv
│       ├── gdp_data.xlsx
│       └── gdp_data.sqlite
│
├── views/                  # ONLY: Streamlit UI rendering (st.* calls live here)
│   ├── __init__.py         # Re-export render functions
│   ├── page_config.py      # st.set_page_config, CSS overrides
│   ├── sidebar.py          # st.sidebar widgets, return user inputs as dict
│   ├── components.py       # Reusable UI fragments (CSV download buttons, tables)
│   ├── worldbank_tab.py    # World Bank GDP screen
│   ├── imf_tab.py          # IMF GDP growth screen
│   ├── japan_tab.py        # Japan economic indicators screen
│   ├── local_csv_tab.py    # Local CSV area chart tab
│   ├── local_sqlite_tab.py # Local SQLite grouped bar chart tab
│   └── local_excel_tab.py  # Local Excel dashdot line chart tab
│
└── docs/
    ├── spec.md             # How to build it (API specs, layouts, exception patterns)
    ├── implementation_plan.md
    ├── task.md             # Current Todo list
    ├── walkthrough.md      # Testing and verification report
    └── AI_Python_製造業分析フレームワーク_EUC向け.md # Domain Guide (EUC analysis guidelines)
```

### One-responsibility rule (enforce strictly)

| File/Folder | Allowed | Forbidden |
|---|---|---|
| `app.py` | page layout, tab creation, call `render_*` and `fetch_*`, top-level `try-except` catch | business logic, chart creation, direct API calls |
| `config.py` | constants, default lists, API base URLs | computation, imports from `data/` or `views/` |
| `data/*.py` | API calls, file read, JSON parsing, raise exceptions on failure | `st.*` calls, chart creation, global state |
| `views/*.py` | `st.*` calls, build charts, render tables | API calls, database execution, raw data fetching |
| `sidebar.py` | `st.sidebar.*` widgets, return `dict` of user inputs | data fetching, chart rendering |
| `logger_config.py` | logging initialization, file handler path config | import of streamlit, data layers, or views |

---

## 3. Implementation Order (ALWAYS follow this sequence)

```
1. config.py   → define constants, API URLs, default values
      ↓
2. data/       → fetch/read functions that return DataFrames (one file per source, raise errors)
      ↓
3. views/      → render functions that display DataFrames as charts/tables
      ↓
4. app.py      → wire everything together (tabs, sidebar, logger config, try-except blocks)
      ↓
5. tests/      → E2E tests with Playwright
      ↓
6. docs/       → spec and test report
```

---

## 4. Coding Rules

### 4-1. data/ — Data Fetching & Extraction (Updated!)

Every data-fetching function MUST log errors with tracebacks and propagate exceptions:

```python
import pandas as pd
import requests
import streamlit as st
import logging

logger = logging.getLogger(__name__)

# REQUIRED: cache all data-fetching/loading functions
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_worldbank_gdp(country_codes: tuple[str, ...], start_year: int, end_year: int) -> pd.DataFrame:
    """
    Returns a DataFrame with columns: country, year, gdp_usd
    Raises RuntimeError on connection, timeout, HTTP, or parser errors.
    """
    url = f"https://api.worldbank.org/v2/country/{';'.join(country_codes)}/indicator/NY.GDP.MKTP.CD"
    params = {"format": "json", "per_page": 500, "mrv": end_year - start_year + 1}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        # ... parse and prepare records
        if not records:
             raise ValueError("選択した条件に該当するデータが見つかりませんでした。")
        return pd.DataFrame(records)
    except requests.exceptions.Timeout as e:
        err_msg = "世界銀行 API からの応答がタイムアウトしました。"
        logger.error(f"{err_msg} Details: {e}", exc_info=True)  # REQUIRED: exc_info=True
        raise RuntimeError(err_msg) from e
    except requests.exceptions.RequestException as e:
        err_msg = f"世界銀行 API との通信に失敗しました: {e}"
        logger.error(err_msg, exc_info=True)
        raise RuntimeError(err_msg) from e
    except Exception as e:
        err_msg = f"世界銀行データの解析中に予期しないエラーが発生しました: {e}"
        logger.error(err_msg, exc_info=True)
        raise RuntimeError(err_msg) from e
```

**REQUIRED patterns in data/:**
- `@st.cache_data(ttl=...)` on EVERY fetch/load function — no exceptions. Set appropriate TTL.
- Arguments must be hashable (`tuple`, `str`, `int`, `bool`) — NOT `list` or `dict`.
- **Do NOT swallow errors.** For actual errors (network, parsing, SQLite connectivity, missing critical dependencies), log the traceback using `logger.error("...", exc_info=True)` and raise a descriptive `RuntimeError`.
- If a query is successful but logically returns no rows, return an empty `pd.DataFrame()`.
- Always set `timeout=` on every `requests.get()` call.
- Use `logger.warning()` / `logger.error(..., exc_info=True)` — never `print()`.

**FORBIDDEN in data/:**
- `st.*` calls of any kind (no `st.error()`, `st.spinner()`, `st.write()`).
- Returning `None` — always return a DataFrame on success (or empty result) or raise an exception.
- Hardcoded API keys — always read from `os.environ` (via dotenv).

---

### 4-2. views/ — UI Rendering

Every render function MUST handle empty data gracefully and structure Plotly layouts correctly:

```python
import pandas as pd
import plotly.express as px
import streamlit as st

def render_gdp_chart(df: pd.DataFrame, title: str = "GDP Comparison") -> None:
    # Check for empty data
    if df.empty:
        st.warning("データを取得できませんでした。条件を変えて再試行してください。")
        return

    fig = px.line(
        df,
        x="year",
        y="gdp_usd",
        color="country",
        title=title,
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig, use_container_width=True)  # ALWAYS use_container_width=True
```

**REQUIRED patterns in views/:**
- Check `df.empty` before rendering chart details.
- Always use `use_container_width=True` on `st.plotly_chart()` and `st.dataframe()`.
- Keep rendering logic free of database queries or API fetching.

---

### 4-3. app.py — Top-Level Orchestrator & Try-Except Catching

`app.py` is the entry point. It manages session state, runs setup configurations, and handles exceptions bubbling up from the data layer:

```python
import streamlit as st
import logging
from data.worldbank import fetch_worldbank_gdp
from views.worldbank_tab import render_wb_dashboard
from logger_config import setup_logging

# Configure logging at startup (once)
setup_logging()
logger = logging.getLogger("app")

def main() -> None:
    # Sidebar rendering...
    inputs = render_sidebar()
    
    if inputs["execute"]:
        try:
            with st.spinner("データ取得中..."):
                # Fetching data - propagates exceptions on errors
                st.session_state["data"] = fetch_worldbank_gdp(inputs["codes"], 2010, 2025)
            st.toast("データ取得に成功しました！", icon="✅")
        except RuntimeError as exc:
            # Catch exceptions from data layer, log with exc_info, and show to user
            logger.error(f"データ取得中にエラーが発生しました: {exc}", exc_info=True)
            st.error(f"⚠️ エラー: {exc}")
            st.session_state.pop("data", None) # clear old cache data
```

---

## 5. Error Handling & Exception Propagation Policy

- **Do NOT Swallow Exceptions**: The data layer (`data/*.py`) must raise exceptions (e.g. `RuntimeError` or `ValueError`) on API failures, socket timeouts, DB failures, or parser failures. It must not return an empty DataFrame as a fallback for actual failures.
- **Traceback Logging**: The error must be logged with `logger.error("...", exc_info=True)` to record the full stack trace in `app.log` before raising, or caught and logged by the controller.
- **UI Presentation**: The orchestrator (`app.py`) must catch the exception, pop the corresponding cache key from `st.session_state`, and display a clean, localized error message using `st.error(...)`.

---

## 6. Caching Strategy & Caching Traps

- **Unhashable Argument Trap**:
  - `st.cache_data` uses argument values to construct cache keys.
  - Passing a `list` or `dict` raises `UnhashableTypeError`.
  - **Correction**: Always convert lists to tuples before passing them to cached functions:
    ```python
    # ✅ OK
    fetch_gdp(country_codes=tuple(selected_countries))
    # ❌ Fails
    fetch_gdp(country_codes=selected_countries) # where selected_countries is a list
    ```
- **Stale Cache / Local File Updates**:
  - If a cached function reads a local file (`data/dummy/gdp_data.csv`), updating the file on disk will not refresh the Streamlit display if the TTL is high.
  - **Correction**: Set a shorter TTL for local file reads (`ttl=3600` or less) and implement a "Refresh Cache" button that triggers `st.cache_data.clear()` followed by `st.rerun()`.

---

## 7. Logging Configuration

- Logging configuration must be initialized **exactly once** at the application start via `logger_config.py` using `setup_logging()`.
- **Dual Destination**: Write log messages to both `stderr` (console output) and `app.log` (local text file).
- **Encoding**: The `app.log` file must be written in `UTF-8` encoding to prevent encoding failures on Japanese Windows systems.
- **Log Path Resolution**:
  - In normal environments: Resolve `app.log` relative to the script directory (`Path(__file__).parent`).
  - In a compiled EXE environment: Resolve `app.log` relative to the executable path (`Path(sys.executable).parent`).

---

## 8. Windows Standalone EXE (PyInstaller) Packaging

When compiling Streamlit applications into standalone Windows executables, standard file paths break because the application code is extracted to a temporary directory (`sys._MEIPASS`).

### 8-1. Path Resolution Template

All file access (reading `.env`, writing logs, querying SQLite, loading dummy files) must determine path locations dynamically:

```python
import sys
from pathlib import Path

# Resolve base directories dynamically
if getattr(sys, "frozen", False):
    # Running inside PyInstaller compiled EXE
    base_dir = Path(sys._MEIPASS)            # Contains bundled read-only code/static files
    exe_dir = Path(sys.executable).parent    # Contains the actual executable directory
else:
    # Running as normal script
    base_dir = Path(__file__).parent         # Project root
    exe_dir = base_dir
```

#### Application Rules:
- **User Modifiable / Output Files** (such as `.env`, SQLite files `data/dummy/gdp_data.sqlite`, and `app.log`) must be read and written relative to **`exe_dir`** (so they remain persistent and modifiable).
- **Static Templates / Source Files** must be read relative to **`base_dir`**.

### 8-2. Streamlit Launcher (launcher.py)
Streamlit cannot run natively inside a single EXE without a launcher. `launcher.py` starts the Streamlit server on a background thread and waits for the server port to respond before launching the system's default browser:

```python
# launcher.py template
import sys
import multiprocessing
import streamlit.web.bootstrap as bootstrap

if __name__ == "__main__":
    multiprocessing.freeze_support()
    # Configure streamlit arguments and run bootstrapper
    sys.argv = ["streamlit", "run", "app.py", "--global.developmentMode=false"]
    bootstrap.run("app.py", "", [], flag_options={})
```

### 8-3. PyInstaller Cautions
- **Hidden Imports**: PyInstaller cannot statically analyze Streamlit imports. Specify `--hidden-import` configurations for streamlit libraries or third-party engines (`openpyxl`, `sqlite3`, etc.) in `build.bat` or `.spec` files.
- **Console Mode vs Windowed Mode**: Ensure logging is directed to `app.log` if running in windowed mode (`--noconsole`), as stdout/stderr will be unavailable.

---

## 9. Security Audit & Scan Protocols

Always perform dependency audits and static code security scans before deployment.

### 9-1. Dependency Scan (pip-audit)
Checks installed packages for known vulnerabilities.
```bash
uv run pip-audit
```

### 9-2. Static Analysis Scan (Bandit)
Analyzes code for security flaws (e.g. SQL injections, insecure usage of subprocesses, hardcoded secrets).
```bash
uv run bandit -r app.py config.py data/ views/
```

---

## 10. Data Science & Manufacturing Advisor Guidelines

When building analytical tools for manufacturing domains or non-technical business users (EUC), follow these scientific principles to maintain reliability:

### 10-1. Correlation vs. Causation (相関関係と因果関係)
- **Guidelines**: High mathematical correlation between two manufacturing variables (e.g., Boiler Temperature X and Yield Y) does not imply causation.
- **Rule**: AI must explain to the user that analytical findings need to be validated with process domain knowledge (physical, chemical, mechanical) before implementing process changes.

### 10-2. Outlier and Anomaly Handling (異常値と外れ値)
- **Guidelines**: Sensor noise/glitches must be separated from actual physical process anomalies.
- **Rule**: Do not blindly apply `dropna()` or simple `fillna(mean)`. Ensure the code implements threshold filters that isolate system faults (e.g., dropouts) while flagging physical spikes for technical investigation.

### 10-3. Concept Drift / Model Degradation (概念ドリフト)
- **Guidelines**: Mechanical wear, seasons (humidity/temp changes), and batch variations will degrade predictive models over time.
- **Rule**: Design code structures to support periodic retraining, and provide metrics checking to alert users if model error shifts beyond an acceptable standard deviation.

### 10-4. GIGO (Garbage In, Garbage Out)
- **Guidelines**: Advanced algorithms cannot save poor-quality data.
- **Rule**: Put effort into data validation (checking schema, values within bounds, consistency of columns) rather than over-engineering model complexity.

### 10-5. Large-Scale Data Processing (>100MB)
- When data files exceed 100MB, do NOT use standard pandas for IO operations.
- **Polars** (`import polars as pl`): Utilize Polars for fast parallel processing.
- **DuckDB** (`import duckdb`): Direct in-memory SQL execution over CSVs or Parquet.
- **Parquet Format**: Use binary `.parquet` storage instead of `.csv` or `.xlsx` for storage space reduction and high-speed parsing.

---

## 11. Rules for AI Assistants (How to Avoid Getting Confused)

These instructions prevent AI assistants from breaking configurations, repeating errors, or confusing codebases during "vibe coding".

### 11-1. Behavior & Constraint Checklist
1. **Never Revert Exception Policy**: Do not swallow exceptions in `data/` functions and return `pd.DataFrame()`. Always log tracebacks and raise `RuntimeError`.
2. **Never Hardcode Path Resolving**: Never write static paths like `data/dummy/gdp_data.csv`. Always use the `sys.frozen` dynamic path resolution pattern.
3. **No Unhashable Arguments**: Ensure `@st.cache_data` functions only use tuples, strings, integers, or booleans. Inspect calling structures to make sure lists are cast to tuples.
4. **Command Execution**: Do not propose POSIX commands (like `rm -rf` or `cp`) if the user is running Windows PowerShell/CMD. Use PowerShell commands (`Remove-Item`, `Copy-Item`) or standard python library commands.
5. **No Ad-Hoc Dependencies**: Never import packages not listed in PyProject.toml without asking for permission first.
6. **No Swallow of Logs**: Verify that `logger_config.py` is called once in `app.py` before logging statements occur.
7. **Document Updates**: When adding a new feature, update the corresponding `docs/` Markdown file (`spec.md`, `walkthrough.md`, etc.).

---

## 12. Common Commands

```bash
# Install dependencies
uv sync

# Start the Streamlit app locally
uv run streamlit run app.py

# Package application to standalone EXE
build.bat

# Run dependency security audit
uv run pip-audit

# Run static code security scan
uv run bandit -r app.py config.py data/ views/

# Run Playwright E2E tests (run in separate terminal)
uv run pytest tests/e2e/ -v
```
