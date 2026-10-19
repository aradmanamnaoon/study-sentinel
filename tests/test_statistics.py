import numpy as np
import pandas as pd
import pytest
from study_sentinel.statistics import pearson,ols,permutation_correlation
from study_sentinel.psychometrics import cronbach_alpha,score_scale
from study_sentinel.contracts import Scale
from study_sentinel.errors import AnalysisError

def test_pearson_perfect():
    data=pd.DataFrame({"x":[1,2,3,4,5],"y":[2,4,6,8,10]})
    assert pearson(data,"x","y")["r"]==pytest.approx(1)
def test_ols_exact_with_noise():
    rng=np.random.default_rng(7)
    x=rng.normal(size=100)
    y=2+3*x+rng.normal(0,.2,size=len(x))
    data=pd.DataFrame({"x":x,"y":y})
    assert ols(data,"y",["x"])["coefficients"]["x"]["estimate"]==pytest.approx(3,abs=.1)
def test_permutation_seeded():
    data=pd.DataFrame({"x":np.arange(40),"y":np.arange(40)[::-1]})
    a=permutation_correlation(data,"x","y",seed=11,repeats=100)
    assert a==permutation_correlation(data,"x","y",seed=11,repeats=100)
def test_zero_variance():
    with pytest.raises(AnalysisError): pearson(pd.DataFrame({"x":[1]*6,"y":range(6)}),"x","y")
def test_reversed_scale():
    frame=pd.DataFrame({"a":[1,2,3],"b":[5,4,3]})
    score=score_scale(frame,Scale("s",("a","b"),("b",)))
    assert score.tolist()==pytest.approx([1,2,3])
def test_alpha():
    data=pd.DataFrame({"a":[1,2,3,4,5],"b":[1,2,3,4,5]})
    assert cronbach_alpha(data)==pytest.approx(1)
