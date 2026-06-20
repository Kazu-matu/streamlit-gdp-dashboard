"""
views/local_sqlite_tab.py — ローカル SQLite データの可視化ビュー。
"""
from __future__ import annotations
import pandas as pd
import plotly.express as px
import streamlit as st
from config import COLOR_PALETTE
from views.components import data_table_with_download

def render_local_sqlite(df: pd.DataFrame) -> None:
    """SQLiteデータダッシュボードを描画する。

    Args:
        df: カラム名「国」「年」「GDP (USD)」を持つ DataFrame。
    """
    if df.empty:
        st.warning("表示期間に該当するデータがありません。")
        return

    latest_year = int(df["年"].max())
    latest = df[df["年"] == latest_year].sort_values("GDP (USD)", ascending=False)

    st.markdown(f"#### 📊 SQLite 主要指標（{latest_year}年）")
    cols = st.columns(min(len(latest), 5))
    for i, (_, row) in enumerate(latest.head(5).iterrows()):
        cols[i].metric(label=row["国"], value=f"${row['GDP (USD)'] / 1e12:,.2f} 兆")

    st.markdown("---")

    # SQLite は棒グラフ (Bar Chart) で可視化
    fig = px.bar(
        df,
        x="年", y="GDP (USD)", color="国",
        barmode="group",
        title="ローカル SQLite データ GDP 推移 (グループ棒グラフ)",
        labels={"GDP (USD)": "GDP (USD)", "年": "年"},
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
    st.plotly_chart(fig, use_container_width=True)

    # 生データ表示用のピボットテーブル
    pivot = df.pivot(index="年", columns="国", values="GDP (USD)").sort_index(ascending=False)
    formatted = pivot.copy()
    for col in formatted.columns:
        formatted[col] = formatted[col].apply(lambda x: f"${x / 1e9:,.1f} B" if pd.notna(x) else "—")

    data_table_with_download(formatted, "local_sqlite_gdp.csv")
