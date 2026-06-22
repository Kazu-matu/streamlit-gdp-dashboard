"""日本経済指標ページ。"""
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
logger = logging.getLogger("page.japan")

from views.page_config import setup_page
from config import FRED_SERIES
from data import fetch_fred_series, fetch_estat_ci
from views.japan_tab import render_japan_dashboard
from views.components import empty_tab_placeholder

setup_page()

st.title("🇯🇵 日本経済指標")
st.markdown("FRED（セントルイス連銀）および e-Stat（内閣府）から日本の主要経済指標を取得・可視化します。")

with st.sidebar:
    st.markdown("## ⚙️ 設定")
    st.markdown("---")
    st.markdown("### 🇯🇵 日本経済指標")
    st.caption("鉱工業生産・失業率・CPI・景気動向指数")

    japan_years: tuple[int, int] = st.slider(
        "表示期間", min_value=1980, max_value=2026, value=(2000, 2026), key="japan_years",
    )
    execute = st.button("🔍 データ取得", key="japan_exec", use_container_width=True)

    st.markdown("---")
    st.caption("データソース: FRED / e-Stat（内閣府）")

if execute:
    start_str = f"{japan_years[0]}-01-01"
    end_str = f"{japan_years[1]}-12-31"
    fred_data = {}
    with st.spinner("日本経済指標（FRED）を取得中..."):
        for series_id in FRED_SERIES:
            try:
                fred_data[series_id] = fetch_fred_series(series_id, start_str, end_str)
            except RuntimeError as exc:
                logger.error(f"FRED データ取得エラー（{series_id}）: {exc}", exc_info=True)
                st.error(f"🇯🇵 FRED データ取得エラー（{series_id}）: {exc}")
    if fred_data:
        st.session_state["japan_fred"] = fred_data
    try:
        with st.spinner("景気動向指数（e-Stat）を取得中..."):
            st.session_state["japan_ci"] = fetch_estat_ci()
        st.toast("✅ 日本経済指標を取得しました！", icon="✅")
    except RuntimeError as exc:
        logger.error(f"e-Stat データ取得エラー: {exc}", exc_info=True)
        st.error(f"🇯🇵 e-Stat データ取得エラー: {exc}")
        st.session_state.pop("japan_ci", None)
    st.session_state["japan_year_range"] = japan_years

if "japan_fred" in st.session_state:
    render_japan_dashboard(
        st.session_state["japan_fred"],
        st.session_state.get("japan_ci"),
        st.session_state.get("japan_year_range", (2000, 2026)),
    )
else:
    empty_tab_placeholder("👈 **サイドバー** で期間を選択し、\n「🔍 データ取得」ボタンを押してください。")
