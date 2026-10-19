"""Generated teaching data. No real participants."""
import numpy as np
import pandas as pd
def simulate(*,n:int=300,seed:int=42,missing:float=.06)->pd.DataFrame:
    if not 20<=n<=100000: raise ValueError("n outside [20,100000]")
    if not 0<=missing<.6: raise ValueError("missing outside [0,.6)")
    rng=np.random.default_rng(seed)
    age=np.clip(rng.normal(34,11,n),18,80)
    stress=rng.normal(size=n)
    sleep=7.4-.6*stress+rng.normal(0,.9,n)
    well=52-4.2*stress+1.6*(sleep-7.4)+rng.normal(0,6,n)
    items={}
    for i in range(1,6):
        values=np.clip(np.rint(3+( -.8 if i==3 else .8)*stress+rng.normal(0,.85,n)),1,5).astype(float)
        values[rng.random(n)<missing]=np.nan
        items[f"stress_{i}"]=values
    return pd.DataFrame({"participant_id":[f"P{i:06d}" for i in range(n)],
        "age":age,"sleep_hours":sleep,"wellbeing":well,**items})
