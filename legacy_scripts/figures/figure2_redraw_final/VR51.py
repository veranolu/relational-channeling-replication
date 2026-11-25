# Figure 2 (VR47B) 关系集中度双联图 —— 可复现绘图脚本
# 原始数据: /mnt/agents/upload/full_686k_triplets_excel.csv (686,246 行; user_id/agent_id/item_id)
# 公式: s_ua = n_ua / sum_a n_ua; HHI(u) = sum_a s_ua^2; top-share(u) = max_a s_ua
# 运行: python3 figure2_redraw_final.py  -> figure2_redraw.png (3000x1260 @400dpi)
import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# 与交付环境一致的网格设置（沙箱 rcParams 默认）
plt.rcParams.update({'axes.grid': True, 'axes.facecolor': '#FEFEFE',
                     'grid.color': '#E8E8E8', 'grid.alpha': 0.6, 'grid.linewidth': 0.8})

df = pd.read_csv('/mnt/agents/upload/full_686k_triplets_excel.csv')
g = df.groupby(['user_id','agent_id']).size().rename('n').reset_index()
tot = g.groupby('user_id')['n'].sum().rename('tot')
g = g.merge(tot, on='user_id'); g['s'] = g['n']/g['tot']
hhi = g.groupby('user_id')['s'].apply(lambda x:(x**2).sum())
top = g.groupby('user_id')['s'].max()
nag = g.groupby('user_id').size()
multi_vals = hhi[nag>1].values
sv = np.sort(top.values); cdf = np.arange(1,len(sv)+1)/len(sv)*100

fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.15), dpi=400)
ax = axes[0]
bins = np.arange(0.10, 1.001, 0.05)
ax.hist(multi_vals, bins=bins, color='#1f6fb2', edgecolor='white', linewidth=0.4, zorder=3)
ax.bar(1.0, 75411, width=0.028, color='#c0392b', edgecolor='white', linewidth=0.4, zorder=3, align='center')
ax.annotate('atom at HHI = 1:\n75,411 consumers (86.6%)\nbuy from a single agent',
            xy=(1.0, 75411), xytext=(0.56, 66000), fontsize=7.6, color='#c0392b',
            ha='center', va='center', arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.9))
ax.text(0.42, 25000, 'multi-agent consumers\n(n = 11,694): observed\nHHI range 0.12–0.98\nmean HHI = 0.947 (all consumers)\nmedian HHI = 1.000',
        fontsize=7.2, color='#444444', ha='center', va='center', style='italic',
        bbox=dict(boxstyle='round,pad=0.35', fc='white', ec='#bbbbbb', lw=0.6))
ax.axvline(1.0, color='#999999', ls=':', lw=0.8, zorder=2)
ax.set_xlim(0.05, 1.09); ax.set_ylim(0, 86000)
ax.set_xlabel('Within-consumer agent HHI', fontsize=8.5)
ax.set_ylabel('Number of consumers', fontsize=8.5)
ax.set_title('(a) Concentration of purchases across agents', fontsize=9.0, pad=6)
ax.tick_params(labelsize=7.5)
ax.set_yticks([0,20000,40000,60000,80000]); ax.set_yticklabels(['0','20k','40k','60k','80k'])
for s in ['top','right']: ax.spines[s].set_visible(False)

ax = axes[1]
ax.step(sv, cdf, where='post', color='#1f6fb2', lw=1.2, zorder=3)
ax.axvline(0.8, color='#999999', ls=':', lw=0.8, zorder=2)
ax.plot([0.8],[8.77],'o',ms=5,color='#c0392b',zorder=4)
ax.annotate('91.2% of consumers give\n≥80% of purchases to one agent',
            xy=(0.8, 8.8), xytext=(0.40, 30), fontsize=7.6, color='#c0392b',
            ha='center', va='center', arrowprops=dict(arrowstyle='->', color='#c0392b', lw=0.9))
ax.annotate('jump to 100%:\nsingle-agent atom (86.6%)',
            xy=(0.995, 97), xytext=(0.72, 66), fontsize=7.2, color='#444444',
            ha='center', va='center', style='italic',
            arrowprops=dict(arrowstyle='->', color='#777777', lw=0.8))
ax.set_xlim(0.15, 1.05); ax.set_ylim(0, 108)
ax.set_xlabel("Top-agent share of consumer's purchases", fontsize=8.5)
ax.set_ylabel('Cumulative share of consumers (%)', fontsize=8.5)
ax.set_title('(b) Top-agent share (ECDF)', fontsize=9.0, pad=6)
ax.tick_params(labelsize=7.5)
for s in ['top','right']: ax.spines[s].set_visible(False)
plt.tight_layout(w_pad=2.2)
plt.savefig('/mnt/agents/output/答辩留底_Figure回溯复现文档/VR51_figs/figure2_VR51.png', dpi=400, facecolor='white')
print('saved figure2_redraw.png')
