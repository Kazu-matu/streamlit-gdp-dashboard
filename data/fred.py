"""FRED API からのデータ取得関数。"""

from __future__ import annotations
import logging
import os

import pandas as pd
import requests
import streamlit as st

from config import FRED_BASE_URL

logger = logging.getLogger(__name__)


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
        err_msg = "FRED_API_KEY が設定されていません。.env を確認してください。"
        logger.error(err_msg)
        raise RuntimeError(err_msg)

    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start,
        "observation_end": end,
    }
    logger.info(f"Fetching FRED series: {series_id} for period {start} to {end}")
    try:
        resp = requests.get(FRED_BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        err_msg = "FRED API への接続に失敗しました。"
        logger.error(f"{err_msg} Details: {exc}", exc_info=True)
        raise RuntimeError(err_msg)
    except requests.exceptions.Timeout as exc:
        err_msg = "FRED API からの応答がタイムアウトしました。"
        logger.error(f"{err_msg} Details: {exc}", exc_info=True)
        raise RuntimeError(err_msg)
    except requests.exceptions.HTTPError as exc:
        err_msg = f"FRED API エラー: {exc}"
        logger.error(err_msg, exc_info=True)
        raise RuntimeError(err_msg)

    observations = resp.json().get("observations", [])
    if not observations:
        err_msg = f"FRED からデータを取得できませんでした（{series_id}）。"
        logger.error(err_msg)
        raise RuntimeError(err_msg)

    df = pd.DataFrame([
        {"日付": row["date"], "値": pd.to_numeric(row["value"], errors="coerce")}
        for row in observations
    ])
    df["日付"] = pd.to_datetime(df["日付"])
    result = df.dropna(subset=["値"]).reset_index(drop=True)
    logger.info(f"Successfully loaded FRED series {series_id}. Rows: {len(result)}")
    return result

