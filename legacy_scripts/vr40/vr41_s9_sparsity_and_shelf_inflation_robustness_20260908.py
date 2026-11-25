# -*- coding: utf-8 -*-
"""VR41: S9 robustness — (a) exclude pairs with g<3; (b) inflate transaction-observed shelf by 20%.
Uniform-benchmark coverage and evenness ratios of means. Input: full_686k_triplets.csv (user_id, agent_id, item_id).
Anchor gates: full-sample coverage RoM = 1.0289492218225114; g>=2 & shelf>1 evenness RoM = 0.9940848304288114.
"""
import numpy as np, pandas as pd
from collections import Counter
from scipy.special import gammaln

df = pd.read_csv("full_686k_triplets.csv"); df.columns = ["u", "a", "i"]
pi = df.groupby(["u", "a"])["i"].apply(list)
ug = list(pi.index); pa = np.array([k[1] for k in ug])
shelf = df.groupby("a")["i"].nunique()
pns = shelf.loc[pa].values.astype(float)
pg = pi.apply(len).values.astype(float)
uniq = pi.apply(lambda s: len(set(s))).values.astype(float)
H = np.zeros(len(ug))
for j, its in enumerate(pi):
    c = np.array(list(Counter(its).values()), dtype=float); p = c / c.sum(); H[j] = -(p * np.log(p)).sum()

def Ecov(g, n): return n * (1 - (1 - 1 / n) ** g)
def EH(g, n):
    k = np.arange(0, g + 1)
    lg = gammaln(g + 1) - gammaln(k + 1) - gammaln(g - k + 1) + k * np.log(1 / n) + (g - k) * np.log(1 - 1 / n)
    pmf = np.exp(lg); pr = k / g
    return -n * np.sum(np.where(k > 0, pmf * pr * np.log(pr), 0.0))
Ecov_v = np.vectorize(Ecov); EH_v = np.vectorize(EH)

# anchor gates
ec = Ecov_v(pg, pns)
assert abs(uniq.mean() / ec.mean() - 1.0289492218225114) < 1e-9
mask = (pg >= 2) & (pns > 1)
eh = EH_v(pg[mask].astype(int), pns[mask])
assert abs(H[mask].mean() / eh.mean() - 0.9940848304288114) < 1e-9

# g distribution (pair level)
print("g percentiles P25/median/P75/P90:", np.percentile(pg, [25, 50, 75, 90]))

# (a) exclude g < 3
m3 = pg >= 3
print("g>=3 coverage RoM = %.4f (N=%d)" % (uniq[m3].mean() / Ecov_v(pg[m3], pns[m3]).mean(), m3.sum()))
m3e = (pg >= 3) & (pns > 1)
eh3 = EH_v(pg[m3e].astype(int), pns[m3e])
print("g>=3 evenness RoM = %.4f, MoR = %.4f (N=%d)" % (H[m3e].mean() / eh3.mean(), np.mean(H[m3e] / eh3), m3e.sum()))

# (b) shelf inflation +20%
print("inflate coverage RoM = %.4f" % (uniq.mean() / Ecov_v(pg, pns * 1.2).mean()))
ehi = EH_v(pg[mask].astype(int), pns[mask] * 1.2)
print("inflate evenness RoM = %.4f, MoR = %.4f" % (H[mask].mean() / ehi.mean(), np.mean(H[mask] / ehi)))
