"""IMF GDP 成長率タブの描画。"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from config import COLOR_PALETTE, IMF_COUNTRIES
from views.components import data_table_with_download


def render_imf_dashboard(
    df: pd.DataFrame,
    selected_codes: list[str],
    year_range: tuple[int, int],
) -> None:
    """IMF GDP 成長率タブのメインコンテンツを描画する。

    Args:
        df: fetch_imf_gdp_growth() で取得した DataFrame。
        selected_codes: 表示する国コードのリスト。
        year_range: 表示期間 (開始年, 終了年)。
    """
    available = [c for c in selected_codes if c in df.index]
    if not available:
        st.warning("選択した国のデータが見つかりませんでした。")
        return

    year_cols = [c for c in df.columns if year_range[0] <= c <= year_range[1]]
    if not year_cols:
        st.warning("選択した期間のデータが見つかりませんでした。")
        return

    filtered = df.loc[available, year_cols]
    latest_year = max(year_cols)

    st.markdown(f"#### 📊 主要指標（{latest_year}年）")
    cols = st.columns(min(len(available), 5))
    for i, code in enumerate(available[:5]):
        val = filtered.loc[code, latest_year]
        name = IMF_COUNTRIES.get(code, code)
        cols[i].metric(label=name, value=f"{val:+.2f} %" if pd.notna(val) else "N/A")

    st.markdown("---")

    plot_df = (
        filtered.T.reset_index()
        .rename(columns={"index": "年"})
        .melt(id_vars="年", var_name="国コード", value_name="成長率 (%)")
    )
    plot_df["国"] = plot_df["国コード"].map(IMF_COUNTRIES).fillna(plot_df["国コード"])

    fig = px.line(
        plot_df,
        x="年", y="成長率 (%)", color="国",
        title="実質 GDP 成長率の推移",
        labels={"成長率 (%)": "成長率 (%)", "年": "年"},
        color_discrete_sequence=COLOR_PALETTE,
        template="plotly_white",
    )
    fig.add_hline(
        y=0, line_dash="dash", line_color="#9ca3af", opacity=0.6,
        annotation_text="0%", annotation_position="bottom right",
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=520,
        margin=dict(t=60, b=40),
    )
    fig.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig, use_container_width=True)

    export = filtered.copy()
    export.index = export.index.map(lambda x: f"{IMF_COUNTRIES.get(x, x)}（{x}）")
    formatted = export.T.sort_index(ascending=False).copy()
    for col in formatted.columns:
        formatted[col] = formatted[col].apply(lambda x: f"{x:+.2f} %" if pd.notna(x) else "—")

    data_table_with_download(formatted, "imf_gdp_growth.csv")
