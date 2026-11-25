# P5B2 revision reproduction package v1.2.0
Core consumer-level analysis: tested from the archived original split CSV copies, not a fresh public download. Obtain data from https://github.com/fenglixu/RecoGCN; prepare train_sample.csv, test_sample.csv, val_sample.csv with user_id, agent_id, item_id columns. No third-party data are distributed here. Preserve repeated records.

Install: python -m pip install -r core/requirements.txt
Run: python run.py /path/to/split_csv_directory
Outputs are generated locally in core/; do not redistribute generated transaction or consumer-level CSVs without authorization. verify.py checks the frozen aggregate results.

Legacy scripts are retained as historical assets, not part of the verified entry point. They may require path fixes, additional inputs and dependencies. Full historical table/figure reproduction is not certified. Figure 3 was manually drawn. Fixed-reference CR1 does not include reference re-estimation uncertainty.

For local H5 extraction see data_access/README.md. Python 3.13.5 was used for verification.

Version 1.2.0 is a GitHub release candidate based on the archived v1.1.0 (https://doi.org/10.5281/zenodo.24530007). The core numerical pipeline is unchanged and was rerun from archived split CSVs. A fresh upstream H5 download remains unverified. The final release DOI will be assigned after publication.
