"""IMF GDP 成長率ページ。"""
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
logger = logging.getLogger("page.imf")

from views.page_config import setup_page
from config import IMF_COUNTRIES, IMF_DEFAULTS
from data import fetch_imf_gdp_growth
from views.imf_tab import render_imf_dashboard
from views.components import empty_tab_placeholder

setup_page()

st.title("📈 IMF — 実質 GDP 成長率")
st.markdown("World Bank API v2 から実質 GDP 成長率を取得し、各国の経済成長を比較します。")

with st.sidebar:
    st.markdown("## ⚙️ 設定")
    st.markdown("---")
    st.markdown("### 📈 IMF GDP 成長率")
    st.caption("実質 GDP 成長率の国際比較")

    imf_countries: list[str] = st.multiselect(
        "比較する国を選択",
        options=list(IMF_COUNTRIES.keys()),
        default=IMF_DEFAULTS,
        key="imf_countries",
        format_func=lambda x: f"{IMF_COUNTRIES.get(x, x)}（{x}）",
    )
    imf_years: tuple[int, int] = st.slider(
        "表示期間", min_value=1980, max_value=2029, value=(2000, 2029), key="imf_years",
    )
    execute = st.button("🔍 データ取得", key="imf_exec", use_container_width=True)

    st.markdown("---")
    st.caption("データソース: World Bank API v2（成長率指標）")

if execute:
    if not imf_countries:
        st.toast("⚠️ 国を1つ以上選択してください。", icon="⚠️")
    else:
        try:
            with st.spinner("IMF データを取得中..."):
                st.session_state["imf_data"] = fetch_imf_gdp_growth(
                    tuple(imf_countries), *imf_years
                )
            st.session_state["imf_selected"] = imf_countries
            st.session_state["imf_year_range"] = imf_years
            st.toast("✅ IMF データを取得しました！", icon="✅")
        except RuntimeError as exc:
            logger.error(f"IMF データ取得エラー: {exc}", exc_info=True)
            st.error(f"📈 IMF データ取得エラー: {exc}")
            st.session_state.pop("imf_data", None)

if "imf_data" in st.session_state:
    render_imf_dashboard(
        st.session_state["imf_data"],
        st.session_state.get("imf_selected", IMF_DEFAULTS),
        st.session_state.get("imf_year_range", (2000, 2029)),
    )
else:
    empty_tab_placeholder()
