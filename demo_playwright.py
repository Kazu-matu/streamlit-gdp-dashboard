"""
GDP ダッシュボード — Playwright 自動デモ & 録画スクリプト
========================================================
Streamlit アプリ (localhost:8501) を Playwright で自動操作し、
デモの様子を動画（WebM）として録画します。

前提:
    1. Streamlit アプリが起動済み (http://localhost:8501)
    2. Playwright ブラウザがインストール済み
       (初回は `playwright install chromium` を実行)

実行方法:
    uv run --with playwright demo_playwright.py

出力:
    recordings/ ディレクトリに動画ファイルが保存されます。
"""

from __future__ import annotations

import time
from pathlib import Path

from playwright.sync_api import sync_playwright, Page, expect


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Configuration
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APP_URL = "http://localhost:8501"
RECORDING_DIR = Path(__file__).parent
VIEWPORT_W = 1920
VIEWPORT_H = 1080
SLOW_MO = 300  # ms — 操作間のディレイ（デモを見やすくする）


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Helper Functions
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def wait_for_streamlit(page: Page, timeout: int = 30_000) -> None:
    """Streamlit のメインコンテンツが完全にロードされるまで待つ。"""
    page.wait_for_selector(
        "[data-testid='stAppViewContainer']",
        state="visible",
        timeout=timeout,
    )
    # Streamlit の初期レンダリング完了を待つ
    time.sleep(2)


def wait_for_chart_render(page: Page, seconds: float = 4.0) -> None:
    """Plotly チャートのレンダリング完了を待つ。"""
    try:
        page.wait_for_selector(".js-plotly-plot", state="visible", timeout=15_000)
    except Exception:
        pass
    time.sleep(seconds)


def smooth_scroll(page: Page, target_y: int, steps: int = 10) -> None:
    """スムーズスクロールを実行する（デモ映え用）。"""
    page.evaluate(
        f"""
        (async () => {{
            const mainArea = document.querySelector('[data-testid="stAppViewContainer"]')
                          || document.querySelector('section.main')
                          || document.documentElement;
            const scrollEl = mainArea.querySelector('[data-testid="stVerticalBlockBorderWrapper"]')
                           ? mainArea
                           : document.documentElement;

            // Use smooth scroll
            window.scrollTo({{ top: {target_y}, behavior: 'smooth' }});
        }})();
        """
    )
    time.sleep(1.5)


def click_sidebar_button(page: Page, index: int = 0) -> None:
    """サイドバー内の「データ取得」ボタンをクリックする。

    Args:
        page: Playwright Page オブジェクト。
        index: ボタンのインデックス（0: 世界銀行, 1: IMF）。
    """
    sidebar = page.locator('[data-testid="stSidebar"]')
    buttons = sidebar.locator('button:has-text("データ取得")')
    buttons.nth(index).click()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Demo Scenario
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def run_demo(page: Page) -> None:
    """デモシナリオを実行する。

    1. アプリを開く
    2. 世界銀行 GDP データを取得 → グラフ・テーブル表示
    3. IMF GDP 成長率データを取得 → グラフ・テーブル表示
    4. 各要素をゆっくりスクロールして見せる
    """
    print("🚀 [1/8] アプリを開きます...")
    page.goto(APP_URL)
    wait_for_streamlit(page)
    time.sleep(2)

    # ── Step 2: 世界銀行 データ取得 ──
    print("🌍 [2/8] 世界銀行 GDP — データ取得ボタンをクリック...")
    click_sidebar_button(page, index=0)
    wait_for_chart_render(page, seconds=6)

    # ── Step 3: メトリクス & グラフを閲覧 ──
    print("📊 [3/8] 世界銀行 GDP — グラフを表示中...")
    smooth_scroll(page, 300)
    time.sleep(2)
    smooth_scroll(page, 600)
    time.sleep(2)

    # ── Step 4: 生データ表を開く ──
    print("📋 [4/8] 世界銀行 GDP — 生データテーブルを展開...")
    try:
        expander = page.locator('text=生データを表示').first
        expander.click()
        time.sleep(2)
        smooth_scroll(page, 900)
        time.sleep(2)
    except Exception:
        print("  ⚠️ エクスパンダーが見つかりませんでした。スキップします。")

    # ── Step 5: トップに戻る ──
    print("⬆️  [5/8] ページトップに戻ります...")
    smooth_scroll(page, 0)
    time.sleep(1.5)

    # ── Step 6: IMF タブに切り替え ──
    print("📈 [6/8] IMF タブに切り替え...")
    imf_tab = page.locator('button[role="tab"]:has-text("IMF")')
    imf_tab.click()
    time.sleep(1.5)

    # ── Step 7: サイドバーをスクロールして IMF データ取得 ──
    print("📈 [7/8] IMF GDP 成長率 — データ取得ボタンをクリック...")
    # サイドバーをスクロールして IMF ボタンを表示
    sidebar = page.locator('[data-testid="stSidebar"]')
    sidebar_inner = sidebar.locator('[data-testid="stSidebarContent"]').first
    try:
        sidebar_inner.evaluate("el => el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })")
    except Exception:
        sidebar.evaluate("el => el.scrollTo({ top: el.scrollHeight, behavior: 'smooth' })")
    time.sleep(1)

    click_sidebar_button(page, index=1)
    wait_for_chart_render(page, seconds=8)

    # ── Step 8: IMF グラフ・テーブル閲覧 ──
    print("📊 [8/8] IMF GDP 成長率 — グラフとデータを表示中...")
    smooth_scroll(page, 300)
    time.sleep(2)
    smooth_scroll(page, 600)
    time.sleep(2)

    # 生データ表を開く
    try:
        expander = page.locator('text=生データを表示').first
        if expander.is_visible():
            expander.click()
            time.sleep(2)
            smooth_scroll(page, 900)
            time.sleep(2)
    except Exception:
        pass

    # 最後にトップに戻る
    smooth_scroll(page, 0)
    time.sleep(2)

    print("✅ デモ完了！")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Main
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def main() -> None:
    """Playwright でデモを実行し、動画として録画する。"""
    RECORDING_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("  GDP ダッシュボード — Playwright 自動デモ & 録画")
    print("=" * 60)
    print(f"  🎬 録画先: {RECORDING_DIR.resolve()}")
    print(f"  🌐 対象URL: {APP_URL}")
    print(f"  📐 解像度: {VIEWPORT_W}x{VIEWPORT_H}")
    print("=" * 60)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=False,
            slow_mo=SLOW_MO,
        )
        context = browser.new_context(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            record_video_dir=str(RECORDING_DIR),
            record_video_size={"width": VIEWPORT_W, "height": VIEWPORT_H},
            locale="ja-JP",
        )
        page = context.new_page()

        try:
            run_demo(page)
        except Exception as exc:
            print(f"❌ エラーが発生しました: {exc}")
            import traceback
            traceback.print_exc()
        finally:
            # コンテキストを閉じることで録画が保存される
            context.close()
            browser.close()

    # 録画ファイルを表示
    video_files = list(RECORDING_DIR.glob("*.webm"))
    if video_files:
        latest = max(video_files, key=lambda f: f.stat().st_mtime)
        print(f"\n🎬 録画ファイル: {latest.resolve()}")
        print(f"   サイズ: {latest.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print("\n⚠️ 録画ファイルが見つかりませんでした。")

    print("\n🏁 完了！")


if __name__ == "__main__":
    main()
