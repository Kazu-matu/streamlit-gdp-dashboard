"""
data/local_sqlite.py — ローカルの SQLite データベースからデータを読み込むモジュール。
"""
from __future__ import annotations
import sqlite3
import pandas as pd
import streamlit as st

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_local_sqlite(dbpath: str) -> pd.DataFrame:
    """ローカルの SQLite データベースから GDP データを取得して DataFrame に変換する。

    Args:
        dbpath: 接続する SQLite データベースファイルへのパス。

    Returns:
        「国」「年」「GDP (USD)」列を持つ DataFrame。
    """
    conn = sqlite3.connect(dbpath)
    try:
        # クエリ実行（sqlite3 + pandas）
        df = pd.read_sql_query("SELECT country, year, gdp_usd FROM gdp_data", conn)
    finally:
        conn.close()
        
    # カラム名のマッピング（多言語や大文字小文字の揺らぎに対応）
    rename_map = {
        "country": "国",
        "year": "年",
        "gdp_usd": "GDP (USD)",
    }
    df = df.rename(columns=rename_map)
    # 必要なカラムの存在チェック
    required = ["国", "年", "GDP (USD)"]
    for col in required:
        if col not in df.columns:
            raise KeyError(f"SQLiteデータベースに必要なカラム '{col}' が存在しません。")
            
    return df[required].sort_values(["国", "年"]).reset_index(drop=True)
