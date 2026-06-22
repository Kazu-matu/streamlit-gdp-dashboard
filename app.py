"""
各国GDP比較ダッシュボード — ホームページ
=========================================
実行方法:
    uv run streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    load_dotenv(Path(sys.executable).parent / ".env")
else:
    load_dotenv(Path(__file__).parent / ".env")

from logger_config import setup_logging
setup_logging()

import streamlit as st
from views.page_config import setup_page

setup_page()

st.title("📊 各国 GDP 比較ダッシュボード")
st.markdown("世界銀行と IMF のオープンデータを活用し、各国の GDP および経済成長率を可視化・比較します。")

st.markdown("---")

st.markdown("## 📋 ページ一覧")

pages = [
    ("🌍 世界銀行", "World Bank API v2", "GDP（米ドル建て）の国際比較"),
    ("📈 IMF", "World Bank API v2（成長率）", "実質 GDP 成長率の国際比較"),
    ("🇯🇵 日本経済指標", "FRED / e-Stat", "鉱工業生産・失業率・CPI・景気動向指数"),
    ("📁 CSV", "ローカルファイル", "ダミー GDP データ（CSV）"),
    ("🗄️ SQLite", "ローカルファイル", "ダミー GDP データ（SQLite）"),
    ("📊 Excel", "ローカルファイル", "ダミー GDP データ（Excel）"),
]

cols = st.columns(3)
for i, (page, source, desc) in enumerate(pages):
    with cols[i % 3]:
        st.info(f"**{page}**\n\n{desc}\n\n*データソース: {source}*")

st.markdown("---")

st.markdown(
    """
## 対象国（世界銀行・IMF）

日本・アメリカ・中国・ドイツ・インド・イギリス・フランス・ブラジル・カナダ・韓国 ほか **16 カ国**

## 使い方

1. 左サイドバーのナビゲーションから表示したいページを選択
2. 各ページのサイドバーで国・期間を設定し「データ取得」ボタンを押す
3. グラフや表でデータを確認・CSV ダウンロード

## 技術スタック

Python 3.10+ / Streamlit 1.40+ / Plotly 5.20+ / pandas 2.0+ / uv
"""
)
