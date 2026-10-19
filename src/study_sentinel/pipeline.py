"""End-to-end reproducible report generation."""
from pathlib import Path
from .contracts import Study
from .io import read_study,file_digest
from .quality import quality_report
from .psychometrics import reliability
from .statistics import pearson,ols,permutation_correlation
from .errors import AnalysisError

def run(study:Study,csv:str|Path,*,permutations:int=999)->dict:
    df=read_study(csv,study)
    result={"schema_version":"0.1","study":study.as_dict(),"input_sha256":file_digest(csv),
            "quality":quality_report(df,study),
            "reliability":[reliability(df,s) for s in study.scales],
            "disclaimer":"Only aggregate reports; synthetic demo is not scientific evidence."}
    for key,analysis in (
      ("correlation",lambda:pearson(df,study.exposure,study.outcome)),
      ("ols",lambda:ols(df,study.outcome,[study.exposure,*study.covariates])),
      ("permutation",lambda:permutation_correlation(df,study.exposure,study.outcome,seed=study.seed,repeats=permutations))):
        try: result[key]=analysis()
        except AnalysisError as exc: result[key]={"status":"unavailable","reason":str(exc)}
    return result
