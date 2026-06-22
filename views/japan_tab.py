"""日本経済指標タブの描画。"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from config import FRED_SERIES
from views.components import csv_download_button, data_table_with_download


def _render_ci_section(ci_df: pd.DataFrame, start_ts: pd.Timestamp, end_ts: pd.Timestamp) -> None:
    """景気動向指数（先行CI・一致CI）セクションを描画する。"""
    filtered = ci_df[(ci_df["日付"] >= start_ts) & (ci_df["日付"] <= end_ts)]
    if filtered.empty:
        return

    st.markdown("#### 📈 景気動向指数（内閣府）")

    latest_date = filtered["日付"].max()
    cols = st.columns(2)
    for i, label in enumerate(["先行CI", "一致CI"]):
        subset = filtered[filtered["指標"] == label]
        if subset.empty:
            continue
        vals = subset[subset["日付"] == latest_date]["値"].values
        cols[i].metric(
            label=f"{label}（{latest_date.strftime('%Y年%m月')}）",
            value=f"{vals[0]:.1f}" if len(vals) else "N/A",
        )

    fig = px.line(
        filtered, x="日付", y="値", color="指標",
        title="景気動向指数（先行CI・一致CI）",
        color_discrete_sequence=["#e94560", "#0f3460"],
        template="plotly_white",
    )
    fig.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=420,
        margin=dict(t=60, b=40),
    )
    fig.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig, use_container_width=True)

    export = filtered.copy()
    export["日付"] = export["日付"].dt.strftime("%Y-%m")
    export = export.sort_values("日付", ascending=False).set_index("日付")
    data_table_with_download(export, "japan_ci.csv", height=300)
    st.markdown("---")


def _render_fred_metric(
    series_id: str,
    df: pd.DataFrame,
    start_ts: pd.Timestamp,
    end_ts: pd.Timestamp,
) -> None:
    """FRED の1指標セクションを描画する。"""
    filtered = df[(df["日付"] >= start_ts) & (df["日付"] <= end_ts)]
    if filtered.empty:
        return

    meta = FRED_SERIES[series_id]
    label, unit = meta["label"], meta["unit"]

    st.markdown(f"#### 📊 {label}")
    latest = filtered.iloc[-1]
    st.metric(
        label=f"最新値（{latest['日付'].strftime('%Y年%m月')}）",
        value=f"{latest['値']:.2f} {unit}",
    )

    fig = px.line(
        filtered, x="日付", y="値",
        title=f"{label} 推移",
        labels={"値": f"{label}（{unit}）", "日付": "日付"},
        color_discrete_sequence=["#16c79a"],
        template="plotly_white",
    )
    fig.update_layout(hovermode="x unified", height=380, margin=dict(t=60, b=40))
    fig.update_traces(line=dict(width=2.5))
    st.plotly_chart(fig, use_container_width=True)

    export = filtered[["日付", "値"]].copy()
    export["日付"] = export["日付"].dt.strftime("%Y-%m")
    export = export.sort_values("日付", ascending=False).set_index("日付")
    export.columns = [label]
    data_table_with_download(export, f"japan_{series_id.lower()}.csv", height=300)
    st.markdown("---")


def render_japan_dashboard(
    fred_data: dict[str, pd.DataFrame],
    ci_df: pd.DataFrame | None,
    year_range: tuple[int, int],
) -> None:
    """日本経済指標タブのメインコンテンツを描画する。

    Args:
        fred_data: シリーズIDをキー、DataFrameを値とする辞書。
        ci_df: fetch_estat_ci() で取得した景気動向指数 DataFrame（None なら非表示）。
        year_range: 表示期間 (開始年, 終了年)。
    """
    start_ts = pd.Timestamp(year=year_range[0], month=1, day=1)
    end_ts = pd.Timestamp(year=year_range[1], month=12, day=31)

    if ci_df is not None and not ci_df.empty:
        _render_ci_section(ci_df, start_ts, end_ts)

    for series_id, df in fred_data.items():
        if df is not None and not df.empty:
            _render_fred_metric(series_id, df, start_ts, end_ts)
