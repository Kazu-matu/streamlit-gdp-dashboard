"""世界銀行 GDP ページ。"""
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
logger = logging.getLogger("page.worldbank")

from views.page_config import setup_page
from config import WB_COUNTRIES, WB_DEFAULTS
from data import fetch_wb_gdp
from views.worldbank_tab import render_wb_dashboard
from views.components import empty_tab_placeholder

setup_page()

st.title("🌍 世界銀行 — GDP（米ドル建て）")
st.markdown("World Bank API v2 から各国の GDP（米ドル建て）を取得し、国際比較します。")

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
        "表示期間", min_value=1960, max_value=2023, value=(2000, 2023), key="wb_years",
    )
    execute = st.button("🔍 データ取得", key="wb_exec", use_container_width=True)

    st.markdown("---")
    st.caption("データソース: World Bank API v2")

if execute:
    if not wb_countries:
        st.toast("⚠️ 国を1つ以上選択してください。", icon="⚠️")
    else:
        codes = tuple(WB_COUNTRIES[n] for n in wb_countries)
        try:
            with st.spinner("世界銀行データを取得中..."):
                st.session_state["wb_data"] = fetch_wb_gdp(codes, *wb_years)
            st.toast("✅ 世界銀行データを取得しました！", icon="✅")
        except RuntimeError as exc:
            logger.error(f"世界銀行データ取得エラー: {exc}", exc_info=True)
            st.error(f"🌍 世界銀行データ取得エラー: {exc}")
            st.session_state.pop("wb_data", None)

if "wb_data" in st.session_state:
    render_wb_dashboard(st.session_state["wb_data"])
else:
    empty_tab_placeholder()
