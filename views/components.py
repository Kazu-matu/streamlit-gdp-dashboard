"""再利用可能な UI コンポーネント。"""

from __future__ import annotations

import pandas as pd
import streamlit as st

PLACEHOLDER_INFO = (
    "👈 **サイドバー** で国と期間を選択し、\n「🔍 データ取得」ボタンを押してください。"
)


def csv_download_button(
    df: pd.DataFrame,
    filename: str,
    label: str = "💾 CSVダウンロード",
) -> None:
    """DataFrame を UTF-8 BOM 付き CSV でダウンロードするボタンを表示する。

    BOM 付きにすることで Excel での文字化けを防ぐ。
    """
    csv_bytes = df.to_csv(index=True, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(label=label, data=csv_bytes, file_name=filename, mime="text/csv")


def data_table_with_download(
    df: pd.DataFrame,
    filename: str,
    expander_label: str = "📋 生データを表示",
    height: int = 400,
) -> None:
    """エクスパンダー付きデータテーブルとCSVダウンロードボタンを横並びで表示する。"""
    col_exp, col_dl = st.columns([4, 1])
    with col_exp:
        with st.expander(expander_label):
            st.dataframe(df, use_container_width=True, height=height)
    with col_dl:
        csv_download_button(df, filename)


def empty_tab_placeholder(message: str = PLACEHOLDER_INFO) -> None:
    """データ未取得時のプレースホルダーを表示する。"""
    st.markdown("")
    st.info(message, icon="💡")
