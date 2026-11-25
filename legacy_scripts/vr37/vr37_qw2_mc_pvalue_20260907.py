# -*- coding: utf-8 -*-
"""
VR37 QW2: null distribution of the SAMPLE-WIDE cross-agent overlap incidence
under LOPO uniform / popularity benchmarks, via per-replicate aggregation
across all 11,694 multi-agent consumers. B=1000, seed=42.
Observed incidence = 342/11,694 = 2.9246%.
Output: null mean/std, percentile of observed, one-sided p per mode.
Adapted from vr28b_mc_lopo_20260906.py (same RNG layout style).
"""
import pandas as pd
import numpy as np
import json, time, datetime

t0 = time.time()
SCRIPT = "vr37_qw2_mc_pvalue_20260907.py"
TRIP = "/mnt/agents/upload/full_686k_triplets_excel.csv"
SIX = "/mnt/agents/output/anonymous_repo_20260906/data/user_level_6vars_anonymized_87105.csv"
OUT = "/mnt/agents/output/anonymous_repo_20260906/scripts/vr37/vr37_qw2_mc_pvalue_20260907.json"
B = 1000
SEED = 42
OBS = 342 / 11694

df = pd.read_csv(TRIP)
six = pd.read_csv(SIX)
print(f"[{SCRIPT}] {datetime.datetime.now()} triplets={len(df):,} B={B} seed={SEED} obs={OBS:.6f}", flush=True)

# user_id in six is anonymized 0..N-1 row index order matching? -> derive multi-agent from triplets directly
uc = df.groupby("user_id")["agent_id"].nunique()
multi_users = set(uc[uc >= 2].index)
assert len(multi_users) == 11694, len(multi_users)

agent_item_cnt = df.groupby(["agent_id", "item_id"]).size()
agent_shelf_items = df.groupby("agent_id")["item_id"].unique().apply(np.sort)
pair_cnt = df.groupby(["user_id", "agent_id", "item_id"]).size()
pair_g = df.groupby(["user_id", "agent_id"]).size()

mdf = df[df["user_id"].isin(multi_users)]
pairs = list(mdf.groupby(["user_id", "agent_id"]).size().index)

pair_data = []
for (u, a) in pairs:
    items = agent_shelf_items[a]
    ac = agent_item_cnt.loc[a].reindex(items).to_numpy(dtype=np.float64)
    pc = np.array([pair_cnt.get((u, a, it), 0) for it in items], dtype=np.float64)
    loo = ac - pc
    pos = loo > 0
    li = items[pos]; lw = loo[pos]
    if len(li) == 0:  # LOPO empty: fall back to uniform over own shelf items
        li = items; lw = ac
    pair_data.append((u, li, lw, int(pair_g[(u, a)])))

from collections import defaultdict
cons_pairs = defaultdict(list)
for rec in pair_data:
    cons_pairs[rec[0]].append(rec)
consumers = sorted(cons_pairs.keys())
rng = np.random.default_rng(SEED)

def mc_consumer_indicators(recs, mode):
    """Return (B,) float indicator: 1 if any item drawn from >=2 sides in replicate b."""
    draws = []
    for (u, li, lw, g) in recs:
        if mode == "uni_lopo":
            items = li
            idx = rng.integers(0, len(items), size=(B, g))
        else:
            items = li
            cw = np.cumsum(lw)
            idx = np.searchsorted(cw, rng.random((B, g)) * cw[-1])
            idx = np.minimum(idx, len(items) - 1)
        draws.append(items[idx])
    m = len(draws)
    rep_list, item_list, side_list = [], [], []
    base = np.arange(B)
    for si, d in enumerate(draws):
        g = d.shape[1]
        rep_list.append(np.repeat(base, g))
        item_list.append(d.ravel())
        side_list.append(np.full(B * g, si, dtype=np.int64))
    rep = np.concatenate(rep_list); itm = np.concatenate(item_list); side = np.concatenate(side_list)
    order = np.lexsort((side, itm, rep))
    rep_s, itm_s, side_s = rep[order], itm[order], side[order]
    new_grp = np.ones(len(rep_s), dtype=bool)
    new_grp[1:] = (rep_s[1:] != rep_s[:-1]) | (itm_s[1:] != itm_s[:-1])
    grp_id = np.cumsum(new_grp) - 1
    side_diff = np.ones(len(rep_s), dtype=np.int64)
    side_diff[1:] = ((side_s[1:] != side_s[:-1]) | new_grp[1:]).astype(np.int64)
    sides_per_grp = np.bincount(grp_id, weights=side_diff)
    rep_of_grp = rep_s[new_grp]
    multi = sides_per_grp >= 2
    ov = np.zeros(B, dtype=np.float64)
    ov[np.unique(rep_of_grp[multi])] = 1.0
    return ov

R = {"observed_incidence": OBS, "B": B, "seed": SEED, "n_consumers": len(consumers)}
for mode in ["uni_lopo", "pop_lopo"]:
    mat = np.zeros((len(consumers), B), dtype=np.float64)
    for ci, u in enumerate(consumers):
        mat[ci] = mc_consumer_indicators(cons_pairs[u], mode)
        if (ci + 1) % 2000 == 0:
            print(f"  {mode} {ci+1:,}/{len(consumers):,} ({time.time()-t0:.0f}s)", flush=True)
    inc = mat.mean(axis=0)  # (B,) null sample-wide incidence
    R[f"{mode}_null_mean_pct"] = 100 * float(inc.mean())
    R[f"{mode}_null_sd_pct"] = 100 * float(inc.std(ddof=1))
    R[f"{mode}_null_q025_pct"] = 100 * float(np.quantile(inc, 0.025))
    R[f"{mode}_null_q975_pct"] = 100 * float(np.quantile(inc, 0.975))
    R[f"{mode}_p_ge_obs"] = float((inc >= OBS).mean())
    R[f"{mode}_p_le_obs"] = float((inc <= OBS).mean())
    R[f"{mode}_obs_percentile"] = float((inc < OBS).mean())
    print(mode, {k: round(v, 4) for k, v in R.items() if k.startswith(mode)}, flush=True)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2)
print(json.dumps(R, ensure_ascii=False, indent=2))
print(f"[{SCRIPT}] DONE ({time.time()-t0:.0f}s)", flush=True)
