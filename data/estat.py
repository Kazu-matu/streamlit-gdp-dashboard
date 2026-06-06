"""e-Stat API からのデータ取得関数。"""

from __future__ import annotations

import os

import pandas as pd
import requests
import streamlit as st

from config import ESTAT_BASE_URL, ESTAT_CI_CODES, ESTAT_STATS_DATA_ID, ESTAT_TAB_CI


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_estat_ci() -> pd.DataFrame:
    """e-Stat API から景気動向指数（先行CI・一致CI）を取得する。

    Returns:
        「日付」「指標」「値」列を持つ DataFrame。
    """
    app_id = os.environ.get("ESTAT_APP_ID", "")
    if not app_id:
        raise RuntimeError("ESTAT_APP_ID が設定されていません。.env を確認してください。")

    params = {
        "appId": app_id,
        "statsDataId": ESTAT_STATS_DATA_ID,
        "cdTab": ESTAT_TAB_CI,
        "cdCat01": ",".join(ESTAT_CI_CODES.keys()),
        "limit": 10000,
    }
    try:
        resp = requests.get(ESTAT_BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise RuntimeError("e-Stat API への接続に失敗しました。")
    except requests.exceptions.Timeout:
        raise RuntimeError("e-Stat API からの応答がタイムアウトしました。")
    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(f"e-Stat API エラー: {exc}")

    try:
        stat_data = resp.json()["GET_STATS_DATA"]["STATISTICAL_DATA"]
        if int(stat_data.get("RESULT_INF", {}).get("TOTAL_NUMBER", 0)) == 0:
            raise RuntimeError("e-Stat API から景気動向指数データを取得できませんでした（件数0）。")
        values = stat_data["DATA_INF"]["VALUE"]
    except KeyError as exc:
        raise RuntimeError(f"e-Stat API レスポンスの解析に失敗しました: {exc}")

    records = []
    for v in values:
        label = ESTAT_CI_CODES.get(v.get("@cat01", ""))
        if label is None:
            continue
        time_code = v.get("@time", "")
        try:
            date = pd.Timestamp(year=int(time_code[:4]), month=int(time_code[6:8]), day=1)
        except (ValueError, IndexError):
            continue
        val = pd.to_numeric(v.get("$", ""), errors="coerce")
        if pd.notna(val):
            records.append({"日付": date, "指標": label, "値": val})

    if not records:
        raise RuntimeError("e-Stat から景気動向指数データを取得できませんでした。")

    return pd.DataFrame(records).sort_values(["指標", "日付"]).reset_index(drop=True)
