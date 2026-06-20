"""World Bank API からのデータ取得関数。"""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests
import streamlit as st

from config import (
    IMF_ALPHA3_TO_ALPHA2,
    IMF_COUNTRIES,
    WB_EN_TO_JP,
    WB_GROWTH_INDICATOR,
    WB_INDICATOR,
)


import logging

logger = logging.getLogger(__name__)


def _wb_get(url: str, params: dict[str, Any], source: str) -> Any:
    """World Bank API へ GET し、JSON を返す。エラーは RuntimeError に変換する。"""
    logger.info(f"Fetching from {source}. URL: {url} with params: {params}")
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError as exc:
        err_msg = f"{source} への接続に失敗しました。ネットワーク接続を確認してください。"
        logger.error(f"{err_msg} Details: {exc}", exc_info=True)
        raise RuntimeError(err_msg)
    except requests.exceptions.Timeout as exc:
        err_msg = f"{source} からの応答がタイムアウトしました。"
        logger.error(f"{err_msg} Details: {exc}", exc_info=True)
        raise RuntimeError(err_msg)
    except requests.exceptions.HTTPError as exc:
        err_msg = f"{source} エラー: {exc}"
        logger.error(f"{err_msg}", exc_info=True)
        raise RuntimeError(err_msg)
        
    logger.info(f"Successfully fetched JSON from {source}")
    return resp.json()



@st.cache_data(ttl=86400, show_spinner=False)
def fetch_wb_gdp(
    country_codes: tuple[str, ...],
    start: int,
    end: int,
) -> pd.DataFrame:
    """世界銀行 API v2 から GDP（米ドル建て）データを取得する。

    Args:
        country_codes: ISO alpha-2 国コードのタプル。
        start: 開始年。
        end: 終了年。

    Returns:
        「国」「年」「GDP (USD)」列を持つ DataFrame。
    """
    url = f"https://api.worldbank.org/v2/country/{';'.join(country_codes)}/indicator/{WB_INDICATOR}"
    data = _wb_get(url, {"date": f"{start}:{end}", "format": "json", "per_page": 10000}, "世界銀行 API")

    if not isinstance(data, list) or len(data) < 2 or data[1] is None:
        raise RuntimeError("世界銀行 API からデータを取得できませんでした。国や期間の選択を見直してください。")

    records = [
        {
            "国": WB_EN_TO_JP.get(item["country"]["value"], item["country"]["value"]),
            "年": int(item["date"]),
            "GDP (USD)": float(item["value"]),
        }
        for item in data[1]
        if item.get("value") is not None
    ]

    if not records:
        raise RuntimeError("選択した条件に該当するデータが見つかりませんでした。")

    result = pd.DataFrame(records).sort_values(["国", "年"]).reset_index(drop=True)
    logger.info(f"Successfully loaded WB GDP data. Rows: {len(result)}")
    return result


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_imf_gdp_growth(
    country_codes: tuple[str, ...],
    start: int,
    end: int,
) -> pd.DataFrame:
    """World Bank API から実質 GDP 成長率データを取得する。

    Args:
        country_codes: ISO alpha-3 国コードのタプル。
        start: 開始年。
        end: 終了年。

    Returns:
        国コード（alpha-3）をインデックス、年 (int) を列とする DataFrame。
    """
    alpha2_to_alpha3 = {v: k for k, v in IMF_ALPHA3_TO_ALPHA2.items()}
    codes_a2 = [IMF_ALPHA3_TO_ALPHA2[c] for c in country_codes if c in IMF_ALPHA3_TO_ALPHA2]
    url = f"https://api.worldbank.org/v2/country/{';'.join(codes_a2)}/indicator/{WB_GROWTH_INDICATOR}"
    data = _wb_get(url, {"date": f"{start}:{end}", "format": "json", "per_page": 10000}, "World Bank API")

    if not isinstance(data, list) or len(data) < 2 or data[1] is None:
        raise RuntimeError("World Bank API から成長率データを取得できませんでした。")

    records: dict[str, dict[int, float]] = {}
    for item in data[1]:
        if item.get("value") is None:
            continue
        iso3 = item.get("countryiso3code", "")
        code = iso3 if iso3 in IMF_COUNTRIES else alpha2_to_alpha3.get(item["country"]["id"], "")
        if not code:
            continue
        records.setdefault(code, {})[int(item["date"])] = float(item["value"])

    if not records:
        raise RuntimeError("選択した条件に該当する成長率データが見つかりませんでした。")

    df = pd.DataFrame(records).T
    df.columns = df.columns.astype(int)
    df.index.name = "country_code"
    result = df.sort_index(axis=1)
    logger.info(f"Successfully loaded IMF growth data. Shape: {result.shape}")
    return result

