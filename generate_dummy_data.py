"""
generate_dummy_data.py — デモ用のダミーデータ（CSV, Excel, SQLite）を作成するスクリプト。
"""
import os
import pandas as pd
import sqlite3
from pathlib import Path

def generate_dummy_data(base_dir: Path | None = None):
    if base_dir is None:
        import sys
        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).parent
        else:
            base_dir = Path(__file__).parent
            
    dummy_dir = base_dir / "data" / "dummy"
    dummy_dir.mkdir(parents=True, exist_ok=True)

    
    # 1. CSVデータ生成 (カナダ, ブラジル, 韓国)
    csv_rows = []
    # カナダ
    for year in range(2010, 2026):
        val = 1.6e12 + (year - 2010) * 4.5e10 + (year % 3) * 1.5e10
        csv_rows.append({"Country": "カナダ", "Year": year, "GDP (USD)": val})
    # ブラジル
    for year in range(2010, 2026):
        val = 2.2e12 + (year - 2010) * 3.0e10 - (year % 2) * 5.0e10
        csv_rows.append({"Country": "ブラジル", "Year": year, "GDP (USD)": val})
    # 韓国
    for year in range(2010, 2026):
        val = 1.1e12 + (year - 2010) * 5.5e10 + (year % 4) * 2.0e10
        csv_rows.append({"Country": "韓国", "Year": year, "GDP (USD)": val})
        
    csv_df = pd.DataFrame(csv_rows)
    csv_path = dummy_dir / "gdp_data.csv"
    csv_df.to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Created CSV dummy data: {csv_path}")

    # 2. Excelデータ生成 (オーストラリア, インド, ドイツ)
    excel_rows = []
    # オーストラリア
    for year in range(2010, 2026):
        val = 1.1e12 + (year - 2010) * 4.0e10 + (year % 2) * 1.0e10
        excel_rows.append({"Country": "オーストラリア", "Year": year, "GDP (USD)": val})
    # インド
    for year in range(2010, 2026):
        val = 1.7e12 + (year - 2010) * 1.6e11 + (year % 3) * 3.0e10
        excel_rows.append({"Country": "インド", "Year": year, "GDP (USD)": val})
    # ドイツ
    for year in range(2010, 2026):
        val = 3.4e12 + (year - 2010) * 9.0e10 - (year % 2) * 2.0e10
        excel_rows.append({"Country": "ドイツ", "Year": year, "GDP (USD)": val})
        
    excel_df = pd.DataFrame(excel_rows)
    excel_path = dummy_dir / "gdp_data.xlsx"
    excel_df.to_excel(excel_path, index=False, sheet_name="GDP Data")
    print(f"Created Excel dummy data: {excel_path}")

    # 3. SQLiteデータ生成 (イギリス, フランス, イタリア)
    sqlite_path = dummy_dir / "gdp_data.sqlite"
    if sqlite_path.exists():
        try:
            sqlite_path.unlink()
        except OSError:
            pass
            
    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE gdp_data (
            country TEXT,
            year INTEGER,
            gdp_usd REAL
        )
    """)
    sqlite_rows = []
    # イギリス
    for year in range(2010, 2026):
        val = 2.4e12 + (year - 2010) * 5.0e10 + (year % 2) * 1.5e10
        sqlite_rows.append(("イギリス", year, val))
    # フランス
    for year in range(2010, 2026):
        val = 2.6e12 + (year - 2010) * 4.5e10 - (year % 3) * 1.0e10
        sqlite_rows.append(("フランス", year, val))
    # イタリア
    for year in range(2010, 2026):
        val = 2.1e12 + (year - 2010) * 2.5e10 + (year % 2) * 8.0e9
        sqlite_rows.append(("イタリア", year, val))
        
    cursor.executemany("INSERT INTO gdp_data VALUES (?, ?, ?)", sqlite_rows)
    conn.commit()
    conn.close()
    print(f"Created SQLite dummy database: {sqlite_path}")

if __name__ == "__main__":
    generate_dummy_data()
