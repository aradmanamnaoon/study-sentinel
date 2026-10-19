"""Validated, size-constrained CSV ingestion."""
from pathlib import Path
import hashlib
import pandas as pd
import numpy as np
from .contracts import Study
from .errors import ValidationError

def file_digest(path: str | Path) -> str:
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def read_study(path: str | Path, study: Study, *, max_mb:int=100) -> pd.DataFrame:
    p=Path(path)
    if not p.is_file(): raise ValidationError("CSV not found")
    if p.suffix.lower()!=".csv": raise ValidationError("CSV required")
    if p.stat().st_size>max_mb*1024**2: raise ValidationError("CSV too large")
    try:
        df=pd.read_csv(p,dtype="string",keep_default_na=False,na_values=list(study.missing_tokens),encoding="utf-8-sig")
    except (OSError, ValueError, pd.errors.ParserError, UnicodeError) as exc:
        raise ValidationError(f"invalid CSV: {exc}") from exc
    if df.empty: raise ValidationError("zero rows")
    if not df.columns.is_unique: raise ValidationError("duplicate headers")
    absent=study.required_columns()-set(df.columns)
    if absent: raise ValidationError(f"missing columns: {sorted(absent)}")
    if df[study.id_column].isna().any() or df[study.id_column].duplicated().any():
        raise ValidationError("participant IDs must be unique and nonempty")
    for col in sorted(study.required_columns()-{study.id_column}):
        before=df[col]
        converted=pd.to_numeric(before,errors="coerce")
        if (converted.isna() & before.notna()).any():
            raise ValidationError(f"nonnumeric values in {col}")
        values=converted.to_numpy(dtype=float,na_value=np.nan)
        if np.isinf(values).any(): raise ValidationError(f"nonfinite values in {col}")
        df[col]=converted.astype(float)
    for s in study.scales:
        for item in s.items:
            if not df[item].dropna().between(s.minimum,s.maximum).all():
                raise ValidationError(f"{item} outside {s.name} range")
    return df
