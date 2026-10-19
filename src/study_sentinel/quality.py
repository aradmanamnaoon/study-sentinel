"""Aggregate, identifier-free descriptive data checks."""
from dataclasses import dataclass,asdict
import pandas as pd
from .contracts import Study

@dataclass(frozen=True)
class ColumnQuality:
    name: str
    missing: int
    missing_rate: float
    distinct: int
    minimum: float | None
    maximum: float | None

def column_quality(df:pd.DataFrame,name:str)->ColumnQuality:
    s=df[name]
    v=s.dropna()
    return ColumnQuality(name,int(s.isna().sum()),float(s.isna().mean()),int(s.nunique(dropna=True)),
                         float(v.min()) if len(v) else None,float(v.max()) if len(v) else None)

def quality_report(df:pd.DataFrame,study:Study)->dict:
    cols=sorted(study.required_columns()-{study.id_column})
    return {"participants":len(df),"complete_cases":int(df[cols].notna().all(axis=1).sum()),
            "columns":[asdict(column_quality(df,x)) for x in cols],
            "note":"Missingness is descriptive; the missing-data mechanism cannot be identified from these summaries."}
