# P5B2 revision reproduction package v1.2.0
Core consumer-level analysis: tested from the archived original split CSV copies, not a fresh public download. Obtain data from https://github.com/fenglixu/RecoGCN; prepare train_sample.csv, test_sample.csv, val_sample.csv with user_id, agent_id, item_id columns. No third-party data are distributed here. Preserve repeated records.

Install: python -m pip install -r core/requirements.txt
Run: python run.py /path/to/split_csv_directory
Outputs are generated locally in core/; do not redistribute generated transaction or consumer-level CSVs without authorization. verify.py checks the frozen aggregate results.

Legacy scripts are retained as historical assets, not part of the verified entry point. They may require path fixes, additional inputs and dependencies. Full historical table/figure reproduction is not certified. Figure 3 was manually drawn. Fixed-reference CR1 does not include reference re-estimation uncertainty.

For local H5 extraction see data_access/README.md. Python 3.13.5 was used for verification.

## Published Release and Citation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24542520.svg)](https://doi.org/10.5281/zenodo.24542520)

Version 1.2.0 is the officially published replication package for the revised manuscript submitted to *Information*. The core numerical pipeline was rerun using archived copies of the original transaction-data splits. A fresh upstream H5 download was not independently tested for this release.

- **GitHub Release:** https://github.com/veranolu/relational-channeling-replication/releases/tag/v1.2.0
- **Version DOI:** https://doi.org/10.5281/zenodo.24542520
- **Concept DOI:** https://doi.org/10.5281/zenodo.22928747

For reproducibility and citation, please use the version-specific DOI for v1.2.0. Earlier versions remain available for historical traceability.
