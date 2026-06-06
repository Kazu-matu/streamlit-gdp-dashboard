"""FRED API からのデータ取得関数。"""

from __future__ import annotations

import os

import pandas as pd
import requests
import streamlit as st

from config import FRED_BASE_URL


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_fred_series(series_id: str, start: str, end: str) -> pd.DataFrame:
    """FRED API から指定シリーズの月次データを取得する。

    Args:
        series_id: FRED シリーズID（例: "JPNPROINDMISMEI"）。
        start: 取得開始日 "YYYY-MM-DD"。
        end: 取得終了日 "YYYY-MM-DD"。

    Returns:
        「日付」「値」列を持つ DataFrame。
    """
    api_key = os.environ.get("FRED_API_KEY", "")
    if not api_key:
        raise RuntimeError("FRED_API_KEY が設定されていません。.env を確認してください。")

    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start,
        "observation_end": end,
    }
    try:
        resp = requests.get(FRED_BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise RuntimeError("FRED API への接続に失敗しました。")
    except requests.exceptions.Timeout:
        raise RuntimeError("FRED API からの応答がタイムアウトしました。")
    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(f"FRED API エラー: {exc}")

    observations = resp.json().get("observations", [])
    if not observations:
        raise RuntimeError(f"FRED からデータを取得できませんでした（{series_id}）。")

    df = pd.DataFrame([
        {"日付": row["date"], "値": pd.to_numeric(row["value"], errors="coerce")}
        for row in observations
    ])
    df["日付"] = pd.to_datetime(df["日付"])
    return df.dropna(subset=["値"]).reset_index(drop=True)
