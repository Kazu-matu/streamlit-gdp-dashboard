from .worldbank import fetch_wb_gdp, fetch_imf_gdp_growth
from .fred import fetch_fred_series
from .estat import fetch_estat_ci
from .local_csv import fetch_local_csv
from .local_excel import fetch_local_excel
from .local_sqlite import fetch_local_sqlite

__all__ = [
    "fetch_wb_gdp",
    "fetch_imf_gdp_growth",
    "fetch_fred_series",
    "fetch_estat_ci",
    "fetch_local_csv",
    "fetch_local_excel",
    "fetch_local_sqlite",
]

