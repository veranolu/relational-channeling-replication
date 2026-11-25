# Figure 3 (VR47B) RQ3 零模型基准双联图 —— 可复现绘图脚本
# 原始数据: /mnt/agents/upload/vr30_fig3_plotarray_86710_20260906.csv
#   (86,710 对 g>=2 pairs; 列: pair_id, H_obs, H_unif, H_lopo, H_global)
#   该数组即 Table 5 stages 6-7 产出的 pair-level 数组（Table 8 同源）
# 公式: H_obs = -sum_i p_i ln p_i (Eq.1, 逐对购买份额);
#   H_unif = E[H|g,K_shelf] 均匀零模型闭式期望 (Eq.3);
#   H_lopo = E[H|g,shelf-popularity,leave-one-pair-out] (Eq.4);
#   deviation = H_obs - H_exp
# 运行: python3 figure3_redraw_final.py -> figure3_redraw.png (3000x1280 @400dpi)
import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'axes.grid': True, 'axes.facecolor': '#FEFEFE',
                     'grid.color': '#E8E8E8', 'grid.alpha': 0.6, 'grid.linewidth': 0.8})
BLUE='#1f6fb2'; GREEN='#2e8540'; GREY='#444444'; RED='#c0392b'
arr = pd.read_csv('/mnt/agents/upload/vr30_fig3_plotarray_86710_20260906.csv')
d_unif = (arr.H_obs - arr.H_unif).values
d_lopo = (arr.H_obs - arr.H_lopo).values

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.2), dpi=400)
ax = axes[0]
bins = np.arange(0, 5.01, 0.05)
ax.hist(arr.H_obs, bins=bins, density=True, color=BLUE, alpha=0.28, edgecolor='none', zorder=2)
ax.hist(arr.H_unif, bins=bins, density=True, histtype='step', color='#666666', ls='--', lw=1.1, zorder=3, label='Uniform null (1.687; 18.2% below)')
ax.hist(arr.H_lopo, bins=bins, density=True, histtype='step', color=GREEN, lw=1.3, zorder=4, label='Shelf-popularity LOPO (1.629; 15.7% below)')
ax.hist(arr.H_obs, bins=bins, density=True, histtype='step', color=BLUE, lw=1.3, zorder=5, label='Observed (mean 1.677)')
ax.set_xlim(0, 4.0); ax.set_ylim(0, 2.75)
ax.set_xlabel('Pair-level item entropy (nats)', fontsize=8.5)
ax.set_ylabel('Density across 86,710 pairs', fontsize=8.5)
ax.set_title('(a) Observed vs. null-model distributions', fontsize=9.0, pad=6)
ax.tick_params(labelsize=7.5)
ax.legend(fontsize=6.9, loc='upper right', frameon=True, edgecolor='#bbbbbb', framealpha=1.0, borderpad=0.5, labelspacing=0.35)
for s in ['top','right']: ax.spines[s].set_visible(False)

ax = axes[1]
dbins = np.arange(-2.0, 2.01, 0.04)
ax.hist(d_unif, bins=dbins, density=True, histtype='step', color='#666666', ls='--', lw=1.1, zorder=3,
        label='Observed − Uniform (mean Δ = −0.010)')
ax.hist(d_lopo, bins=dbins, density=True, histtype='step', color=GREEN, lw=1.3, zorder=4,
        label='Observed − LOPO (mean Δ = +0.048)')
ax.axvline(0, color=RED, lw=1.0, zorder=2)
ax.text(-0.15, 3.55, 'left of zero: observed below null', fontsize=7.0, color=RED, ha='right', va='center')
ax.text(-0.15, 3.10, '18.2% (Uniform) · 15.7% (LOPO)', fontsize=6.8, color=GREY, ha='right', va='center')
ax.set_xlim(-2.0, 2.0); ax.set_ylim(0, 7.0)
ax.set_xlabel('Pair-level entropy deviation (nats)', fontsize=8.5)
ax.set_ylabel('Density', fontsize=8.5)
ax.set_title('(b) Pair-level deviations from benchmarks', fontsize=9.0, pad=6)
ax.tick_params(labelsize=7.5)
ax.legend(fontsize=6.9, loc='upper right', frameon=True, edgecolor='#bbbbbb', framealpha=1.0, borderpad=0.5, labelspacing=0.35)
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout(w_pad=2.2)
plt.savefig('figure3_redraw.png', dpi=400, facecolor='white')
print('saved figure3_redraw.png')
