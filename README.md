# P5B2 revision reproduction package v1.3.0
Core consumer-level analysis: tested from the archived original split CSV copies, not a fresh public download. Obtain data from https://github.com/fenglixu/RecoGCN; prepare train_sample.csv, test_sample.csv, val_sample.csv with user_id, agent_id, item_id columns. No third-party data are distributed here. Preserve repeated records.

Install: python -m pip install -r core/requirements.txt
Run: python run.py /path/to/split_csv_directory
Outputs are generated locally in core/; do not redistribute generated transaction or consumer-level CSVs without authorization. verify.py checks the frozen aggregate results.

Legacy scripts are retained as historical assets, not part of the verified entry point. They may require path fixes, additional inputs and dependencies. Full historical table/figure reproduction is not certified. Historical figures outside the unified workflow are not certified. Fixed-reference CR1 does not include reference re-estimation uncertainty.

For local H5 extraction see data_access/README.md. Python 3.13.5 was used for verification.

## v1.3.0
The unified entry point now additionally runs core/contrast.py and core/verify_contrast.py. It verifies all six slopes, component CR1 standard errors, normal intervals and two-sided p-values against frozen aggregate targets (absolute tolerance 1e-12). The paired cluster-score and covariance identities are checked. Table S16 is covered; Table S17 is regenerated from the split CSVs by sensitivity/recompute.py, preserving historical train–validation–test contributor order. All 10 perturbations and four amplitudes are checked against archived targets (absolute tolerance 1e-10). The unified entry point also generates the coefficient plot in PNG (600 dpi), SVG and PDF. See sensitivity/README.md. Previous published version: https://doi.org/10.5281/zenodo.24542520. No new DOI is asserted until publication.

Checkpoint recovery: rerun the same command after interruption. Verified sensitivity aggregates are cached locally in sensitivity/.checkpoint.json, bound to hashes of inputs, code and frozen targets. Delete that file for a fresh sensitivity run. The checkpoint is not distributed. Final verification used a resumed run with exit code 0.
