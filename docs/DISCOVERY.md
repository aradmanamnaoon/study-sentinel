# Flagship discovery and project selection

**Date:** 2026-10-19. This is a qualitative design exercise, not a peer-reviewed systematic review or verified market-demand survey.

## Candidate comparison

Weights: real researcher usefulness 25%, differentiation 15%, engineering/scientific rigor 20%, demo appeal 10%, adoption potential 15%, implementation feasibility on free local CPU 15%. Scores reflect hypotheses that require practitioner validation.

| Candidate | User and pain | Existing reference points | Differentiator and demo | Risks | Feasibility |
| --- | --- | --- | --- | --- | --- |
| Study Sentinel | Psychologists and behavioral scientists auditing survey CSVs before inferential statistics | [JASP](https://jasp-stats.org/), [jamovi](https://www.jamovi.org/), [Great Expectations](https://greatexpectations.io/) | Pre-analysis contracts, reverse-key provenance, missingness and statistical report tied to input digest; offline synthetic demonstration | Statistical overinterpretation, poorly documented instruments, leakage of personal data | CPU feasible |
| BrainBIDS Compass | Neuroimaging researchers with mislabelled modalities or subject/session metadata | [BIDS Validator](https://github.com/bids-standard/bids-validator), [Datalad](https://www.datalad.org/) | BIDS-to-model input readiness with suggested remediations and auditable input inventories | MRI data licensing, large file sizes, modality heterogeneity | Small public fixtures feasible |
| TrialTrace | Agent developers debugging evaluator leakage and unreliable judge outputs | [Inspect AI](https://inspect.aisi.org.uk/), [LangSmith](https://docs.smith.langchain.com/) | Multi-seed tool execution traces, adversarial contamination checks, judge calibration | Evaluation circularity, potentially high inference cost | Fake/recorded models on CPU |
| SensorSignal Bench | Physiological time-series analysts fighting invalid windows and mislabeled events | [MNE-Python](https://mne.tools/), [NeuroKit2](https://neuropsychology.github.io/NeuroKit/) | Data-quality-to-label-integrity audit of EDF/CSV before ML training | Hardware sampling differences, label ambiguity | Synthetic physiological signals feasible |
| SplitScope | ML practitioners encountering duplicate, group or temporal contamination | [skrub](https://skrub-data.org/), [scikit-learn](https://scikit-learn.org/) | Cross-split entity graph with counterfactual split repair reports | False positives and changing split semantics | CPU feasible |
| PipelineProof | Scientific Python teams unable to trace source data to reported plots | [DVC](https://dvc.org/), [MLflow](https://mlflow.org/) | Cryptographic evidence manifests and verification from inputs to public reports | Overlap with existing provenance tools, complex integration | CPU feasible |

## Why Study Sentinel

It offers the clearest end-to-end user journey on legitimately generated data: define study schema, validate observations, calculate descriptive and inferential checks, produce human and machine-readable outputs. Psychometric scoring and statistical assumptions remain explicit and inspectable.

The novelty claim is deliberately limited. Established statistical packages have far more mature estimation capabilities; this project focuses on an opinionated audit workflow. No measured superiority or demonstrated adoption is claimed.

## Free reproducible data

The `study-sentinel demo` command generates a seeded, artificial dataset with participant-like rows, five ordinal items, and continuous covariates/outcome. This teaching fixture is **not** an open population survey and does not support substantive scientific conclusions.

## Scientific reading and source provenance

- Wilkinson et al. (2016), FAIR Guiding Principles, [DOI 10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18)
- Poldrack et al. (2017), Toward open sharing of task-based fMRI data: BIDS, [DOI 10.1038/sdata.2016.44](https://doi.org/10.1038/sdata.2016.44)
- Cronbach (1951), Coefficient alpha and the internal structure of tests, [DOI 10.1007/BF02310555](https://doi.org/10.1007/BF02310555)
- White (1980), A heteroskedasticity-consistent covariance matrix estimator, [DOI 10.2307/1912934](https://doi.org/10.2307/1912934)

These links identify relevant prior work, not endorsements. Developer demand and maintenance maturity for this repository remain unmeasured.
