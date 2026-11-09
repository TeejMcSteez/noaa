import hashlib
import os

import pandas
import duckdb

def get_bulk_data(url: str ) -> pandas.DataFrame:
    duckdb.sql("SET s3_endpoint='storage.googlesapis.com'")

    query = duckdb.sql(f"""SELECT * FROM read_parquet('{url}')""")
    assert query is not None
    return query.to_df()

def get_data(path: str | None) -> pandas.DataFrame | FileNotFoundError:
    """
    Uses pandas read csv to read file from cwd/arg
    """
    cwd = os.getcwd()
    current_path = ""
    if path:
        current_path = f"{cwd}/{path}"
    else:
        raise FileNotFoundError
    return pandas.read_csv(current_path)


def assign_split(key: str, train=0.8, val=0.1) -> str:
    h = int(hashlib.md5(key.encode()).hexdigest(), 16) % 10_000 / 10_000
    return "train" if h < train else "val" if h < train + val else "test"


def md5(s: str) -> str:
    return hashlib.md5(s.encode()).hexdigest()[:12]


def norm_text(s: pandas.Series) -> pandas.Series:
    return s.fillna("").str.lower().str.replace(r"\s+", " ", regex=True).str.strip()
