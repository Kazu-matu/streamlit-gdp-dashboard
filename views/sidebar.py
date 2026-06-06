"""サイドバー UI の描画。"""

from __future__ import annotations

from typing import Any

import streamlit as st

from config import IMF_COUNTRIES, IMF_DEFAULTS, WB_COUNTRIES, WB_DEFAULTS


def render_sidebar() -> dict[str, Any]:
    """サイドバーの UI を描画し、ユーザー入力をまとめて返す。

    Returns:
        各ウィジェットの値を格納した辞書。
    """
    with st.sidebar:
        st.markdown("## ⚙️ ダッシュボード設定")
        st.markdown("---")

        st.markdown("### 🌍 世界銀行 GDP")
        st.caption("GDP（米ドル建て）の国際比較")
        wb_countries: list[str] = st.multiselect(
            "比較する国を選択", options=list(WB_COUNTRIES.keys()),
            default=WB_DEFAULTS, key="wb_countries",
        )
        wb_years: tuple[int, int] = st.slider(
            "表示期間", min_value=1960, max_value=2023, value=(2000, 2023), key="wb_years",
        )
        wb_execute: bool = st.button("🔍 データ取得", key="wb_exec", use_container_width=True)

        st.markdown("---")

        st.markdown("### 📈 IMF GDP 成長率")
        st.caption("実質 GDP 成長率の国際比較")
        imf_countries: list[str] = st.multiselect(
            "比較する国を選択", options=list(IMF_COUNTRIES.keys()),
            default=IMF_DEFAULTS, key="imf_countries",
            format_func=lambda x: f"{IMF_COUNTRIES.get(x, x)}（{x}）",
        )
        imf_years: tuple[int, int] = st.slider(
            "表示期間", min_value=1980, max_value=2029, value=(2000, 2029), key="imf_years",
        )
        imf_execute: bool = st.button("🔍 データ取得", key="imf_exec", use_container_width=True)

        st.markdown("---")

        st.markdown("### 🇯🇵 日本経済指標")
        st.caption("鉱工業生産・失業率・CPI・景気動向指数")
        japan_years: tuple[int, int] = st.slider(
            "表示期間", min_value=1980, max_value=2026, value=(2000, 2026), key="japan_years",
        )
        japan_execute: bool = st.button("🔍 データ取得", key="japan_exec", use_container_width=True)

        st.markdown("---")
        st.caption("データソース: World Bank API v2 / FRED / e-Stat")

    return {
        "wb_countries": wb_countries,
        "wb_years": wb_years,
        "wb_execute": wb_execute,
        "imf_countries": imf_countries,
        "imf_years": imf_years,
        "imf_execute": imf_execute,
        "japan_years": japan_years,
        "japan_execute": japan_execute,
    }
