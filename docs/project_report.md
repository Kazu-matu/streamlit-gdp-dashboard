# 各国GDP比較ダッシュボード — プロジェクト完了報告書

作成日: 2026-06-06  
プロジェクト期間: 2026-06-06（単日完了）

---

## 1. プロジェクト概要

世界銀行・IMF・FRED・e-Stat の4つの公開APIを統合し、各国GDP・経済成長率・日本の経済指標を可視化・比較する Streamlit ダッシュボードを開発した。  
開発・検証・リファクタリング・ドキュメント整備までを一貫して実施。

---

## 2. 成果物一覧

### 2.1 アプリケーション

| ファイル / ディレクトリ | 役割 |
|---|---|
| `app.py` | エントリーポイント・タブ制御・セッション管理 |
| `config.py` | 全定数・マスターデータ（国コード・API URL・カラーパレット） |
| `data/worldbank.py` | 世界銀行 GDP・成長率データ取得 |
| `data/fred.py` | FRED 月次指標データ取得 |
| `data/estat.py` | e-Stat 景気動向指数データ取得 |
| `views/page_config.py` | ページ設定・グローバル CSS |
| `views/sidebar.py` | サイドバー UI |
| `views/components.py` | 共通 UI 部品（CSV ダウンロード・テーブル） |
| `views/worldbank_tab.py` | 世界銀行 GDP タブ描画 |
| `views/imf_tab.py` | IMF 成長率タブ描画 |
| `views/japan_tab.py` | 日本経済指標タブ描画 |
| `pyproject.toml` | 依存パッケージ定義（uv 管理） |
| `.env` | API キー（FRED / e-Stat） |

### 2.2 自動化スクリプト

| ファイル | 役割 |
|---|---|
| `demo_playwright.py` | Playwright による自動デモ & WebM 録画（8ステップ） |

### 2.3 ドキュメント

| ファイル | 内容 |
|---|---|
| `docs/spec.md` | アプリ仕様書（アーキテクチャ・画面設計・Mermaid図） |
| `docs/japan_indicators_research.md` | 日本経済指標 API 調査メモ |
| `docs/prompts.md` | 開発プロンプト履歴 |

### 2.4 録画ファイル

デモ実行のたびに `*.webm` として出力。最終確認済み録画を含む計3件。

---

## 3. 実装機能

### 3.1 タブ構成

| タブ | データソース | 主要指標 |
|---|---|---|
| 🌍 世界銀行 GDP | World Bank API v2 | GDP（米ドル建て）`NY.GDP.MKTP.CD` |
| 📈 IMF GDP 成長率 | World Bank API v2 | 実質 GDP 成長率 `NY.GDP.MKTP.KD.ZG` |
| 🇯🇵 日本経済指標 | FRED + e-Stat（内閣府） | 鉱工業生産・失業率・CPI・景気動向指数 |

### 3.2 共通機能

- **国・期間の動的選択**（マルチセレクト + スライダー）
- **ボタン押下時のオンデマンド取得**（初期表示ではAPI呼び出しなし）
- **24時間キャッシュ**（`@st.cache_data(ttl=86400)`）によるAPI負荷軽減
- **CSV ダウンロード**（UTF-8 BOM 付き、Excel 対応）
- **エラーハンドリング**（接続エラー・タイムアウト・空データを `st.error` で通知）
- **セッション状態保持**（タブ切替時もデータを保持）

### 3.3 日本経済指標（詳細）

| 指標 | API | シリーズID | 種別 |
|---|---|---|---|
| 景気動向指数 先行CI | e-Stat（内閣府） | `0003446461` cat01=100 | 先行 |
| 景気動向指数 一致CI | e-Stat（内閣府） | `0003446461` cat01=110 | 実績 |
| 鉱工業生産指数 | FRED | `JPNPROINDMISMEI` | 実績 |
| 完全失業率 | FRED | `LRUN64TTJPM156S` | 実績 |
| CPI（消費者物価） | FRED | `JPNCPIALLMINMEI` | 実績 |

---

## 4. アーキテクチャ

### 4.1 モジュール構成

リファクタリングにより 1014 行の単一ファイルを11モジュールに分割。

| 区分 | ファイル数 | 合計行数 | 最大行数/ファイル |
|---|---|---|---|
| リファクタリング前 | 1 | 1,014 行 | 1,014 行 |
| リファクタリング後 | 11 | 901 行 | 120 行 |

### 4.2 設計方針

- **関心の分離**: データ取得（`data/`）・UI 描画（`views/`）・定数（`config.py`）を完全分離
- **拡張性**: 指標追加は `config.py` の `FRED_SERIES` に1エントリ追加するだけで対応可能
- **環境非依存**: `pyproject.toml` + `uv` による仮想環境管理（`.venv`）でシステム Python に依存しない

---

## 5. 解決した技術的課題

| 課題 | 原因 | 対応 |
|---|---|---|
| `UnicodeEncodeError` | Windows コンソールの cp932 エンコーディング | `PYTHONIOENCODING=utf-8` を設定 |
| `ModuleNotFoundError: plotly` | システム Python でアプリ起動していた | `pyproject.toml` + `uv sync` で仮想環境を構築 |
| IMF API 403 エラー | IMF サーバーが `www.imf.org` からのリクエストをブロック | 同一指標（`NY.GDP.MKTP.KD.ZG`）を World Bank API で代替取得 |
| e-Stat `'DATA_INF'` KeyError | カテゴリコード・`cdTab` パラメータの誤り | 正しいコード（`cdTab=100`, `cdCat01=100,110`）とタイムコードパース（位置6〜8桁）に修正 |

---

## 6. 検証結果

### 6.1 Playwright 自動デモ（最終実行）

| ステップ | 内容 | 結果 |
|---|---|---|
| 1 | アプリ起動・Streamlit ロード待機 | ✅ |
| 2 | 世界銀行「データ取得」クリック → チャート表示 | ✅ |
| 3 | スムーズスクロールでグラフ閲覧 | ✅ |
| 4 | 生データ エクスパンダー展開 | ✅ |
| 5 | ページトップへ戻る | ✅ |
| 6 | IMF タブに切り替え | ✅ |
| 7 | IMF「データ取得」クリック → チャート表示 | ✅ |
| 8 | IMF グラフ・テーブル閲覧 | ✅ |

録画ファイル: `page@6b246a1a9cf07be19f7c3cb49e6e4916.webm`（5.5 MB）

### 6.2 構文チェック

全11モジュールの `ast.parse` チェック: **全件 OK**

---

## 7. 実行方法

```powershell
# 初回セットアップ
uv sync
playwright install chromium   # デモ録画用

# アプリ起動
uv run streamlit run app.py

# 自動デモ & 録画
$env:PYTHONIOENCODING="utf-8"; uv run python demo_playwright.py
```

---

## 8. セキュリティ検査結果

実施日: 2026-06-06

### 8.1 依存パッケージ脆弱性スキャン（pip-audit）

`uv audit` は現バージョン（gdp-dashboard 0.1.0）で未サポートのため、`pip-audit` を使用。  
`uv export` で生成した依存ロックファイル（55パッケージ）を対象にスキャンを実施。

```
$ pip-audit -r requirements.txt
Resolved 55 packages in 0.76ms
No known vulnerabilities found
```

**結果: 既知の脆弱性 0 件**

| 対象 | パッケージ数 | 検出件数 |
|---|---|---|
| 直接依存 + 推移的依存 | 55 | **0** |

### 8.2 静的コード解析（Bandit）

ソースコード（`app.py` / `config.py` / `data/` / `views/`）730行を対象に解析。

```
$ bandit -r app.py config.py data/ views/

Test results:
    No issues identified.

Code scanned:
    Total lines of code: 730
    Total lines skipped (#nosec): 0

Run metrics:
    Total issues (by severity):
        Low: 0 / Medium: 0 / High: 0
    Total issues (by confidence):
        Low: 0 / Medium: 0 / High: 0
```

**結果: 指摘事項 0 件**

| 深刻度 | 件数 |
|---|---|
| High | **0** |
| Medium | **0** |
| Low | **0** |

### 8.3 総評

| 検査項目 | ツール | 結果 |
|---|---|---|
| 依存パッケージ既知脆弱性 | pip-audit | ✅ 問題なし |
| ソースコード静的解析 | Bandit | ✅ 問題なし |

---

## 9. 今後の拡張候補

| 項目 | 概要 |
|---|---|
| 指標追加 | `config.py` の `FRED_SERIES` に追加するだけで日本指標を拡張可能 |
| 対象国追加 | `WB_COUNTRIES` / `IMF_COUNTRIES` にエントリを追加 |
| Streamlit マルチページ化 | タブをページ分割し、URL で直接アクセス可能にする |
| テスト追加 | `data/` 層の取得関数に pytest + モックを整備 |
| CI/CD | GitHub Actions で `uv run python -m pytest` を自動実行 |
