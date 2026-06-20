"""
各国GDP比較ダッシュボード
=========================
実行方法:
    uv run streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    load_dotenv(Path(sys.executable).parent / ".env")
else:
    load_dotenv(Path(__file__).parent / ".env")

from config import IMF_DEFAULTS, FRED_SERIES  # noqa: E402
from data import (  # noqa: E402
    fetch_wb_gdp,
    fetch_imf_gdp_growth,
    fetch_fred_series,
    fetch_estat_ci,
    fetch_local_csv,
    fetch_local_excel,
    fetch_local_sqlite,
)
from views import (  # noqa: E402
    setup_page,
    render_sidebar,
    render_wb_dashboard,
    render_imf_dashboard,
    render_japan_dashboard,
    render_local_csv,
    render_local_excel,
    render_local_sqlite,
)
from views.components import empty_tab_placeholder  # noqa: E402



def main() -> None:
    setup_page()

    st.title("📊 各国 GDP 比較ダッシュボード")
    st.markdown("世界銀行と IMF のオープンデータを活用し、各国の GDP および経済成長率を可視化・比較します。")

    inputs = render_sidebar()

    # ── 世界銀行 ──
    if inputs["wb_execute"]:
        if not inputs["wb_countries"]:
            st.toast("⚠️ 世界銀行: 国を1つ以上選択してください。", icon="⚠️")
        else:
            from config import WB_COUNTRIES
            codes = tuple(WB_COUNTRIES[n] for n in inputs["wb_countries"])
            try:
                with st.spinner("世界銀行データを取得中..."):
                    st.session_state["wb_data"] = fetch_wb_gdp(codes, *inputs["wb_years"])
                st.toast("✅ 世界銀行データを取得しました！", icon="✅")
            except RuntimeError as exc:
                st.error(f"🌍 世界銀行データ取得エラー: {exc}")
                st.session_state.pop("wb_data", None)

    # ── IMF ──
    if inputs["imf_execute"]:
        if not inputs["imf_countries"]:
            st.toast("⚠️ IMF: 国を1つ以上選択してください。", icon="⚠️")
        else:
            try:
                with st.spinner("IMF データを取得中..."):
                    st.session_state["imf_data"] = fetch_imf_gdp_growth(
                        tuple(inputs["imf_countries"]), *inputs["imf_years"]
                    )
                st.session_state["imf_selected"] = inputs["imf_countries"]
                st.session_state["imf_year_range"] = inputs["imf_years"]
                st.toast("✅ IMF データを取得しました！", icon="✅")
            except RuntimeError as exc:
                st.error(f"📈 IMF データ取得エラー: {exc}")
                st.session_state.pop("imf_data", None)

    # ── 日本経済指標 ──
    if inputs["japan_execute"]:
        start_str = f"{inputs['japan_years'][0]}-01-01"
        end_str = f"{inputs['japan_years'][1]}-12-31"
        fred_data = {}
        with st.spinner("日本経済指標（FRED）を取得中..."):
            for series_id in FRED_SERIES:
                try:
                    fred_data[series_id] = fetch_fred_series(series_id, start_str, end_str)
                except RuntimeError as exc:
                    st.error(f"🇯🇵 FRED データ取得エラー（{series_id}）: {exc}")
        if fred_data:
            st.session_state["japan_fred"] = fred_data
        try:
            with st.spinner("景気動向指数（e-Stat）を取得中..."):
                st.session_state["japan_ci"] = fetch_estat_ci()
            st.toast("✅ 日本経済指標を取得しました！", icon="✅")
        except RuntimeError as exc:
            st.error(f"🇯🇵 e-Stat データ取得エラー: {exc}")
            st.session_state.pop("japan_ci", None)
        st.session_state["japan_year_range"] = inputs["japan_years"]

    # ── ローカルデータ ──
    base_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
    csv_path = base_dir / "data" / "dummy" / "gdp_data.csv"
    excel_path = base_dir / "data" / "dummy" / "gdp_data.xlsx"
    sqlite_path = base_dir / "data" / "dummy" / "gdp_data.sqlite"

    if inputs["local_execute"]:
        try:
            with st.spinner("ローカルデータ（CSV/Excel/SQLite）を読み込み中..."):
                # もしファイルが存在しなければ自動生成
                if not (csv_path.exists() and excel_path.exists() and sqlite_path.exists()):
                    from generate_dummy_data import generate_dummy_data
                    generate_dummy_data(base_dir)
                
                st.session_state["local_csv_raw"] = fetch_local_csv(str(csv_path))
                st.session_state["local_excel_raw"] = fetch_local_excel(str(excel_path))
                st.session_state["local_sqlite_raw"] = fetch_local_sqlite(str(sqlite_path))
            st.toast("✅ ローカルデータを読み込みました！", icon="✅")
        except Exception as exc:
            st.error(f"📁 ローカルデータ読込エラー: {exc}")

    # ローカルデータ フィルタリング処理
    for key in ["csv", "excel", "sqlite"]:
        raw_key = f"local_{key}_raw"
        filtered_key = f"local_{key}_filtered"
        if raw_key in st.session_state:
            df = st.session_state[raw_key]
            st.session_state[filtered_key] = df[
                (df["年"] >= inputs["local_years"][0]) & (df["年"] <= inputs["local_years"][1])
            ]

    # ── タブ ──
    tab_wb, tab_imf, tab_japan, tab_csv, tab_sqlite, tab_excel = st.tabs([
        "🌍 世界銀行 — GDP（米ドル建て）",
        "📈 IMF — 実質 GDP 成長率",
        "🇯🇵 日本経済指標",
        "📁 CSVデータ (ローカル)",
        "🗄️ SQLiteデータ (ローカル)",
        "📊 Excelデータ (ローカル)",
    ])

    with tab_wb:
        if "wb_data" in st.session_state:
            render_wb_dashboard(st.session_state["wb_data"])
        else:
            empty_tab_placeholder()

    with tab_imf:
        if "imf_data" in st.session_state:
            render_imf_dashboard(
                st.session_state["imf_data"],
                st.session_state.get("imf_selected", IMF_DEFAULTS),
                st.session_state.get("imf_year_range", (2000, 2024)),
            )
        else:
            empty_tab_placeholder()

    with tab_japan:
        if "japan_fred" in st.session_state:
            render_japan_dashboard(
                st.session_state["japan_fred"],
                st.session_state.get("japan_ci"),
                st.session_state.get("japan_year_range", (2000, 2026)),
            )
        else:
            empty_tab_placeholder("👈 **サイドバー** で期間を選択し、\n「🔍 データ取得」ボタンを押してください。")

    with tab_csv:
        if "local_csv_filtered" in st.session_state:
            render_local_csv(st.session_state["local_csv_filtered"])
        else:
            empty_tab_placeholder("👈 **サイドバー** で「🔌 ローカルデータ読込」ボタンを押してください。")

    with tab_sqlite:
        if "local_sqlite_filtered" in st.session_state:
            render_local_sqlite(st.session_state["local_sqlite_filtered"])
        else:
            empty_tab_placeholder("👈 **サイドバー** で「🔌 ローカルデータ読込」ボタンを押してください。")

    with tab_excel:
        if "local_excel_filtered" in st.session_state:
            render_local_excel(st.session_state["local_excel_filtered"])
        else:
            empty_tab_placeholder("👈 **サイドバー** で「🔌 ローカルデータ読込」ボタンを押してください。")



if __name__ == "__main__":
    main()
