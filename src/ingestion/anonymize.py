import hashlib
import os

import pandas as pd


def _salt() -> str:
    salt = os.environ.get("BRONZE_HASH_SALT")
    if not salt:
        raise RuntimeError("BRONZE_HASH_SALT não definido — configure o .env antes de pseudonimizar.")
    return salt


def hash_value(value: str, salt: str) -> str | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    return hashlib.sha256(f"{salt}:{value}".encode("utf-8")).hexdigest()


def anonymize_dataframe(df: pd.DataFrame, hash_columns: list[str], drop_columns: list[str]) -> pd.DataFrame:
    salt = _salt()
    df = df.drop(columns=[c for c in drop_columns if c in df.columns])
    for col in hash_columns:
        if col in df.columns:
            df[col] = df[col].apply(lambda v: hash_value(v, salt))
    return df
