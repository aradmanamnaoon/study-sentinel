"""Bivariate association, OLS with HC3 and seeded permutation null."""
import numpy as np
import pandas as pd
from scipy import stats
from .errors import AnalysisError

def pearson(df:pd.DataFrame,x:str,y:str)->dict:
    complete=df[[x,y]].dropna()
    if len(complete)<4: raise AnalysisError("at least four pairs required")
    a=complete[x].to_numpy(dtype=float)
    b=complete[y].to_numpy(dtype=float)
    if np.std(a)==0 or np.std(b)==0: raise AnalysisError("zero variation")
    result=stats.pearsonr(a,b)
    return {"n":len(complete),"r":float(result.statistic),"p_value":float(result.pvalue),
            "ci95":[float(z) for z in result.confidence_interval(.95)],
            "note":"Association does not establish causality."}

def ols(df:pd.DataFrame,outcome:str,predictors:list[str])->dict:
    if not predictors or len(set(predictors))!=len(predictors):
        raise AnalysisError("invalid predictors")
    complete=df[[outcome,*predictors]].dropna()
    n=len(complete)
    x=np.column_stack([np.ones(n),complete[predictors].to_numpy(dtype=float)])
    y=complete[outcome].to_numpy(dtype=float)
    p=x.shape[1]
    if n<=p+2: raise AnalysisError("insufficient residual degrees of freedom")
    if np.linalg.matrix_rank(x)<p: raise AnalysisError("singular design")
    beta=np.linalg.lstsq(x,y,rcond=None)[0]
    residual=y-x@beta
    mse=float(residual@residual/(n-p))
    ss=float(((y-y.mean())**2).sum())
    leverage=np.sum(x*(x@np.linalg.inv(x.T@x)),axis=1)
    if np.any(leverage>=1-1e-10): raise AnalysisError("HC3 undefined at leverage one")
    meat=(x*(residual/(1-leverage))[:,None]).T@(x*(residual/(1-leverage))[:,None])
    covariance=np.linalg.inv(x.T@x)@meat@np.linalg.inv(x.T@x)
    se=np.sqrt(np.maximum(np.diag(covariance),0))
    z=np.divide(beta,se,out=np.full_like(beta,np.nan),where=se>0)
    pvals=2*stats.norm.sf(np.abs(z))
    names=["intercept",*predictors]
    return {"n":n,"r_squared":1-float(residual@residual)/ss if ss>0 else None,
            "coefficients":{name:{"estimate":float(beta[i]),"se_hc3":float(se[i]),
                                "p_value_normal_approx":float(pvals[i])} for i,name in enumerate(names)},
            "note":"OLS is observational; HC3 robust SE and asymptotic normal inference."}

def permutation_correlation(df:pd.DataFrame,x:str,y:str,*,seed:int=42,repeats:int=999)->dict:
    if not 10<=repeats<=100000: raise AnalysisError("permutations must be from 10 to 100000")
    complete=df[[x,y]].dropna()
    a=complete[x].to_numpy(dtype=float)
    b=complete[y].to_numpy(dtype=float)
    if len(a)<4 or a.std()==0 or b.std()==0: raise AnalysisError("insufficient variation")
    observed=float(np.corrcoef(a,b)[0,1])
    rng=np.random.default_rng(seed)
    extreme=0
    for _ in range(repeats):
        perm=float(np.corrcoef(a,rng.permutation(b))[0,1])
        if abs(perm)>=abs(observed)-1e-12: extreme+=1
    return {"n":len(a),"r":observed,"repeats":repeats,"seed":seed,
            "p_two_sided":(extreme+1)/(repeats+1),
            "note":"Simple permutation test assumes exchangeable observations under the null."}
