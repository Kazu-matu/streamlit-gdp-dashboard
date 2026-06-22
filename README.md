# 📊 各国GDP比較ダッシュボード

世界銀行・FRED・e-Stat（内閣府）の公開APIを統合した Streamlit ダッシュボード。  
各国のGDP・実質成長率・日本の経済指標をインタラクティブに可視化・比較できます。

---

## 各ページの機能

| ページ | データソース | 主な指標 |
| ------ | ----------- | ------- |
| 🌍 世界銀行 | World Bank API v2 | GDP（米ドル建て）`NY.GDP.MKTP.CD` の国際比較 |
| 📈 IMF | World Bank API v2（成長率） | 実質 GDP 成長率 `NY.GDP.MKTP.KD.ZG` の国際比較 |
| 🇯🇵 日本経済指標 | FRED / e-Stat | 鉱工業生産・失業率・CPI・景気動向指数 |
| 📁 CSV | ローカルファイル | ダミー GDP データ（CSV） |
| 🗄️ SQLite | ローカルファイル | ダミー GDP データ（SQLite） |
| 📊 Excel | ローカルファイル | ダミー GDP データ（Excel） |

**対象国（世界銀行・IMF）**: 日本・アメリカ・中国・ドイツ・インド・イギリス・フランス・ブラジル・カナダ・韓国 ほか 16 カ国

- **左サイドバーのナビゲーション**でページを切り替え
- **各ページのサイドバー**で国・期間を動的選択（マルチセレクト + スライダー）
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
├── app.py              # ホームページ（概要・ページ一覧）
├── pages/              # マルチページ（Streamlit 自動ナビゲーション）
│   ├── 1_🌍_世界銀行.py
│   ├── 2_📈_IMF.py
│   ├── 3_🇯🇵_日本経済指標.py
│   ├── 4_📁_CSV.py
│   ├── 5_🗄️_SQLite.py
│   └── 6_📊_Excel.py
├── config.py           # 全定数（国コード・API設定・カラーパレット）
├── pyproject.toml      # 依存パッケージ（uv管理）
├── build.bat           # EXE ビルドスクリプト（PyInstaller）
├── launcher.py         # EXE 起動ラッパー（ブラウザ自動起動）
├── .env                # APIキー ※コミット禁止
├── data/               # データ取得層（World Bank / FRED / e-Stat / ローカル）
├── views/              # UI描画層（各ページ描画関数・共通部品）
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

---

## 🛠️ フレームワーク設計原則 & 開発ガイドライン (EUC/DS専門家目線)

本リポジトリは、Streamlit を用いた堅牢なダッシュボード構築、およびデータサイエンスの製造現場・実務適用に向けた「フレームワーク」として以下の設計原則・注意点を定義しています。

### 1. データサイエンティスト＆システム開発専門家のアドバイス
- **相関関係と因果関係の混同防止**: 統計的な相関（例: プロセス温度と歩留まり）があるからといって、因果関係があるとは限りません。物理的・化学的なプロセス知識（ドメイン知識）と照らし合わせ、AIの分析結果が常識と矛盾しないか必ず人間が検証してください。
- **製造現場の異常値と外れ値の分類**: センサーの一時的な通信瞬断やノイズ（単なる欠損）と、装置の過熱などの急激なプロセス変化（異常予兆）を区別してください。安易な `dropna()` や一律の `fillna(mean)` で片付けるコードは作成せず、ドメインに合わせた前処理を選択してください。
- **概念ドリフト（モデルの経年劣化）対策**: 装置の経年摩耗、季節の変化（外気温・湿度の差）、原料ロットの違いによって予測モデルの精度は徐々に低下します。定期的な再学習（Retraining）や、予測誤差が許容値を超えた際にアラートを出す設計をあらかじめ組み込んでください。
- **GIGO (Garbage In, Garbage Out)**: 入力データの品質や制約条件（例: 設備の最大稼働時間）の定義が現実と乖離していれば、どんなに高度なアルゴリズムも「使い物にならないゴミ」を出力します。アルゴリズム調整以上にデータと制約条件の検証に時間を割いてください。
- **大容量データ（100MB以上）の処理指針**: 通常の `pandas` での読み込みは速度低下やメモリ不足を引き起こします。そのような場合は、AIに指示して高速な **Polars**（並列処理）、**DuckDB**（インメモリSQL実行）、あるいは圧縮効率とパース速度に優れた **Parquet形式**（`.parquet` 列指向バイナリ）による処理を組み込んでください。

### 2. Windows スタンドアロン EXE（PyInstaller）化での注意事項
本フレームワークは `pyinstaller` を用いた Windows 向けスタンドアロン EXE 配布に対応していますが、ビルドの際は以下に注意してください。
- **動的なパス解決 (`sys.frozen` のハンドリング)**:
  PyInstaller EXE 起動時は、コードが一時フォルダ `sys._MEIPASS` に展開されます。そのため、パス解決を以下のように使い分ける必要があります。
  - **`exe_dir` (sys.executable基準)**: ユーザーが書き換え可能な外部設定ファイル（`.env`）、ログファイル（`app.log`）、およびデータベースファイル（SQLite等）などの動的アセットを配置・取得します。
  - **`base_dir` (sys._MEIPASS基準 / `__file__`基準)**: 実行ファイル内部に Bundled されたプログラムコードや静的なテンプレートファイルを取得します。
- **バックグラウンド起動とポート待機制御**: `launcher.py` は、コンソールを立ち上げずにバックグラウンドスレッドで Streamlit Web サーバーを起動し、ポートの通信準備が整い次第デフォルトの Web ブラウザを自動表示する制御を行っています。
- **Hidden Imports とビルド構成**: PyInstaller は Streamlit やサードパーティエンジン（`openpyxl`, `sqlite3` 等）の動的インポートを静的解析で検知できません。ビルド用のバッチスクリプト（`build.bat`）で `--hidden-import` オプションを明示指定して同梱させてください。

### 3. バイブコーディング（Vibe Coding）における AI 指示の徹底
AI（Cursor/Copilot/Gemini/Claude等）を用いたバイブコーディングを行う際、AIが迷ったり誤った実装へデグレードさせないための指示基準です。
- **例外の伝播とログ記録ポリシー**: データ取得層（`data/*.py`）でエラーが発生した際、**例外をその場でにぎりつぶして空の DataFrame を返してはいけません。** `logger.error("...", exc_info=True)` により `app.log` へ完全なスタックトレースを明示的に出力した上で、`RuntimeError` などを発生させて呼び出し元（`app.py` などの UI/Orchestrator 層）へ必ず伝播（raise）させてください。UI層がこれをキャッチして `st.error` で適切にユーザーフレンドリーなメッセージを表示します。
- **Streamlitキャッシュの落とし穴回避**: `@st.cache_data` は引数をハッシュキーにするため、`list` や `dict` などのミュータブル（変更可能）オブジェクトを渡すと `UnhashableTypeError` が発生します。引数には必ず `tuple` や `str`, `int` などのイミュータブル（変更不可能）オブジェクトを使用するように強制してください。
- **Windows 環境への配慮**: PowerShell / CMD で実行されるため、POSIX系（Linux系）のコマンド（`rm -rf` や `cp`）の提案・実行は禁止し、PowerShellコマンドまたは Python の標準ライブラリ（`shutil`, `os` 等）を使用させてください。
- **開発前の Git Checkpoint コミットの徹底**: 新しいデータソースやモジュールの追加、大規模なリファクタリングなどを行う前は、必ず AI 自体に「これから変更されるファイル一覧」を出力させ、Git コミットによるセーブポイントの作成を促すプロセスを徹底してください。
