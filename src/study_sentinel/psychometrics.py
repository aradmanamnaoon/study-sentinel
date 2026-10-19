"""Scale scoring and classical reliability estimators."""
import pandas as pd
from .contracts import Scale
from .errors import AnalysisError

def reverse_coded(df:pd.DataFrame, scale:Scale)->pd.DataFrame:
    items=df[list(scale.items)].copy()
    for item in scale.reverse: items[item]=scale.minimum+scale.maximum-items[item]
    return items

def score_scale(df:pd.DataFrame,scale:Scale)->pd.Series:
    items=reverse_coded(df,scale)
    scores=items.mean(axis=1).where(items.notna().sum(axis=1)>=scale.min_answered)
    scores.name=scale.name
    return scores

def cronbach_alpha(items:pd.DataFrame)->float:
    complete=items.dropna()
    k=len(complete.columns)
    if k<2 or len(complete)<3: raise AnalysisError("insufficient complete cases")
    variance=complete.sum(axis=1).var(ddof=1)
    if variance<=0: raise AnalysisError("no scale variance")
    return float(k/(k-1)*(1-complete.var(ddof=1).sum()/variance))

def reliability(df:pd.DataFrame,scale:Scale)->dict:
    items=reverse_coded(df,scale)
    try: alpha=cronbach_alpha(items)
    except AnalysisError: alpha=None
    scored=score_scale(df,scale)
    return {"scale":scale.name,"n_complete":int(items.notna().all(axis=1).sum()),
            "n_scored":int(scored.notna().sum()),"alpha":alpha,
            "mean_score":float(scored.mean()) if scored.notna().any() else None,
            "note":"Coefficient alpha is not evidence of unidimensionality or construct validity."}
