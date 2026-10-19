# Reproducibility

Install with `python -m pip install -e '.[api,test]'`. Use seeded `study-sentinel demo --out demo-study --n 300 --seed 42`. Run `study-sentinel analyze --manifest demo-study/study.json --csv demo-study/synthetic_study.csv --out reports`. The JSON report contains the source CSV SHA-256 and analysis seed. Python dependency versions are constrained but not lockfile-pinned; cross-environment byte-identical output is not guaranteed. The scientific demo is synthetic and not a real patient or participant sample. Never interpret generated p-values as empirical evidence.
