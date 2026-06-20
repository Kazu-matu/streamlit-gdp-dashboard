"""
Streamlit ダッシュボード開発テンプレート生成スクリプト

使い方:
    python create_template.py <アプリ名>
    python create_template.py my_dashboard

生成されるフォルダ:
    ../<アプリ名>/   <- このフォルダをコピーして開発開始

生成後の GitHub 登録手順:
    cd ../<アプリ名>
    git init && git add . && git commit -m "chore: initial template"
    gh repo create <アプリ名> --public --source=. --remote=origin --push
    gh repo edit <アプリ名> --template
"""

import sys
import shutil
from pathlib import Path
from datetime import date


# ─────────────────────────────────────────────
# ヘルパー
# ─────────────────────────────────────────────

def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  作成: {path.relative_to(path.parents[len(path.parts) - 2])}")


def touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.touch()
    print(f"  作成: {path.relative_to(path.parents[len(path.parts) - 2])}")


def copy_doc(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copy2(src, dst)
        print(f"  コピー: {dst.relative_to(dst.parents[len(dst.parts) - 2])}")
    else:
        print(f"  スキップ（元ファイルなし）: {src}")


# ─────────────────────────────────────────────
# メイン
# ─────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        print("使い方: python create_template.py <アプリ名>")
        print("例    : python create_template.py my_dashboard")
        sys.exit(1)

    app_name = sys.argv[1].strip()
    if not app_name.isidentifier():
        print(f"エラー: アプリ名 '{app_name}' は Python の識別子として有効な名前にしてください")
        print("       （英数字とアンダースコアのみ、先頭は英字）")
        sys.exit(1)

    here   = Path(__file__).parent
    target = here.parent / app_name

    if target.exists():
        ans = input(f"'{target}' はすでに存在します。上書きしますか？ [y/N]: ")
        if ans.lower() != "y":
            print("中断しました。")
            sys.exit(0)
        shutil.rmtree(target)

    print(f"\nテンプレートを作成しています: {target}\n")
    today = date.today().isoformat()

    # ─── 1. pyproject.toml ───────────────────────────────────────────
    write(target / "pyproject.toml", f"""\
[project]
name = "{app_name}"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "streamlit>=1.40",
    "pandas>=2.0",
    "plotly>=5.20",
    "requests>=2.31",
    "python-dotenv>=1.0",
    "pyinstaller>=6.21.0",
]

[dependency-groups]
dev = [
    "playwright>=1.44.0",
    "pytest>=8.0.0",
    "pytest-playwright>=0.5.0",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
""")

    # ─── 1-2. logger_config.py ───────────────────────────────────────
    write(target / "logger_config.py", """\
\"\"\"
logger_config.py — アプリ全体のロギングを設定するモジュール。
\"\"\"
import sys
import logging
from pathlib import Path

def setup_logging():
    \"\"\"ロギングシステムをセットアップする。

    標準エラー出力と `app.log` の両方に出力する。
    EXE起動時は、実行ファイル本体と同階層に `app.log` を配置する。
    \"\"\"
    root_logger = logging.getLogger()
    
    # 既にハンドラが定義済みの場合は再設定をスキップ
    if root_logger.handlers:
        return
        
    if getattr(sys, "frozen", False):
        log_dir = Path(sys.executable).parent
    else:
        log_dir = Path(__file__).parent
        
    log_file = log_dir / "app.log"
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    
    root_logger.setLevel(logging.INFO)
    
    # 1. コンソール出力 (標準エラー)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # 2. ファイル出力 (UTF-8)
    try:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        logging.getLogger("logger_config").info(f"Logging initialized. File: {log_file}")
    except Exception as exc:
        logging.getLogger("logger_config").warning(f"Failed to initialize file logging: {exc}")
""")

    # ─── 2. .env.example ─────────────────────────────────────────────
    write(target / ".env.example", """\
# 環境設定テンプレート
# このファイルをコピーして .env を作成してください
#   cp .env.example .env   (Mac/Linux)
#   copy .env.example .env (Windows)

# -------------------------------------------------------------------
# 外部 API キー（使用するデータソースのキーのみ記載する）
# -------------------------------------------------------------------

# FRED API キー（セントルイス連銀）
# 取得先: https://fred.stlouisfed.org/docs/api/api_key.html
# FRED_API_KEY=your_fred_api_key_here

# e-Stat アプリID（政府統計の総合窓口）
# 取得先: https://www.e-stat.go.jp/api/
# ESTAT_APP_ID=your_estat_app_id_here
""")

    # ─── 3. .gitignore ───────────────────────────────────────────────
    write(target / ".gitignore", """\
# 機密情報（絶対にコミットしない）
.env

# Python
__pycache__/
*.py[cod]
.venv/
*.egg-info/

# テスト
.pytest_cache/
test-results/

# Streamlit
.streamlit/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# PyInstaller
build/
dist/
*.spec
""")

    # ─── 4. config.py ────────────────────────────────────────────────
    write(target / "config.py", """\
\"\"\"アプリ全体で共有する定数・マスターデータ。\"\"\"

from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------------------------
# API キー（.env から読み込む）
# -------------------------------------------------------------------
FRED_API_KEY:  str = os.getenv("FRED_API_KEY", "")
ESTAT_APP_ID:  str = os.getenv("ESTAT_APP_ID", "")

# -------------------------------------------------------------------
# 世界銀行（API キー不要）
# -------------------------------------------------------------------
WB_COUNTRIES: dict[str, str] = {
    "日本": "JP", "アメリカ": "US", "中国": "CN", "ドイツ": "DE",
    "インド": "IN", "イギリス": "GB", "フランス": "FR", "ブラジル": "BR",
    "カナダ": "CA", "韓国": "KR",
}

WB_EN_TO_JP: dict[str, str] = {
    "Japan": "日本", "United States": "アメリカ", "China": "中国",
    "Germany": "ドイツ", "India": "インド", "United Kingdom": "イギリス",
    "France": "フランス", "Brazil": "ブラジル", "Canada": "カナダ",
    "Korea, Rep.": "韓国",
}

WB_DEFAULTS: list[str] = ["日本", "アメリカ", "中国", "ドイツ", "インド"]
WB_INDICATOR: str = "NY.GDP.MKTP.CD"   # GDP（米ドル建て）

# -------------------------------------------------------------------
# カラーパレット
# -------------------------------------------------------------------
COLOR_PALETTE: list[str] = [
    "#e94560", "#0f3460", "#16c79a", "#f5a623",
    "#8b5cf6", "#06b6d4", "#f43f5e", "#10b981",
    "#6366f1", "#ec4899", "#14b8a6", "#f59e0b",
]
""")

    # ─── 5. app.py ───────────────────────────────────────────────────
    write(target / "app.py", f"""\
\"\"\"
{app_name}
{'=' * len(app_name)}
実行方法:
    uv run streamlit run app.py
\"\"\"

from __future__ import annotations

import sys
from pathlib import Path
import logging

import streamlit as st
from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    load_dotenv(Path(sys.executable).parent / ".env")
else:
    load_dotenv(Path(__file__).parent / ".env")

from logger_config import setup_logging            # noqa: E402
setup_logging()
logger = logging.getLogger("app")

from config import WB_COUNTRIES, WB_DEFAULTS       # noqa: E402
from data import fetch_wb_gdp                       # noqa: E402
from views import setup_page, render_sidebar        # noqa: E402
from views import render_wb_dashboard               # noqa: E402
from views.components import empty_tab_placeholder  # noqa: E402


def main() -> None:
    setup_page()

    st.title("📊 {app_name}")
    st.markdown("世界銀行のオープンデータを活用して各国の GDP を可視化・比較します。")

    inputs = render_sidebar()

    # ── データ取得 ──────────────────────────────────────────────────
    if inputs["wb_execute"]:
        if not inputs["wb_countries"]:
            st.toast("国を 1 つ以上選択してください。", icon="⚠️")
        else:
            codes = tuple(WB_COUNTRIES[n] for n in inputs["wb_countries"])
            try:
                with st.spinner("データを取得中..."):
                    st.session_state["wb_data"] = fetch_wb_gdp(codes, *inputs["wb_years"])
                st.toast("データを取得しました！", icon="✅")
            except RuntimeError as exc:
                logger.error(f"データ取得エラー: {{exc}}", exc_info=True)
                st.error(f"データ取得エラー: {{exc}}")
                st.session_state.pop("wb_data", None)


    # ── タブ ────────────────────────────────────────────────────────
    (tab_wb,) = st.tabs(["🌍 世界銀行 GDP"])

    with tab_wb:
        if "wb_data" in st.session_state:
            render_wb_dashboard(st.session_state["wb_data"])
        else:
            empty_tab_placeholder()


if __name__ == "__main__":
    main()
""")

    # ─── 5-2. launcher.py ─────────────────────────────────────────────
    write(target / "launcher.py", f"""\
\"\"\"
launcher.py – EXE 起動ラッパー（bootstrap.run 直接呼び出し版）
\"\"\"
import sys
import os
import time
import socket
import threading
import webbrowser
import logging

PORT = 8501
URL  = f"http://localhost:{{PORT}}"

logger = logging.getLogger("launcher")


def find_app_py() -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "app.py")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")


def wait_for_server(host: str = "localhost", port: int = PORT, timeout: float = 30.0):
    \"\"\"ポートが開くまで待機してからブラウザを開く\"\"\"
    logger.info(f"Port listener thread started. Waiting for {{host}}:{{port}}...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                logger.info(f"Server detected on port {{port}}. Triggering default browser to: {{URL}}")
                webbrowser.open(URL)
                return
        except OSError:
            time.sleep(0.3)
    logger.warning("Server startup check timed out. Attempting to open browser anyway.")
    webbrowser.open(URL)  # タイムアウトしても一応開く


if __name__ == "__main__":
    from logger_config import setup_logging
    setup_logging()
    
    logger.info("Starting execution of launcher...")
    app_path = find_app_py()
    logger.info(f"Resolved app.py path: {{app_path}}")

    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"

    threading.Thread(target=wait_for_server, daemon=True).start()

    logger.info("Starting Streamlit programmatic bootstrap run...")
    from streamlit.web import bootstrap
    flag_options = {{
        "server.port": PORT,
        "server.headless": True,
        "server.enableCORS": False,
        "server.enableXsrfProtection": False,
        "browser.gatherUsageStats": False,
        "global.developmentMode": False,
    }}
    bootstrap.load_config_options(flag_options)
    bootstrap.run(
        main_script_path=app_path,
        is_hello=False,
        args=[],
        flag_options=flag_options,
    )

# PyInstaller 静的解析用のダミーインポート
if False:
    import app
    import config
    import logger_config
    import data.worldbank
    import views.page_config
    import views.sidebar
    import views.components
    import views.dashboard
""")

    # ─── 5-3. build.bat ───────────────────────────────────────────────
    write(target / "build.bat", f"""\
@echo off
chcp 65001 > nul
echo ============================================
echo  {app_name} - PyInstaller Build Script
echo ============================================

echo [1/3] Cleaning previous build...
if exist build  rmdir /s /q build
if exist dist   rmdir /s /q dist

echo [2/3] Running PyInstaller...
uv run pyinstaller ^
  --name "{app_name}" ^
  --onedir ^
  --windowed ^
  --add-data "app.py;." ^
  --add-data "config.py;." ^
  --add-data "logger_config.py;." ^
  --add-data "data;data" ^
  --add-data "views;views" ^
  --add-data ".venv\\Lib\\site-packages\\streamlit;streamlit" ^
  --add-data ".venv\\Lib\\site-packages\\plotly;plotly" ^
  --hidden-import streamlit ^
  --hidden-import pandas ^
  --hidden-import requests ^
  --hidden-import plotly ^
  --hidden-import dotenv ^
  --hidden-import config ^
  --hidden-import logger_config ^
  --hidden-import data.worldbank ^
  --hidden-import views.page_config ^
  --hidden-import views.sidebar ^
  --hidden-import views.components ^
  --hidden-import views.dashboard ^
  --hidden-import streamlit.web.cli ^
  --hidden-import streamlit.runtime.scriptrunner ^
  --hidden-import streamlit.runtime.caching ^
  --collect-all streamlit ^
  --collect-all plotly ^
  launcher.py

echo [3/3] Done!
echo.
echo Output: dist\\{app_name}\\{app_name}.exe
echo.
pause
""")

    # ─── 6. data/ ────────────────────────────────────────────────────
    write(target / "data" / "__init__.py", """\
from .worldbank import fetch_wb_gdp

__all__ = ["fetch_wb_gdp"]
""")

    write(target / "data" / "worldbank.py", """\
\"\"\"世界銀行 API からのデータ取得。\"\"\"

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
import requests
import streamlit as st

from config import WB_EN_TO_JP, WB_INDICATOR

logger = logging.getLogger(__name__)


def _wb_get(url: str, params: dict[str, Any]) -> Any:
    \"\"\"World Bank API へ GET し JSON を返す。エラーは RuntimeError に変換する。\"\"\"
    logger.info(f"Fetching GDP data. URL: {url} with params: {params}")
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        err_msg = "世界銀行 API への接続に失敗しました。ネットワーク接続を確認してください。"
        logger.error(f"{err_msg} Details: {exc}", exc_info=True)
        raise RuntimeError(err_msg)
    except requests.exceptions.Timeout as exc:
        err_msg = "世界銀行 API からの応答がタイムアウトしました。"
        logger.error(f"{err_msg} Details: {exc}", exc_info=True)
        raise RuntimeError(err_msg)
    except requests.exceptions.HTTPError as exc:
        err_msg = f"世界銀行 API エラー: {exc}"
        logger.error(err_msg, exc_info=True)
        raise RuntimeError(err_msg)
    logger.info("Successfully fetched JSON from World Bank API")
    return resp.json()


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_wb_gdp(
    country_codes: tuple[str, ...],
    start: int,
    end: int,
) -> pd.DataFrame:
    \"\"\"世界銀行 API v2 から GDP データを取得する。

    Args:
        country_codes: ISO alpha-2 国コードのタプル（キャッシュのため list ではなく tuple）
        start: 開始年
        end: 終了年

    Returns:
        「国」「年」「GDP (USD)」列を持つ DataFrame
    \"\"\"
    url = (
        f"https://api.worldbank.org/v2/country/"
        f"{{';'.join(country_codes)}}/indicator/{{WB_INDICATOR}}"
    )
    data = _wb_get(url, {{"date": f"{{start}}:{{end}}", "format": "json", "per_page": 10000}})

    if not isinstance(data, list) or len(data) < 2 or data[1] is None:
        err_msg = "世界銀行 API からデータを取得できませんでした。"
        logger.error(err_msg)
        raise RuntimeError(err_msg)

    records = [
        {{
            "国": WB_EN_TO_JP.get(item["country"]["value"], item["country"]["value"]),
            "年": int(item["date"]),
            "GDP (USD)": float(item["value"]),
        }}
        for item in data[1]
        if item.get("value") is not None
    ]

    if not records:
        err_msg = "選択した条件に該当するデータが見つかりませんでした。"
        logger.error(err_msg)
        raise RuntimeError(err_msg)

    result = pd.DataFrame(records).sort_values(["国", "年"]).reset_index(drop=True)
    logger.info(f"Successfully loaded WB GDP data. Rows: {len(result)}")
    return result
""")

    # ─── 7. views/ ───────────────────────────────────────────────────
    write(target / "views" / "__init__.py", """\
from .page_config import setup_page
from .sidebar import render_sidebar
from .dashboard import render_wb_dashboard

__all__ = [
    "setup_page",
    "render_sidebar",
    "render_wb_dashboard",
]
""")

    write(target / "views" / "page_config.py", f"""\
\"\"\"ページ設定・グローバル CSS の適用。\"\"\"

from __future__ import annotations

import streamlit as st

_CSS = \"\"\"
<style>
/* サイドバー */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}}
[data-testid="stSidebar"] * {{ color: #e2e8f0 !important; }}

/* 実行ボタン */
[data-testid="stSidebar"] .stButton > button {{
    background: linear-gradient(135deg, #e94560 0%, #c23152 100%);
    color: #fff !important;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    transition: all 0.25s ease;
    box-shadow: 0 4px 14px rgba(233,69,96,0.35);
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 22px rgba(233,69,96,0.55);
}}

/* タブ */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: #f1f5f9;
    border-radius: 12px;
    padding: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px;
    padding: 0.55rem 1.6rem;
    font-weight: 600;
}}
.stTabs [aria-selected="true"] {{
    background: #fff !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.08);
}}
</style>
\"\"\"


def setup_page() -> None:
    \"\"\"ページの初期設定とカスタム CSS を適用する。\"\"\"
    st.set_page_config(
        page_title="{app_name}",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(_CSS, unsafe_allow_html=True)
""")

    write(target / "views" / "sidebar.py", """\
\"\"\"サイドバー UI の描画。\"\"\"

from __future__ import annotations

from typing import Any

import streamlit as st

from config import WB_COUNTRIES, WB_DEFAULTS


def render_sidebar() -> dict[str, Any]:
    \"\"\"サイドバーの UI を描画し、ユーザー入力をまとめて返す。\"\"\"
    with st.sidebar:
        st.markdown("## ⚙️ 設定")
        st.markdown("---")

        st.markdown("### 🌍 世界銀行 GDP")
        st.caption("GDP（米ドル建て）の国際比較")

        wb_countries: list[str] = st.multiselect(
            "比較する国を選択",
            options=list(WB_COUNTRIES.keys()),
            default=WB_DEFAULTS,
            key="wb_countries",
        )
        wb_years: tuple[int, int] = st.slider(
            "表示期間",
            min_value=1960,
            max_value=2023,
            value=(2000, 2023),
            key="wb_years",
        )
        wb_execute: bool = st.button(
            "🔍 データ取得", key="wb_exec", use_container_width=True
        )

        st.markdown("---")
        st.caption("データソース: World Bank API v2（API キー不要）")

    return {
        "wb_countries": wb_countries,
        "wb_years": wb_years,
        "wb_execute": wb_execute,
    }
""")

    write(target / "views" / "dashboard.py", """\
\"\"\"GDP ダッシュボードの描画。\"\"\"

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from config import COLOR_PALETTE
from views.components import data_table_with_download


def render_wb_dashboard(df: pd.DataFrame) -> None:
    \"\"\"世界銀行 GDP タブのメインコンテンツを描画する。

    Args:
        df: fetch_wb_gdp() で取得した DataFrame
    \"\"\"
    if df.empty:
        st.warning("データを取得できませんでした。国や期間の選択を確認してください。")
        return

    latest_year = int(df["年"].max())
    latest = df[df["年"] == latest_year].sort_values("GDP (USD)", ascending=False)

    st.markdown(f"#### 📊 主要指標（{latest_year}年）")
    cols = st.columns(min(len(latest), 5))
    for i, (_, row) in enumerate(latest.head(5).iterrows()):
        cols[i].metric(
            label=row["国"],
            value=f"${row['GDP (USD)'] / 1e12:,.2f} 兆",
        )

    st.markdown("---")

    fig = px.line(
        df,
        x="年",
        y="GDP (USD)",
        color="国",
        title="GDP 推移（米ドル建て）",
        labels={"GDP (USD)": "GDP（米ドル）", "年": "年"},
        color_discrete_sequence=COLOR_PALETTE,
        template="plotly_white",
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_tickformat=",.0f",
        height=520,
        margin=dict(t=60, b=40),
    )
    fig.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig, use_container_width=True)

    pivot = (
        df.pivot(index="年", columns="国", values="GDP (USD)")
        .sort_index(ascending=False)
    )
    formatted = pivot.copy()
    for col in formatted.columns:
        formatted[col] = formatted[col].apply(
            lambda x: f"${x / 1e9:,.1f} B" if pd.notna(x) else "-"
        )
    data_table_with_download(formatted, "gdp_data.csv")
""")

    write(target / "views" / "components.py", """\
\"\"\"再利用可能な UI コンポーネント。\"\"\"

from __future__ import annotations

import pandas as pd
import streamlit as st

PLACEHOLDER_INFO = (
    "👈 **サイドバー** で国と期間を選択し、\\n「🔍 データ取得」ボタンを押してください。"
)


def csv_download_button(
    df: pd.DataFrame,
    filename: str,
    label: str = "💾 CSV ダウンロード",
) -> None:
    \"\"\"DataFrame を UTF-8 BOM 付き CSV でダウンロードするボタンを表示する。\"\"\"
    csv_bytes = df.to_csv(index=True, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(label=label, data=csv_bytes, file_name=filename, mime="text/csv")


def data_table_with_download(
    df: pd.DataFrame,
    filename: str,
    expander_label: str = "📋 生データを表示",
    height: int = 400,
) -> None:
    \"\"\"エクスパンダー付きデータテーブルと CSV ダウンロードボタンを表示する。\"\"\"
    col_exp, col_dl = st.columns([4, 1])
    with col_exp:
        with st.expander(expander_label):
            st.dataframe(df, use_container_width=True, height=height)
    with col_dl:
        csv_download_button(df, filename)


def empty_tab_placeholder(message: str = PLACEHOLDER_INFO) -> None:
    \"\"\"データ未取得時のプレースホルダーを表示する。\"\"\"
    st.markdown("")
    st.info(message, icon="💡")
""")

    # ─── 8. tests/ ───────────────────────────────────────────────────
    write(target / "tests" / "__init__.py", "")
    write(target / "tests" / "e2e" / "__init__.py", "")

    write(target / "tests" / "test_imports.py", f"""\
\"\"\"モジュールのインポートが通ることを確認するスモークテスト。\"\"\"


def test_import_config():
    import config
    assert hasattr(config, "WB_COUNTRIES")
    assert hasattr(config, "COLOR_PALETTE")


def test_import_data():
    from data import fetch_wb_gdp
    assert callable(fetch_wb_gdp)


def test_import_views():
    from views import setup_page, render_sidebar, render_wb_dashboard
    assert callable(setup_page)
    assert callable(render_sidebar)
    assert callable(render_wb_dashboard)


def test_import_views_components():
    from views.components import empty_tab_placeholder, data_table_with_download
    assert callable(empty_tab_placeholder)
    assert callable(data_table_with_download)
""")

    touch(target / "tests" / "e2e" / "test_app.py")

    # ─── 9. .github/workflows/ci.yml ─────────────────────────────────
    write(target / ".github" / "workflows" / "ci.yml", """\
name: CI

on:
  push:
    branches: ["main", "master"]
  pull_request:
    branches: ["main", "master"]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          enable-cache: true

      - name: Install dependencies
        run: uv sync

      - name: Copy .env for testing
        run: cp .env.example .env

      - name: Run smoke tests (import check)
        run: uv run pytest tests/test_imports.py -v --tb=short
""")

    # ─── 10. docs/ ────────────────────────────────────────────────────
    guide_src = here / "docs" / "事例で学ぶWeb開発入門_Streamlit.md"
    copy_doc(guide_src, target / "docs" / "事例で学ぶWeb開発入門_Streamlit.md")

    for tmpl_name in ["テンプレート_01_要件定義.md", "テンプレート_02_仕様書.md",
                       "テンプレート_03_テスト仕様書.md", "テンプレート_04_報告書.md"]:
        tmpl_src = here / "docs" / tmpl_name
        dest_name = tmpl_name.replace("テンプレート_", "")
        copy_doc(tmpl_src, target / "docs" / dest_name)

    # ─── 11. AI 指示書 ────────────────────────────────────────────────
    inst_src = here / ".github" / "copilot-instructions.md"
    copy_doc(inst_src, target / ".github" / "copilot-instructions.md")

    ai_src = here / "AI_INSTRUCTIONS.md"
    copy_doc(ai_src, target / "AI_INSTRUCTIONS.md")

    # ─── 12. README.md ────────────────────────────────────────────────
    write(target / "README.md", f"""\
# {app_name}

（ダッシュボードの概要を 1〜2 文で記載）

---

## 必要な環境

| 項目 | 内容 |
| --- | --- |
| Python | 3.10 以上 |
| パッケージ管理 | [uv](https://docs.astral.sh/uv/) |
| 外部 API | 世界銀行（API キー不要） |

---

## セットアップ

```bash
# 1. 環境設定ファイルを作成
cp .env.example .env        # Mac/Linux
copy .env.example .env      # Windows

# 2. 依存パッケージをインストール
uv sync

# 3. アプリを起動
uv run streamlit run app.py
```

ブラウザで `http://localhost:8501/` が自動で開きます。

---

## EXE化 (実行ファイルの作成)

Windows 環境で、以下のバッチファイルを実行するとスタンドアロンの EXE（実行ファイル）を作成できます。

```bash
build.bat
```

ビルド完了後、`dist/{app_name}/{app_name}.exe` をダブルクリックするだけで、コンソールウィンドウなしで起動し、自動的にブラウザでダッシュボードが開きます。
※ 起動時に `.env` ファイルの情報を読み込むため、`dist/{app_name}/` フォルダの中に `.env` ファイルをコピーして配置してください。

---

## API キーが必要なデータソースを追加する場合

`.env` に API キーを記載してください。

```env
FRED_API_KEY=your_fred_api_key_here   # https://fred.stlouisfed.org/docs/api/api_key.html
ESTAT_APP_ID=your_estat_app_id_here   # https://www.e-stat.go.jp/api/
```

---

## テストの実行

```bash
# スモークテスト（インポート確認）
uv run pytest tests/test_imports.py -v

# E2E テスト（アプリ起動後に実行）
uv run playwright install chromium
uv run pytest tests/e2e/ -v
```

---

## プロジェクト構成

```text
{app_name}/
├── app.py           # エントリーポイント（st.set_page_config は必ずここで最初に呼ぶ）
├── launcher.py      # EXE 起動用ラッパー
├── build.bat        # EXE ビルド用バッチファイル
├── config.py        # 定数・APIキー・マスターデータ
├── data/            # 外部 API 呼び出し専用（st.* は書かない）
│   └── worldbank.py # 世界銀行 API（@st.cache_data 必須）
├── views/           # 描画専用（API 呼び出しは書かない）
│   ├── page_config.py
│   ├── sidebar.py
│   ├── dashboard.py
│   └── components.py
├── tests/
│   ├── test_imports.py  # スモークテスト
│   └── e2e/             # Playwright E2E テスト
└── docs/
    ├── 01_要件定義.md
    ├── 02_仕様書.md
    ├── 03_テスト仕様書.md
    ├── 04_報告書.md
    └── 事例で学ぶWeb開発入門_Streamlit.md
```

---

## 新しいデータソースの追加手順

1. `data/<source>.py` を作成（`@st.cache_data(ttl=...)` 必須）
2. `data/__init__.py` に追記
3. `views/<tab>.py` を作成（`df.empty` チェック必須）
4. `views/__init__.py` に追記
5. `app.py` のタブ一覧に追加
6. `docs/02_仕様書.md` を更新（Mermaid 図も更新）

---

## ドキュメント

| ファイル | 内容 |
| --- | --- |
| [01_要件定義.md](docs/01_要件定義.md) | 何を見せるか（目的・データソース・画面） |
| [02_仕様書.md](docs/02_仕様書.md) | どう作るか（データフロー・画面仕様・設定値） |
| [03_テスト仕様書.md](docs/03_テスト仕様書.md) | どう検証するか（E2E テスト設計） |
| [04_報告書.md](docs/04_報告書.md) | 結果（テスト結果・不具合・デプロイ依頼） |
| [Streamlit 開発入門](docs/事例で学ぶWeb開発入門_Streamlit.md) | バイブコーディング入門＋技術解説 |
""")

    # ─── 完了メッセージ ───────────────────────────────────────────────
    print(f"""
==========================================================
  テンプレートを作成しました
==========================================================

場所: {target}

生成ファイル:
  app.py / config.py / launcher.py / build.bat / logger_config.py
  data/worldbank.py
  views/page_config.py / sidebar.py / dashboard.py / components.py
  tests/test_imports.py / tests/e2e/
  docs/   (01_要件定義 ~ 04_報告書 + 開発入門)
  AI_INSTRUCTIONS.md / .github/copilot-instructions.md
  .github/workflows/ci.yml  <- GitHub Actions (自動テスト)

----------------------------------------------------------
ローカルで動かす
----------------------------------------------------------
  cd {target}
  copy .env.example .env       (Windows)
  cp .env.example .env         (Mac/Linux)
  uv sync
  uv run streamlit run app.py
  -> http://localhost:8501/

----------------------------------------------------------
EXE化する
----------------------------------------------------------
  cd {target}
  build.bat
  -> dist/{app_name}/{app_name}.exe が生成されます

テスト実行:
  uv run pytest tests/test_imports.py -v

----------------------------------------------------------
GitHub に登録する (テンプレートリポジトリとして公開)
----------------------------------------------------------
  cd {target}
  git init
  git add .
  git commit -m "chore: initial template from streamlit-gdp-dashboard"

  # GitHub CLI でリポジトリ作成 & プッシュ
  gh repo create {app_name} --public --source=. --remote=origin --push

  # テンプレートリポジトリに設定
  # (他の人が Use this template で使えるようになる)
  gh repo edit {app_name} --template

----------------------------------------------------------
新しいデータソースの追加 (AI への一言)
----------------------------------------------------------
  「AI_INSTRUCTIONS.md のルールに従って、
   data/fred.py に FRED API のデータ取得関数を追加して。
   views/fred_tab.py も作って app.py のタブに追加して」
==========================================================
""")


if __name__ == "__main__":
    main()
