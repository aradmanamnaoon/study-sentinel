# Study Sentinel

Offline-first behavioral research audit workbench: validate study contracts, inspect missingness, score scales, estimate reliability and associations, and produce source-hashed aggregate reports.

> **Status:** prototype, not clinical software or causal inference. The 10,000-source-line target is not met.

## Quickstart

```bash
python -m pip install -e '.[api,test]'
study-sentinel demo --out demo-study --n 300 --seed 42
study-sentinel analyze --manifest demo-study/study.json --csv demo-study/synthetic_study.csv --out study-report
python -m pytest -q
```

All example data are synthetic. See the documentation and build log for limitations.