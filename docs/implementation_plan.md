# 統合計画: EXE化対応およびマルチデータソースデモ機能の追加

この計画では、`D:\streamlit-gdp-dashboard` における以下の2つのタスクについて説明します。

1. **`create_template.py` のEXE化対応**: テンプレート生成スクリプトを更新し、生成されるプロジェクトが最初から PyInstaller によるEXE（実行ファイル）ビルドに対応した構成になるようにします（ランチャー、ビルドスクリプト、修正版のアプリ起動処理、`.gitignore`、READMEの追加）。
2. **メインアプリへのマルチデータソースデモ機能の追加**: フレームワークの柔軟性を示すため、ローカルデータソース（CSV、SQLite、Excel）からのデータ読み込み機能を追加し、ダミーデータ生成スクリプト、新規データ取得モジュール、ダッシュボードの新規タブを実装します。

---

## ユーザー確認が必要な事項

> [!IMPORTANT]
> - **依存関係の追加**: Pandas で Excel ファイルを読み込めるようにするため、`pyproject.toml` の `dependencies` に `openpyxl>=3.1.0` を追加します。その後、`uv sync` を実行してローカル環境を同期します。
> - **ダミーデータの自動生成**: ユーザーが「🔌 ローカルデータ読込」ボタンをクリックした際、もしローカルのダミーデータファイルが存在しない場合は、アプリ側で自動的に `generate_dummy_data.py` を呼び出してファイルをその場で自動生成します。

---

## 提案される変更点

### 1. テンプレートジェネレータ (`create_template.py`)

#### [MODIFY] [create_template.py](file:///d:/streamlit-gdp-dashboard/create_template.py)
- **pyproject.toml テンプレート**: `dependencies` に `"pyinstaller>=6.21.0"` を追加。
- **.gitignore テンプレート**: ビルド出力物が Git に混入するのを防ぐため、`build/`, `dist/`, `*.spec` を追加。
- **app.py テンプレート**: EXE（frozen状態）として実行されている場合は実行ファイルと同じフォルダの `.env` を読み込み、スクリプト実行の場合はスクリプトと同じフォルダの `.env` を読み込むよう動的ロードに修正。
- **launcher.py (新規テンプレートファイル)**: Streamlit をプログラムから起動し、ブラウザを自動で開くためのランチャースクリプトを生成対象に追加。
- **build.bat (新規テンプレートファイル)**: PyInstaller を使用して、コンソール非表示（`--windowed`）、フォルダ出力（`--onedir`）、ライブラリ同梱のビルドを行うバッチファイルを生成対象に追加。
- **README.md テンプレート**: EXE化ビルドの手順およびビルド後の `.env` 配置についてドキュメントを追記。
- **完了メッセージ**: テンプレート生成成功時のコンソール出力に、EXE化の手順を追加。

---

### 2. メインのGDPダッシュボードプロジェクト (`D:\streamlit-gdp-dashboard`)

#### [MODIFY] [pyproject.toml](file:///d:/streamlit-gdp-dashboard/pyproject.toml)
- `dependencies` に `"openpyxl>=3.1.0"` を追加。

#### [MODIFY] [views/sidebar.py](file:///d:/streamlit-gdp-dashboard/views/sidebar.py)
- サイドバーに「📁 ローカルデータ」のセクションを追加し、期間選択スライダー（2010〜2025年）と「🔌 ローカルデータ読込」ボタンを配置。

#### [MODIFY] [views/__init__.py](file:///d:/streamlit-gdp-dashboard/views/__init__.py)
- 新規追加する `render_local_csv`, `render_local_excel`, `render_local_sqlite` をエクスポート。

#### [MODIFY] [launcher.py](file:///d:/streamlit-gdp-dashboard/launcher.py)
- PyInstaller の静的解析で新規追加するデータ取得層やビュー層のモジュールが漏れないよう、`if False:` ブロック内にインポート文を追加（`data.local_csv`, `views.local_csv_tab` など）。

#### [MODIFY] [build.bat](file:///d:/streamlit-gdp-dashboard/build.bat)
- 新規追加したモジュール群を PyInstaller ビルド時に同梱するための `--hidden-import` オプションの追加。

#### [NEW] [generate_dummy_data.py](file:///d:/streamlit-gdp-dashboard/generate_dummy_data.py)
- 2010〜2025年の各国ダミーGDPデータを生成し、`data/dummy/` ディレクトリ配下に以下の3つの形式で出力するスクリプトを作成：
  - CSV (`data/dummy/gdp_data.csv`)：カナダ、ブラジル、韓国のデータ
  - Excel (`data/dummy/gdp_data.xlsx`)：オーストラリア、インド、ドイツのデータ
  - SQLite (`data/dummy/gdp_data.sqlite`)：イギリス、フランス、イタリアのデータ（`gdp_data` テーブル）

#### [NEW] [data/local_csv.py](file:///d:/streamlit-gdp-dashboard/data/local_csv.py)
- Pandas を使用して `gdp_data.csv` を読み込み、カラム名を日本語（国、年、GDP (USD)）に統一するデータ取得関数を定義。

#### [NEW] [data/local_excel.py](file:///d:/streamlit-gdp-dashboard/data/local_excel.py)
- Pandas を使用して `gdp_data.xlsx` の `"GDP Data"` シートを読み込み、カラム名を統一するデータ取得関数を定義。

#### [NEW] [data/local_sqlite.py](file:///d:/streamlit-gdp-dashboard/data/local_sqlite.py)
- `sqlite3` と Pandas を使用して `gdp_data.sqlite` からクエリを実行し、カラム名を統一するデータ取得関数を定義。

#### [MODIFY] [data/__init__.py](file:///d:/streamlit-gdp-dashboard/data/__init__.py)
- 新規作成したローカルデータ読み込み関数 `fetch_local_csv`, `fetch_local_excel`, `fetch_local_sqlite` をエクスポート。

#### [NEW] [views/local_csv_tab.py](file:///d:/streamlit-gdp-dashboard/views/local_csv_tab.py)
- 最新の主要指標メトリクス、Plotlyによる積層エリアチャート (`px.area`)、生データテーブルを表示するCSVダッシュボード画面を定義。

#### [NEW] [views/local_excel_tab.py](file:///d:/streamlit-gdp-dashboard/views/local_excel_tab.py)
- 最新の主要指標メトリクス、Plotlyによる折れ線グラフ (`px.line`)、生データテーブルを表示するExcelダッシュボード画面を定義。

#### [NEW] [views/local_sqlite_tab.py](file:///d:/streamlit-gdp-dashboard/views/local_sqlite_tab.py)
- 最新の主要指標メトリクス、Plotlyによる棒グラフ (`px.bar`)、生データテーブルを表示するSQLiteダッシュボード画面を定義。

#### [MODIFY] [app.py](file:///d:/streamlit-gdp-dashboard/app.py)
- サイドバーからの入力を受け取り、ダミーデータが不足している場合は `generate_dummy_data.py` を呼び出して自動生成。
- 取得したデータをセッション状態に保存し、期間スライダーによる動的フィルタリングを適用。
- 「📁 CSVデータ (ローカル)」「🗄️ SQLiteデータ (ローカル)」「📊 Excelデータ (ローカル)」の3つの新規タブを追加して描画処理を呼び出し。

---

## 検証計画

### 自動検証
1. `uv sync` を実行して、`openpyxl` を含めた仮想環境を構築・同期。
2. `python generate_dummy_data.py` を手動実行し、`data/dummy/` に3ファイルが正しく作成されるか確認。
3. `uv run streamlit run app.py` を実行してブラウザで動作確認。
4. `python create_template.py test_app` を実行し、生成された `D:\test_app` に適切な `pyproject.toml`, `launcher.py`, `build.bat`, `app.py` などが含まれているか確認。
5. メインアプリの `build.bat` を実行し、エラーなく PyInstaller のEXEビルドが完了することを確認。

### 手動検証
1. ダッシュボードをブラウザで開き、新たに追加されたCSV、SQLite、Excel用のタブを表示する。
2. 「🔌 ローカルデータ読込」をクリックし、それぞれのタブで対応する国々（カナダ/ブラジル/韓国、イギリス/フランス/イタリア、オーストラリア/インド/ドイツ）のデータが正しくグラフとテーブルで表示されるか確認。
3. スライダー操作により、グラフに表示される期間が動的に切り替わることを確認。
4. ビルドされた `dist\GDP_Dashboard\GDP_Dashboard.exe` をダブルクリックし、コンソール画面なしで起動し、ブラウザで全ての機能（ローカルデータ読込含む）が正しく動作することを確認。
