"""
logger_config.py — アプリ全体のロギングを設定するモジュール。
"""
import sys
import logging
from pathlib import Path

def setup_logging():
    """ロギングシステムをセットアップする。

    標準エラー出力と `app.log` の両方に出力する。
    EXE起動時は、実行ファイル本体と同階層に `app.log` を配置する。
    """
    root_logger = logging.getLogger()
    
    # 既にハンドラが定義済みの場合は再設定をスキップ
    if root_logger.handlers:
        return
        
    if getattr(sys, "frozen", False):
        log_dir = Path(sys.executable).parent
    else:
        log_dir = Path(__file__).parent
        
    log_file = log_dir / "app.log"
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    
    root_logger.setLevel(logging.INFO)
    
    # 1. コンソール出力 (標準エラー)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # 2. ファイル出力 (UTF-8)
    try:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(log_format)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        logging.getLogger("logger_config").info(f"Logging initialized. File: {log_file}")
    except Exception as exc:
        logging.getLogger("logger_config").warning(f"Failed to initialize file logging: {exc}")
