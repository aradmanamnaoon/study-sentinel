"""Local-only optional FastAPI entry point; no filesystem upload endpoint."""
from __future__ import annotations
from fastapi import FastAPI
from pydantic import BaseModel, Field
from .simulation import simulate
from .quality import column_quality

app=FastAPI(title="Study Sentinel",description="Aggregate-only demo API for synthetic research data",version="0.1.0")

class DemoRequest(BaseModel):
    n:int=Field(default=300,ge=20,le=5000)
    seed:int=Field(default=42,ge=0,lt=2**32)

@app.get("/health")
def health()->dict:
    return {"status":"ok","mode":"local-demo"}

@app.post("/demo/summary")
def demo_summary(request:DemoRequest)->dict:
    frame=simulate(n=request.n,seed=request.seed)
    return {"synthetic":True,"participants":len(frame),
            "sleep_hours_mean":float(frame["sleep_hours"].mean()),
            "wellbeing_mean":float(frame["wellbeing"].mean()),
            "stress_item_missing":[{"item":f"stress_{i}","missing":column_quality(frame,f"stress_{i}").missing} for i in range(1,6)],
            "note":"Synthetic demonstration only; no clinical evidence."}
