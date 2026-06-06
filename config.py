"""アプリ全体で共有する定数・マスターデータ。"""

from __future__ import annotations

# ── 世界銀行 ──────────────────────────────────────────────

WB_COUNTRIES: dict[str, str] = {
    "日本": "JP", "アメリカ": "US", "中国": "CN", "ドイツ": "DE",
    "インド": "IN", "イギリス": "GB", "フランス": "FR", "ブラジル": "BR",
    "カナダ": "CA", "韓国": "KR", "オーストラリア": "AU", "イタリア": "IT",
    "ロシア": "RU", "メキシコ": "MX", "インドネシア": "ID", "スペイン": "ES",
}

WB_EN_TO_JP: dict[str, str] = {
    "Japan": "日本", "United States": "アメリカ", "China": "中国",
    "Germany": "ド���ツ", "India": "インド", "United Kingdom": "イギリス",
    "France": "フランス", "Brazil": "ブラジル", "Canada": "カナダ",
    "Korea, Rep.": "韓国", "Australia": "オーストラリア", "Italy": "イタリア",
    "Russian Federation": "ロシア", "Mexico": "メキシコ",
    "Indonesia": "インドネシア", "Spain": "スペイン",
}

WB_DEFAULTS: list[str] = ["日本", "アメリカ", "中国", "ドイツ", "インド"]
WB_INDICATOR: str = "NY.GDP.MKTP.CD"
WB_GROWTH_INDICATOR: str = "NY.GDP.MKTP.KD.ZG"

# ── IMF / 成長率（World Bank経由）────────────────────────

IMF_COUNTRIES: dict[str, str] = {
    "JPN": "日本", "USA": "アメリカ", "CHN": "中国", "DEU": "ドイツ",
    "IND": "インド", "GBR": "イギリス", "FRA": "フランス", "BRA": "ブラジル",
    "CAN": "カナダ", "KOR": "韓国", "AUS": "オーストラリア", "ITA": "イタリア",
    "RUS": "ロシア", "MEX": "メキシコ", "IDN": "インドネシア", "ESP": "スペイン",
}

IMF_ALPHA3_TO_ALPHA2: dict[str, str] = {
    "JPN": "JP", "USA": "US", "CHN": "CN", "DEU": "DE", "IND": "IN",
    "GBR": "GB", "FRA": "FR", "BRA": "BR", "CAN": "CA", "KOR": "KR",
    "AUS": "AU", "ITA": "IT", "RUS": "RU", "MEX": "MX", "IDN": "ID",
    "ESP": "ES",
}

IMF_DEFAULTS: list[str] = ["JPN", "USA", "CHN", "DEU", "IND"]

# ── FRED ─────────────────────────────────────────────────

FRED_BASE_URL: str = "https://api.stlouisfed.org/fred/series/observations"

FRED_SERIES: dict[str, dict[str, str]] = {
    "JPNPROINDMISMEI": {"label": "鉱工業生産指数", "unit": "指数", "type": "実績"},
    "LRUN64TTJPM156S": {"label": "完全失業率",     "unit": "%",   "type": "実績"},
    "JPNCPIALLMINMEI": {"label": "CPI（消費者物価）", "unit": "指数", "type": "実績"},
}

# ── e-Stat ────────────────────────────────────────────────

ESTAT_BASE_URL: str = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
ESTAT_STATS_DATA_ID: str = "0003446461"
ESTAT_TAB_CI: str = "100"
ESTAT_CI_CODES: dict[str, str] = {
    "100": "先行CI",
    "110": "一致CI",
}

# ── カラーパレット ────────────────────────────────────────

COLOR_PALETTE: list[str] = [
    "#e94560", "#0f3460", "#16c79a", "#f5a623",
    "#8b5cf6", "#06b6d4", "#f43f5e", "#10b981",
    "#6366f1", "#ec4899", "#14b8a6", "#f59e0b",
    "#3b82f6", "#ef4444", "#22c55e", "#a855f7",
]
