# タスクリスト: EXE化対応およびマルチデータソースデモ機能

## 1. 依存関係とダミーデータの準備
- `[x]` `pyproject.toml` に `openpyxl` を追加し、`uv sync` で環境を更新
- `[x]` `generate_dummy_data.py` スクリプトを作成
- `[x]` `generate_dummy_data.py` を実行して、`data/dummy/` にダミーデータを作成

## 2. データ取得層 (data/) の実装
- `[x]` `data/local_csv.py` を作成（CSV読み込み）
- `[x]` `data/local_excel.py` を作成（Excel読み込み）
- `[x]` `data/local_sqlite.py` を作成（SQLite読み込み）
- `[x]` `data/__init__.py` に新規関数をエクスポート追加

## 3. UI 描画層 (views/) の実装
- `[x]` `views/local_csv_tab.py` を作成（エリアチャート可視化）
- `[x]` `views/local_excel_tab.py` を作成（折れ線グラフ可視化）
- `[x]` `views/local_sqlite_tab.py` を作成（棒グラフ可視化）
- `[x]` `views/__init__.py` に新規タブビューをエクスポート追加
- `[x]` `views/sidebar.py` にローカルデータ用UI（期間スライダーと読込ボタン）を追加


## 4. アプリケーション統合とビルド定義の更新
- `[x]` `app.py` にローカルデータ取得・キャッシュ・動的フィルタリング処理を追加し、3つの新規タブを配置
- `[x]` `launcher.py` に新規モジュールの静的インポートを追加
- `[x]` `build.bat` に新規モジュールの `--hidden-import` を追加

## 5. テンプレート生成スクリプトの改修
- `[x]` `create_template.py` をEXE化（PyInstaller依存関係、ランチャー、ビルドバッチ、README、完了通知）に対応するよう修正


## 6. 検証
- `[x]` ローカルサーバーを起動し、CSV/Excel/SQLiteタブが正常に動作し、期間スライダーで絞り込めるか確認
- `[x]` `build.bat` を実行し、生成された `dist\GDP_Dashboard\GDP_Dashboard.exe` が正常に動くか確認
- `[x]` `python create_template.py test_app` を実行し、生成されたテンプレートプロジェクトでEXEビルドができるか確認
- `[x]` 成果のウォークスルー文書 `walkthrough.md` を更新
