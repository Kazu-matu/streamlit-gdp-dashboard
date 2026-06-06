"""ページ設定・グローバル CSS の適用。"""

from __future__ import annotations

import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

html, body, [class*="st-"] { font-family: 'Noto Sans JP', sans-serif; }

/* ── サイドバー ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }

/* ── 実行ボタン ── */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #e94560 0%, #c23152 100%);
    color: #fff !important;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.02em;
    transition: all 0.25s ease;
    box-shadow: 0 4px 14px rgba(233,69,96,0.35);
}
[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 22px rgba(233,69,96,0.55);
}
[data-testid="stSidebar"] .stButton > button:active { transform: translateY(0); }

/* ── メトリクスカード ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    border-left: 5px solid #e94560;
}
[data-testid="stMetricValue"] { font-weight: 700; }

/* ── タブ ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #f1f5f9;
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 0.55rem 1.6rem;
    font-weight: 600;
    font-size: 0.92rem;
}
.stTabs [aria-selected="true"] {
    background: #fff !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.08);
}

/* ── タイトル ── */
h1 {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 800 !important;
    letter-spacing: -0.02em;
}

/* ── info / warning ── */
[data-testid="stAlert"] { border-radius: 12px; }
</style>
"""


def setup_page() -> None:
    """ページの初期設定とカスタム CSS を適用する。"""
    st.set_page_config(
        page_title="GDP 比較ダッシュボード",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(_CSS, unsafe_allow_html=True)
