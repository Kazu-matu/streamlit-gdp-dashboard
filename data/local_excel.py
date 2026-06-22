"""
data/local_excel.py — ローカルの Excel ファイルからデータを読み込むモジュール。
"""
from __future__ import annotations
import logging
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_local_excel(filepath: str) -> pd.DataFrame:
    """ローカルの Excel ファイルから GDP データを取得して DataFrame に変換する。

    Args:
        filepath: 読み込む Excel ファイルのパス。

    Returns:
        「国」「年」「GDP (USD)」列を持つ DataFrame。
    """
    logger.info(f"Loading local Excel file from: {filepath}")
    try:
        # openpyxl を利用して読み込む
        df = pd.read_excel(filepath, sheet_name="GDP Data")
        # カラム名のマッピング（多言語や大文字小文字の揺らぎに対応）
        rename_map = {
            "Country": "国",
            "Year": "年",
            "GDP (USD)": "GDP (USD)",
            "country": "国",
            "year": "年",
            "gdp_usd": "GDP (USD)",
        }
        df = df.rename(columns=rename_map)
        # 必要なカラムの存在チェック
        required = ["国", "年", "GDP (USD)"]
        for col in required:
            if col not in df.columns:
                raise KeyError(f"Excelファイルに必要なカラム '{col}' が存在しません。")
                
        result = df[required].sort_values(["国", "年"]).reset_index(drop=True)
        logger.info(f"Successfully loaded Excel data. Rows: {len(result)}")
        return result
    except Exception as exc:
        logger.error(f"Error loading Excel file '{filepath}': {exc}", exc_info=True)
        raise

