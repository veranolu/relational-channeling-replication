# -*- coding: utf-8 -*-
"""
VR37b S12 additions (expert batch c2-2):
  S12.2 LOPO-uniform support diagnostics + strict-LOPO coverage/entropy sensitivity
  S12.3 Agent-cluster bootstrap CIs for the four headline ratio-of-means estimands
Fidelity gates: recomputed point estimates must equal vr28b_pair_results anchors.
Input: raw triplets CSV (686,246 rows: user_id, agent_id, item_id).
Output: JSON alongside this script.
"""
import pandas as pd
import numpy as np
from scipy.special import gammaln
import json, time, datetime, os

t0 = time.time()
SCRIPT = "vr37b_s12_lopo_support_and_agent_cluster_bootstrap_20260908.py"
HERE = os.path.dirname(os.path.abspath(__file__))
TRIP = "/mnt/agents/upload/full_686k_triplets_excel.csv"
SEED = 42
B = 1000

df = pd.read_csv(TRIP)
n_in = len(df)
print(f"[{SCRIPT}] {datetime.datetime.now()} input triplets={n_in:,}", flush=True)

# ---------------- pair table ----------------
g = df.groupby(["user_id", "agent_id"])
pair = g.size().rename("g").reset_index()
pair["d"] = g["item_id"].nunique().values
cnt = df.groupby(["user_id", "agent_id", "item_id"]).size().rename("c").reset_index()
cnt["p"] = cnt["c"] / cnt.groupby(["user_id", "agent_id"])["c"].transform("sum")
H = cnt.groupby(["user_id", "agent_id"]).apply(
    lambda x: float(-(x["p"] * np.log(x["p"])).sum()), include_groups=False)
pair["H_obs"] = pair.set_index(["user_id", "agent_id"]).index.map(H).astype(float)
shelf = df.groupby("agent_id")["item_id"].nunique()
pair["n_s"] = pair["agent_id"].map(shelf).astype(int)
pair = pair.sort_values(["user_id", "agent_id"]).reset_index(drop=True)
N_pairs = len(pair)
assert N_pairs == 101577, N_pairs

pu = pair["user_id"].to_numpy(); pa = pair["agent_id"].to_numpy()
pg = pair["g"].to_numpy(); pns = pair["n_s"].to_numpy()
pd_ = pair["d"].to_numpy(); pH = pair["H_obs"].to_numpy()

# ---------------- f(g,p)=E[-(X/g)ln(X/g)], X~Bin(g,p) ----------------
def f_binom_rows(gs, ps):
    """vectorized over rows: gs int array, ps float array, same length."""
    out = np.zeros(len(ps))
    for gv in np.unique(gs):
        m = (gs == gv) & (ps > 0) & (ps < 1)  # p==1 contributes -(1)ln(1)=0 exactly
        if not m.any():
            continue
        pv = ps[m]
        lp = np.log(pv); lq = np.log1p(-pv)
        ks = np.arange(1, gv + 1, dtype=np.float64)
        t = (ks / gv) * np.log(ks / gv)
        logC = gammaln(gv + 1) - gammaln(ks + 1) - gammaln(gv - ks + 1)
        # (K rows) x (k terms) via broadcasting in chunks
        acc = np.zeros_like(pv)
        CH = 20000
        for s0 in range(0, len(pv), CH):
            sl = slice(s0, s0 + CH)
            # shape (chunk, k)
            M = np.exp(logC[None, :] + ks[None, :] * lp[sl, None] + (gv - ks[None, :]) * lq[sl, None])
            acc[sl] = -(M * t[None, :]).sum(axis=1)
        out[m] = acc
    return out

# ---------------- E_u uniform, cached on (g,n_s) ----------------
cache_u = {}
def eu_scalar(gv, nv):
    key = (int(gv), int(nv))
    v = cache_u.get(key)
    if v is None:
        v = 0.0 if (gv <= 1 or nv <= 1) else float(nv) * float(f_binom_rows(np.array([gv]), np.array([1.0 / nv]))[0])
        cache_u[key] = v
    return v
for gv, nv in np.unique(np.stack([pg, pns], axis=1), axis=0):
    eu_scalar(gv, nv)
E_u = np.array([cache_u[(int(a), int(b))] for a, b in zip(pg, pns)])
E_uniq = pns * (1.0 - (1.0 - 1.0 / pns) ** pg)
print(f"  pair table + E_u done ({time.time()-t0:.0f}s)", flush=True)

# ---------------- long table: pair x item with counts ----------------
# cnt: user_id, agent_id, item_id, c
ac = df.groupby(["agent_id", "item_id"]).size().rename("ac").reset_index()          # agent-item totals
gf = df.groupby("item_id").size().rename("gf").reset_index()                        # global item freq
agent_tot = df.groupby("agent_id").size().rename("at").reset_index()                # agent total purchases
cnt = cnt.merge(ac, on=["agent_id", "item_id"]).merge(gf, on="item_id")
cnt = cnt.merge(pair.reset_index()[["user_id", "agent_id", "index"]],
                on=["user_id", "agent_id"]).rename(columns={"index": "pidx"})
cnt["loo"] = cnt["ac"] - cnt["c"]          # other consumers' count (LOPO)

# benchmark supports = agent's FULL transaction-observed shelf: pair x shelf-item long table
pshelf = pair.reset_index()[["index", "agent_id", "g"]].rename(columns={"index": "pidx"})
pshelf = pshelf.merge(ac, on="agent_id")                       # rows = sum of n_s over pairs
pshelf = pshelf.merge(gf, on="item_id")
own = cnt[["pidx", "item_id", "c"]].rename(columns={"c": "own"})
pshelf = pshelf.merge(own, on=["pidx", "item_id"], how="left")
pshelf["own"] = pshelf["own"].fillna(0)
pshelf["loo"] = pshelf["ac"] - pshelf["own"]
pshelf["w_s"] = np.where(pshelf["loo"] > 0, pshelf["loo"], 0.0)
den_s = pshelf.groupby("pidx")["w_s"].transform("sum")
pshelf["p_s"] = np.where(den_s > 0, pshelf["w_s"] / den_s, 0.0)
pshelf["p_g"] = pshelf["gf"] / pshelf.groupby("pidx")["gf"].transform("sum")
print(f"  pair-shelf long table rows={len(pshelf):,} ({time.time()-t0:.0f}s)", flush=True)

E_s = np.zeros(N_pairs); E_g = np.zeros(N_pairs)
CHP = 2000000
for s0 in range(0, len(pshelf), CHP):
    sl = slice(s0, s0 + CHP)
    gg = pshelf["g"].to_numpy()[sl]
    fvals_s = f_binom_rows(gg, pshelf["p_s"].to_numpy()[sl])
    fvals_g = f_binom_rows(gg, pshelf["p_g"].to_numpy()[sl])
    np.add.at(E_s, pshelf["pidx"].to_numpy()[sl], fvals_s)
    np.add.at(E_g, pshelf["pidx"].to_numpy()[sl], fvals_g)
print(f"  E_s / E_g done ({time.time()-t0:.0f}s)", flush=True)

# ---------------- fidelity gates ----------------
g2 = pg >= 2
def rom(num, den, mask):
    return float(num[mask].sum() / den[mask].sum())
ANCH = dict(coverage_RoM_full=1.0289492218225114, uniform_RoM_g2=0.9940848304288114,
            popshelf_RoM_g2=1.029351469042679, popglobal_RoM_g2=1.8254654836209114)
got = dict(coverage_RoM_full=rom(pd_, E_uniq, np.ones(N_pairs, bool)),
           uniform_RoM_g2=rom(pH, E_u, g2),
           popshelf_RoM_g2=rom(pH, E_s, g2),
           popglobal_RoM_g2=rom(pH, E_g, g2))
for k in ANCH:
    ok = abs(got[k] - ANCH[k]) < 1e-9
    print(f"  GATE {k}: {got[k]:.10f} vs anchor {ANCH[k]:.10f} -> {'OK' if ok else 'FAIL'}", flush=True)
    assert ok, k

# ================= S12.2 LOPO-uniform support diagnostics =================
# LOPO support size from the FULL shelf long table (items bought by other consumers)
n_lo = pshelf.groupby("pidx").apply(lambda x: int((x["loo"] > 0).sum()), include_groups=False)
n_prime = np.zeros(N_pairs, dtype=np.int64); n_prime[n_lo.index.to_numpy()] = n_lo.to_numpy()
d_prime_c = cnt[cnt["loo"] > 0].groupby("pidx")["item_id"].nunique()
g_prime_c = cnt[cnt["loo"] > 0].groupby("pidx")["c"].sum()
d_prime = np.zeros(N_pairs, dtype=np.int64); d_prime[d_prime_c.index.to_numpy()] = d_prime_c.to_numpy()
g_prime = np.zeros(N_pairs, dtype=np.int64); g_prime[g_prime_c.index.to_numpy()] = g_prime_c.to_numpy()

elig = g2
supp_ratio = n_prime[elig] / pns[elig]
fully_cov = (d_prime[elig] == pd_[elig])
focal_only_items = int((cnt["loo"] == 0).sum()); focal_items_tot = len(cnt)
res_s122 = dict(
    N_pairs_eligible=int(elig.sum()),
    support_size_ratio_mean=float(supp_ratio.mean()),
    support_size_ratio_median=float(np.median(supp_ratio)),
    fully_covered_pairs_pct=float(100 * fully_cov.mean()),
    focal_only_pair_items=focal_only_items,
    focal_only_share_pct=float(100 * focal_only_items / focal_items_tot),
    pairs_with_any_focal_only_item=int(((cnt["loo"] == 0).groupby(cnt["pidx"]).any()).sum()),
    focal_items_with_support_pct=float(100 - 100 * focal_only_items / focal_items_tot),
)
# reconciliation with S10 headline: share of focal-pair items with outside support, multi-agent pairs only
nag = pair.groupby("user_id")["agent_id"].nunique()
multi_u = set(nag[nag >= 2].index)
mpidx = pair.index[pair["user_id"].isin(multi_u)]
cnt_multi = cnt[cnt["pidx"].isin(set(mpidx))]
res_s122["focal_items_with_support_pct_multiagent_pairs"] = float(100 * (cnt_multi["loo"] > 0).mean())

# strict-LOPO uniform coverage: d' vs E[K|g', n'] ; mask n'==0
m_cov = elig & (n_prime >= 1) & (g_prime >= 1)
E_K_lo = n_prime[m_cov] * (1.0 - (1.0 - 1.0 / n_prime[m_cov]) ** g_prime[m_cov])
cov_rom_strict = float(d_prime[m_cov].sum() / E_K_lo.sum())
cov_mor_strict = float(np.mean(d_prime[m_cov] / E_K_lo))
# strict-LOPO uniform entropy: H' of renormalized in-support counts vs E[H|g', n']
m_ent = elig & (n_prime >= 2) & (g_prime >= 2)
insp = cnt[cnt["loo"] > 0].copy()
insp["p_r"] = insp["c"] / insp.groupby("pidx")["c"].transform("sum")
Hprime = insp.groupby("pidx").apply(lambda x: float(-(x["p_r"] * np.log(x["p_r"])).sum()), include_groups=False)
Hp = np.zeros(N_pairs); Hp[Hprime.index.to_numpy()] = Hprime.to_numpy()
E_H_lo = np.array([eu_scalar(gv, nv) for gv, nv in zip(g_prime[m_ent], n_prime[m_ent])])
ent_rom_strict = float(Hp[m_ent].sum() / E_H_lo.sum())
ent_mor_strict = float(np.mean(Hp[m_ent] / np.where(E_H_lo > 0, E_H_lo, np.nan)))
res_s122.update(dict(
    strict_coverage_N=int(m_cov.sum()), strict_coverage_RoM=cov_rom_strict, strict_coverage_MoR=cov_mor_strict,
    strict_entropy_N=int(m_ent.sum()), strict_entropy_RoM=ent_rom_strict, strict_entropy_MoR=ent_mor_strict,
    orig_coverage_RoM_g2=rom(pd_, E_uniq, g2), orig_entropy_RoM_g2=got["uniform_RoM_g2"],
))
print("  S12.2:", json.dumps(res_s122, indent=1), flush=True)

# ================= S12.3 agent-cluster bootstrap =================
agents = np.sort(pair["agent_id"].unique())
nA = len(agents)
amap = np.zeros(agents.max() + 1, dtype=np.int64) - 1
amap[agents] = np.arange(nA)
paidx = amap[pa]
def aggA(w):
    out = np.zeros(nA)
    np.add.at(out, paidx, w)
    return out
specs = {
    "coverage_RoM_full": (aggA(pd_.astype(float)), aggA(E_uniq), np.ones(N_pairs, bool), got["coverage_RoM_full"], (1.027, 1.030)),
    "uniform_RoM_g2":    (aggA(np.where(g2, pH, 0.0)), aggA(np.where(g2, E_u, 0.0)), g2, got["uniform_RoM_g2"], (0.993, 0.995)),
    "popshelf_RoM_g2":   (aggA(np.where(g2, pH, 0.0)), aggA(np.where(g2, E_s, 0.0)), g2, got["popshelf_RoM_g2"], (1.028, 1.031)),
    "popglobal_RoM_g2":  (aggA(np.where(g2, pH, 0.0)), aggA(np.where(g2, E_g, 0.0)), g2, got["popglobal_RoM_g2"], (1.819, 1.832)),
}
rng = np.random.RandomState(SEED)
boots = {k: np.empty(B) for k in specs}
tb = time.time()
for b in range(B):
    sa = rng.randint(0, nA, size=nA)
    w = np.bincount(sa, minlength=nA).astype(float)
    for k, (num, den, _, _, _) in specs.items():
        boots[k][b] = (w @ num) / (w @ den)
print(f"  agent-cluster bootstrap done ({time.time()-tb:.0f}s)", flush=True)
res_s123 = {}
for k, (_, _, _, point, cci) in specs.items():
    lo, hi = np.percentile(boots[k], [2.5, 97.5])
    res_s123[k] = dict(point=point, consumer_boot_CI=list(cci),
                       agent_cluster_boot_CI=[float(lo), float(hi)])
    print(f"  {k}: point={point:.4f} consumerCI={cci} agentCI=[{lo:.4f},{hi:.4f}]", flush=True)

R = dict(script=SCRIPT, seed=SEED, B=B, input_rows=n_in, elapsed_sec=time.time() - t0,
         gates=got, S12_2=res_s122, S12_3=res_s123)
out = os.path.join(HERE, "vr37b_s12_results_20260908.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2, default=float)
print(f"[{SCRIPT}] DONE -> {out} ({time.time()-t0:.0f}s)", flush=True)
