# AI開発指示書 — 各国GDP比較ダッシュボード

> このファイルはAIアシスタント（Claude / ChatGPT / Gemini / Copilot 等）が  
> プロジェクトの文脈を即座に把握するための指示書です。  
> 会話の冒頭にこのファイルの内容を貼り付けるか、添付してください。

---

## 1. プロジェクト概要

**アプリ名**: 各国GDP比較ダッシュボード  
**目的**: 世界銀行・FRED・e-Stat（内閣府）の公開APIを使い、各国のGDPおよび日本の経済指標を可視化・比較する  
**実行方法**: `uv run streamlit run app.py`  
**URL**: `http://localhost:8501`

---

## 2. 技術スタック

| 項目 | 採用技術 | バージョン |
|---|---|---|
| 言語 | Python | 3.10+ |
| フレームワーク | Streamlit | 1.40+ |
| 可視化 | Plotly Express | 5.20+ |
| データ処理 | pandas | 2.0+ |
| HTTP通信 | requests | 2.31+ |
| 環境管理 | uv + pyproject.toml | — |
| テスト・録画 | Playwright | 1.40+ |
| APIキー管理 | python-dotenv + .env | — |

---

## 3. ディレクトリ構成と各ファイルの役割

```
gdp-dashboard/
├── app.py              # エントリーポイント。タブ制御・session_state管理のみ。ロジックは書かない
├── config.py           # 全定数・マスターデータ。国コード追加はここだけ変更する
├── pyproject.toml      # 依存パッケージ。追加は `uv add <pkg>` で行う
├── .env                # APIキー（FRED_API_KEY / ESTAT_APP_ID）。コミット禁止
├── data/
│   ├── worldbank.py    # fetch_wb_gdp(), fetch_imf_gdp_growth() — World Bank API
│   ├── fred.py         # fetch_fred_series() — FRED API
│   └── estat.py        # fetch_estat_ci() — e-Stat API（景気動向指数）
├── views/
│   ├── page_config.py  # setup_page() — ページ設定・グローバルCSS
│   ├── sidebar.py      # render_sidebar() — サイドバーUI・ユーザー入力
│   ├── components.py   # csv_download_button(), data_table_with_download() — 共通部品
│   ├── worldbank_tab.py # render_wb_dashboard() — 世界銀行タブ
│   ├── imf_tab.py      # render_imf_dashboard() — IMF成長率タブ
│   └── japan_tab.py    # render_japan_dashboard() — 日本経済指標タブ
├── demo_playwright.py  # 自動デモ & WebM録画スクリプト（8ステップ）
└── docs/               # 仕様書・調査メモ・報告書・ガイド
```

---

## 4. アーキテクチャの原則

### 絶対に守ること

- **`app.py` にロジックを書かない** — データ取得・UI描画は各モジュールに委譲する
- **`config.py` に定数を集約する** — 国コード・URL・デフォルト値をコードに直書きしない
- **データ取得関数には `@st.cache_data(ttl=86400)` をつける** — API負荷軽減のため
- **`.env` をコミットしない** — APIキーはコードに書かない

### 指標・国を追加するときのルール

```python
# config.py の FRED_SERIES に1行追加するだけで日本指標が増える
FRED_SERIES: dict[str, dict[str, str]] = {
    "JPNPROINDMISMEI": {"label": "鉱工業生産指数", "unit": "指数", "type": "実績"},
    "LRUN64TTJPM156S": {"label": "完全失業率",     "unit": "%",   "type": "実績"},
    # ↑ここに追加するだけ。views/japan_tab.py は変更不要
}
```

---

## 5. データフロー

```
ユーザーが「🔍 データ取得」ボタンを押す
    ↓
app.py が inputs["xxx_execute"] == True を検知
    ↓
data/*.py の fetch_xxx() を呼ぶ（@st.cache_data でキャッシュ）
    ↓
外部API（World Bank / FRED / e-Stat）にHTTP GET
    ↓
pandas DataFrame に変換して返す
    ↓
st.session_state["xxx_data"] に保存
    ↓
views/*.py の render_xxx(df) を呼んでグラフ・テーブルを描画
```

---

## 6. 外部API仕様

### World Bank API v2
- **エンドポイント**: `https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}`
- **認証**: 不要
- **GDP**: `NY.GDP.MKTP.CD`（米ドル建て）
- **成長率**: `NY.GDP.MKTP.KD.ZG`（実質GDP成長率）
- **注意**: IMF Datamapper API（`www.imf.org`）は403エラーになるため使用しない

### FRED API（セントルイス連銀）
- **エンドポイント**: `https://api.stlouisfed.org/fred/series/observations`
- **認証**: APIキー必要（`.env` の `FRED_API_KEY`）
- **日本指標**: `JPNPROINDMISMEI`（鉱工業生産）/ `LRUN64TTJPM156S`（失業率）/ `JPNCPIALLMINMEI`（CPI）
- **注意**: 欠損値は `"."` で返るため `pd.to_numeric(errors="coerce")` で処理

### e-Stat API（内閣府）
- **エンドポイント**: `https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData`
- **認証**: アプリID必要（`.env` の `ESTAT_APP_ID`）
- **統計表ID**: `0003446461`（景気動向指数 長期系列）
- **パラメータ**: `cdTab=100`（CI指数）/ `cdCat01=100`（先行CI）/ `cdCat01=110`（一致CI）
- **タイムコード形式**: `"1980000101"` → 先頭4桁=年、6〜8桁=月

---

## 7. コーディング規約

- **型ヒント必須**: 全関数に引数・戻り値の型を記載
- **Docstring必須**: Args / Returns / Raises を記載
- **エラーは RuntimeError**: API関連エラーは `RuntimeError` に統一し、呼び出し側で `st.error()` 表示
- **コメントは「なぜ」だけ**: コードで分かる「何を」はコメント不要
- **日本語カラム名**: DataFrame のカラムは「国」「年」「値」等の日本語で統一
- **CSV出力**: `encoding="utf-8-sig"`（BOM付き）でExcel文字化けを防ぐ

---

## 8. AIへの作業依頼ガイド

### 機能追加

```
config.py の FRED_SERIES に「実質賃金指数（FRED: JPNLCULTTT01IXOBSAM）」を追加して。
views/japan_tab.py の描画も対応させて。
```

### バグ修正

```
以下のエラーが発生している。原因を特定して修正して。

[エラーメッセージをそのまま貼る]
```

### リファクタリング

```
japan_tab.py の _render_fred_metric 関数を見直して。
グラフのレイアウト設定が各指標で重複している。共通化できるか検討して。
```

### 新しいタブ追加

```
「為替レート」タブを追加したい。
FRED API で取得できる日米・日欧の為替シリーズIDを調べて、
既存の japan_tab.py と同じ構造で実装して。
```

### 検証・テスト

```
demo_playwright.py を更新して、新しく追加した「為替レート」タブの
データ取得〜グラフ表示までのステップも録画に含めて。
```

---

## 9. やってはいけないこと（AIへの禁止事項）

- `app.py` に直接データ取得ロジックを書かない
- `config.py` 以外の場所に国コードや URL を直書きしない
- `.env` の内容をコードやコメントに含めない
- `@st.cache_data` を外したり `ttl` を短くしない
- `pip install` で直接インストールしない（必ず `uv add` を使う）
- Windows環境のため、シェルスクリプト（`.sh`）は作成しない。PowerShell（`.ps1`）を使う

---

## 10. 現在の既知の制約・メモ

- IMF Datamapper API（`www.imf.org`）は403を返すため、World Bank API で代替している
- Windows環境（Python 3.14）では `PYTHONIOENCODING=utf-8` が必要
- Playwright録画ファイルはプロジェクトルートに `.webm` で出力される
- e-Stat API のタイムコードは `"YYYY00MM00"` 形式（例: `"2024000600"` = 2024年6月）
