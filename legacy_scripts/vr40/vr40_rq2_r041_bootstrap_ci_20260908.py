# -*- coding: utf-8 -*-
"""VR40: consumer-level bootstrap CI for the shelf-size/entropy Pearson correlation (main text Section 4.2, r = 0.41).
Resampling unit: consumer (all pairs of a resampled consumer are kept together). B = 1,000, seed 42, percentile method.
Input: full_686k_triplets.csv (columns: user_id, agent_id, item_id) — the concatenation of the three released RecoGCN splits.
"""
import numpy as np, pandas as pd
from collections import Counter
from scipy import stats as sps

df = pd.read_csv("full_686k_triplets.csv")
df.columns = ["user_id", "agent_id", "item_id"]
assert (len(df), df.user_id.nunique(), df.agent_id.nunique(), df.item_id.nunique()) == (686246, 87105, 13508, 60562)

pi = df.groupby(["user_id", "agent_id"])["item_id"].apply(list)
ug = list(pi.index)
pa = np.array([k[1] for k in ug]); pu = np.array([k[0] for k in ug])
shelf = df.groupby("agent_id")["item_id"].nunique()
pns = shelf.loc[pa].values.astype(float)
H = np.zeros(len(ug))
for i, its in enumerate(pi):
    c = np.array(list(Counter(its).values()), dtype=float); p = c / c.sum(); H[i] = -(p * np.log(p)).sum()

print("r (all pairs, N = %d) = %.4f" % (len(ug), sps.pearsonr(pns, H)[0]))
rng = np.random.default_rng(42)
uc = np.unique(pu)
upos = {u: np.where(pu == u)[0] for u in uc}
B = 1000; rs = np.empty(B)
for b in range(B):
    idx = np.concatenate([upos[u] for u in rng.choice(uc, size=len(uc), replace=True)])
    rs[b] = np.corrcoef(pns[idx], H[idx])[0, 1]
lo, hi = np.percentile(rs, [2.5, 97.5])
print("95%% consumer-level bootstrap CI = [%.4f, %.4f] -> reported [0.40, 0.41]" % (lo, hi))
assert round(lo, 2) == 0.40 and round(hi, 2) == 0.41
