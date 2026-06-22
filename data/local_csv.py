"""
data/local_csv.py — ローカルの CSV ファイルからデータを読み込むモジュール。
"""
from __future__ import annotations
import logging
import pandas as pd
import streamlit as st

logger = logging.getLogger(__name__)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_local_csv(filepath: str) -> pd.DataFrame:
    """ローカルの CSV ファイルから GDP データを取得して DataFrame に変換する。

    Args:
        filepath: 読み込む CSV ファイル의 パス。

    Returns:
        「国」「年」「GDP (USD)」列を持つ DataFrame。
    """
    logger.info(f"Loading local CSV file from: {filepath}")
    try:
        df = pd.read_csv(filepath)
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
                raise KeyError(f"CSVファイルに必要なカラム '{col}' が存在しません。")
                
        result = df[required].sort_values(["国", "年"]).reset_index(drop=True)
        logger.info(f"Successfully loaded CSV data. Rows: {len(result)}")
        return result
    except Exception as exc:
        logger.error(f"Error loading CSV file '{filepath}': {exc}", exc_info=True)
        raise

