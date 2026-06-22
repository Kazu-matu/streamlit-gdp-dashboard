"""CSV ローカルデータページ。"""
from __future__ import annotations
import sys
from pathlib import Path
import logging

import streamlit as st
from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    load_dotenv(Path(sys.executable).parent / ".env")
else:
    load_dotenv(Path(__file__).parent.parent / ".env")

from logger_config import setup_logging
setup_logging()
logger = logging.getLogger("page.csv")

from views.page_config import setup_page
from data import fetch_local_csv
from views.local_csv_tab import render_local_csv
from views.components import empty_tab_placeholder

setup_page()

base_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent.parent
csv_path = base_dir / "data" / "dummy" / "gdp_data.csv"

st.title("📁 CSV データ")
st.markdown("ローカル CSV ファイルからダミー GDP データを読み込み、表示します。")

with st.sidebar:
    st.markdown("## ⚙️ 設定")
    st.markdown("---")
    st.markdown("### 📁 CSV データ")
    st.caption("ローカル CSV ファイルから読み込み")

    local_years: tuple[int, int] = st.slider(
        "表示期間", min_value=2010, max_value=2025, value=(2010, 2025), key="local_years",
    )
    execute = st.button("🔌 データ読込", key="csv_exec", use_container_width=True)

    st.markdown("---")
    st.caption(f"ファイル: `{csv_path.name}`")

if execute:
    try:
        with st.spinner("CSV データを読み込み中..."):
            if not csv_path.exists():
                from generate_dummy_data import generate_dummy_data
                generate_dummy_data(base_dir)
            st.session_state["local_csv_raw"] = fetch_local_csv(str(csv_path))
        st.toast("✅ CSV データを読み込みました！", icon="✅")
    except Exception as exc:
        logger.error(f"CSV 読込エラー: {exc}", exc_info=True)
        st.error(f"📁 CSV 読込エラー: {exc}")

if "local_csv_raw" in st.session_state:
    df = st.session_state["local_csv_raw"]
    filtered = df[(df["年"] >= local_years[0]) & (df["年"] <= local_years[1])]
    render_local_csv(filtered)
else:
    empty_tab_placeholder("👈 **サイドバー** で「🔌 データ読込」ボタンを押してください。")
