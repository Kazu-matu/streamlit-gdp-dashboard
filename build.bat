@echo off
chcp 65001 > nul
echo ============================================
echo  GDP Dashboard - PyInstaller Build Script
echo ============================================

echo [1/3] Cleaning previous build...
if exist build  rmdir /s /q build
if exist dist   rmdir /s /q dist

echo [2/3] Running PyInstaller...
uv run pyinstaller ^
  --name "GDP_Dashboard" ^
  --onefile ^
  --windowed ^
  --add-data "app.py;." ^
  --add-data "config.py;." ^
  --add-data "logger_config.py;." ^
  --add-data "generate_dummy_data.py;." ^
  --add-data "pages;pages" ^
  --add-data "data;data" ^
  --add-data "views;views" ^
  --add-data ".venv\Lib\site-packages\streamlit;streamlit" ^
  --add-data ".venv\Lib\site-packages\plotly;plotly" ^
  --hidden-import streamlit ^
  --hidden-import pandas ^
  --hidden-import requests ^
  --hidden-import plotly ^
  --hidden-import dotenv ^
  --hidden-import config ^
  --hidden-import logger_config ^
  --hidden-import data.worldbank ^
  --hidden-import data.fred ^
  --hidden-import data.estat ^
  --hidden-import data.local_csv ^
  --hidden-import data.local_excel ^
  --hidden-import data.local_sqlite ^
  --hidden-import views.page_config ^
  --hidden-import views.sidebar ^
  --hidden-import views.components ^
  --hidden-import views.worldbank_tab ^
  --hidden-import views.imf_tab ^
  --hidden-import views.japan_tab ^
  --hidden-import views.local_csv_tab ^
  --hidden-import views.local_excel_tab ^
  --hidden-import views.local_sqlite_tab ^
  --hidden-import streamlit.web.cli ^
  --hidden-import streamlit.runtime.scriptrunner ^
  --hidden-import streamlit.runtime.caching ^
  --collect-all streamlit ^
  --collect-all plotly ^
  launcher.py

echo [3/3] Done!
echo.
echo Output: dist\GDP_Dashboard\GDP_Dashboard.exe
echo.
pause
