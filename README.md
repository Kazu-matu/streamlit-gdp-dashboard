# 📊 各国GDP比較ダッシュボード

世界銀行・FRED・e-Stat（内閣府）の公開APIを統合した Streamlit ダッシュボード。  
各国のGDP・実質成長率・日本の経済指標をインタラクティブに可視化・比較できます。

---

## 機能

| タブ | データソース | 主要指標 |
|---|---|---|
| 🌍 世界銀行 GDP | World Bank API v2 | GDP（米ドル建て）`NY.GDP.MKTP.CD` |
| 📈 IMF GDP 成長率 | World Bank API v2 | 実質 GDP 成長率 `NY.GDP.MKTP.KD.ZG` |
| 🇯🇵 日本経済指標 | FRED + e-Stat（内閣府） | 鉱工業生産・失業率・CPI・景気動向指数 |

- **国・期間をサイドバーで動的選択**（マルチセレクト + スライダー）
- **CSVダウンロード**（UTF-8 BOM付き、Excel対応）
- **24時間キャッシュ**でAPI負荷軽減
- **Playwright自動デモ録画**（8ステップ WebM）

---

## クイックスタート

```powershell
# 1. 依存パッケージをインストール
uv sync

# 2. APIキーを設定（.env.example をコピーして編集）
copy .env.example .env
# .env に FRED_API_KEY と ESTAT_APP_ID を記入

# 3. アプリ起動
uv run streamlit run app.py
```

ブラウザで `http://localhost:8501` が開きます。

### 自動デモ録画

```powershell
# Playwright ブラウザを初回インストール
uv run playwright install chromium

# デモ実行 & WebM 録画
$env:PYTHONIOENCODING="utf-8"; uv run python demo_playwright.py
```

---

## ディレクトリ構成

```
gdp-dashboard/
├── app.py              # エントリーポイント（タブ制御・session_state）
├── config.py           # 全定数（国コード・API設定・カラーパレット）
├── pyproject.toml      # 依存パッケージ（uv管理）
├── .env                # APIキー ※コミット禁止
├── data/               # データ取得層（World Bank / FRED / e-Stat）
├── views/              # UI描画層（各タブ・サイドバー・共通部品）
├── demo_playwright.py  # 自動デモ & 録画スクリプト
└── docs/               # ドキュメント一覧（下記参照）
```

---

## 新しいダッシュボードの雛形を作る（create_template.py）

このリポジトリには **テンプレート生成スクリプト** が含まれています。  
コマンド 1 つで、Streamlit + pandas + Plotly の雛形プロジェクトを生成し、そのまま GitHub テンプレートリポジトリとして公開できます。

### 生成コマンド

```bash
# <アプリ名> は Python の識別子（英数字・アンダースコア、先頭は英字）
uv run python create_template.py <アプリ名>

# 例
uv run python create_template.py trade_dashboard
```

生成先: スクリプトと **同じ階層の上の親ディレクトリ** に `<アプリ名>/` フォルダが作られます。

```
D:\
├── streamlit-gdp-dashboard\  ← このリポジトリ
│   └── create_template.py
└── trade_dashboard\          ← 生成されるフォルダ
    ├── app.py / config.py
    ├── data/worldbank.py     ← @st.cache_data 付きデータ取得
    ├── views/                ← 描画専用レイヤー
    ├── tests/test_imports.py ← スモークテスト（即実行可）
    ├── docs/                 ← 01_要件定義 〜 04_報告書 + 開発入門
    ├── AI_INSTRUCTIONS.md
    ├── .github/copilot-instructions.md
    └── .github/workflows/ci.yml  ← GitHub Actions（自動テスト）
```

### 生成後の確認

```bash
cd ..\trade_dashboard     # Windows
cd ../trade_dashboard     # Mac/Linux

copy .env.example .env
uv sync

# スモークテスト（インポート確認）
uv run pytest tests/test_imports.py -v

# アプリ起動
uv run streamlit run app.py
# → http://localhost:8501/ を開いて動作確認
```

### GitHub テンプレートリポジトリとして公開する

```bash
cd ..\trade_dashboard

git init
git add .
git commit -m "chore: initial template"

# GitHub CLI でリポジトリ作成 & プッシュ
gh repo create trade_dashboard --public --source=. --remote=origin --push

# 「Use this template」ボタンを有効化
gh repo edit trade_dashboard --template
```

---

## ドキュメント

| ドキュメント | 内容 |
|---|---|
| [docs/spec.md](docs/spec.md) | アプリ仕様書（アーキテクチャ・Mermaid図・画面設計） |
| [docs/project_report.md](docs/project_report.md) | プロジェクト完了報告書（成果物・技術課題・セキュリティ検査結果） |
| [docs/vibe_coding_guide.md](docs/vibe_coding_guide.md) | バイブコーディング爆速開発ガイド（初心者向け・プロンプト例付き） |
| [docs/japan_indicators_research.md](docs/japan_indicators_research.md) | 日本経済指標 API 調査メモ |
| [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) | AI開発指示書（ChatGPT / Gemini / Copilot / Cursor / Claude 共通） |

---

## 必要なAPIキー

| キー | 取得先 | 用途 |
|---|---|---|
| `FRED_API_KEY` | [FRED（セントルイス連銀）](https://fred.stlouisfed.org/docs/api/api_key.html) | 鉱工業生産・失業率・CPI |
| `ESTAT_APP_ID` | [e-Stat API](https://www.e-stat.go.jp/api/) | 景気動向指数（内閣府） |

World Bank API は認証不要です。

---

## 技術スタック

Python 3.10+ / Streamlit 1.40+ / Plotly 5.20+ / pandas 2.0+ / uv / Playwright

---

## セキュリティ

- pip-audit: **既知の脆弱性 0件**（55パッケージ対象）
- Bandit: **指摘事項 0件**（730行対象）

詳細は [docs/project_report.md](docs/project_report.md) の Section 8 を参照。
