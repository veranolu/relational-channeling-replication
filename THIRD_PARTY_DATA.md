# Third-Party Data Notice

## Upstream source

The analysis uses the experiment dataset associated with:

Fengli Xu, Jianxun Lian, Zhenyu Han, Yong Li, Yujian Xu, and Xing Xie. "Relation-Aware Graph Convolutional Networks for Agent-Initiated Social E-Commerce Recommendation." CIKM 2019, pp. 529–538. DOI: https://doi.org/10.1145/3357384.3357924

Upstream repository: https://github.com/fenglixu/RecoGCN

The upstream README provides the dataset download and requests citation when the code or dataset is used. It defines train, validation, and test samples as `[user, selling_agent, item]` triplets.

## Permission status

No explicit dataset license or redistribution grant was established in the audit on 2026-11-25. The upstream repository metadata reported no license, the root listing contained no license file, and the license endpoint returned no resource.

Therefore:

- Redistribution of the complete transaction triplets is **NOT CONFIRMED**.
- Redistribution of consumer-level or pair-level derivative tables is **NOT CONFIRMED** and also requires a separate privacy and authorization review.
- The MIT license in this package does not establish rights over third-party data.
- No raw transactions or identifier-bearing intermediate tables are included in this package.

This is an engineering permission boundary, not a legal opinion. Obtain explicit upstream permission before redistributing any third-party or derivative dataset.

## Local-access alternative

Use the original upstream access link, retain the required citation, and build inputs locally. See `data_access/README.md`. Local access does not by itself certify the scientific pipeline or authorize public redistribution.
