from __future__ import annotations
import pandas as pd

def _norm_id(row) -> str:
    handle = (str(row.get("handle") or "")).strip()
    email  = (str(row.get("email") or "")).strip().lower()
    return handle if handle else email

def dedupe_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["__id"] = df.apply(_norm_id, axis=1)
    df = df.drop_duplicates(subset=["__id"], keep="first")
    return df.drop(columns=["__id"])
