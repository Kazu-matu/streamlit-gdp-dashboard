"""
launcher.py – EXE 起動ラッパー（bootstrap.run 直接呼び出し版）
"""
import sys
import os
import time
import socket
import threading
import webbrowser

PORT = 8501
URL  = f"http://localhost:{PORT}"


def find_app_py() -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "app.py")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")


import logging

logger = logging.getLogger("launcher")


def wait_for_server(host: str = "localhost", port: int = PORT, timeout: float = 30.0):
    """ポートが開くまで待機してからブラウザを開く"""
    logger.info(f"Port listener thread started. Waiting for {host}:{port}...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                logger.info(f"Server detected on port {port}. Triggering default browser to: {URL}")
                webbrowser.open(URL)
                return
        except OSError:
            time.sleep(0.3)
    logger.warning("Server startup check timed out. Attempting to open browser anyway.")
    webbrowser.open(URL)  # タイムアウトしても一応開く


if __name__ == "__main__":
    from logger_config import setup_logging
    setup_logging()
    
    logger.info("Starting execution of launcher...")
    app_path = find_app_py()
    logger.info(f"Resolved app.py path: {app_path}")

    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "false"
    os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"

    threading.Thread(target=wait_for_server, daemon=True).start()

    logger.info("Starting Streamlit programmatic bootstrap run...")
    from streamlit.web import bootstrap
    flag_options = {
        "server.port": PORT,
        "server.headless": True,
        "server.enableCORS": False,
        "server.enableXsrfProtection": False,
        "browser.gatherUsageStats": False,
        "global.developmentMode": False,
    }
    bootstrap.load_config_options(flag_options)
    bootstrap.run(
        main_script_path=app_path,
        is_hello=False,
        args=[],
        flag_options=flag_options,
    )


# PyInstaller 静的解析用のダミーインポート
if False:
    import app
    import config
    import data.worldbank
    import data.fred
    import data.estat
    import views.page_config
    import views.sidebar
    import views.components
    import views.worldbank_tab
    import views.imf_tab
    import views.japan_tab
    import data.local_csv
    import data.local_excel
    import data.local_sqlite
    import views.local_csv_tab
    import views.local_excel_tab
    import views.local_sqlite_tab

