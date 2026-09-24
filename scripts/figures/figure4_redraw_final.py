# figure4_redraw_final.py — Figure 4 redraw script (legacy version, see README note)
# data freeze source: stratum_summary.csv (5 purchase-frequency bins)
# cross-validation source: batch3_fig3_pair_distribution.csv (86,710 pairs)
# R_u = H_obs / E_uniform (有限抽样均匀基准下的均匀度比值); CI 为 bootstrap 95% CI (冻结值)
# 复现: 沙箱 IPython 内核 exec 逐像素一致; 裸 python3 因字体栈差异为视觉等价
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family':'DejaVu Sans','axes.grid':True,'axes.facecolor':'#FEFEFE',
    'grid.color':'#E8E8E8','grid.alpha':0.6,'grid.linewidth':0.8,
    'axes.axisbelow':True,'figure.facecolor':'white'})

BLUE='#1f77b4'; DARK='#333333'; RED='#B22222'; GRAY='#666666'

bins_lbl=['2','3–5','6–10','11–50','51+']
N_all=[9670,30945,29702,16063,330]
means=[0.9036,0.9712,0.9995,1.0098,0.9978]
ci_lo=[0.8955,0.9686,0.9977,1.0075,0.9823]
ci_hi=[0.9113,0.9737,1.0013,1.0119,1.0121]

fig,ax=plt.subplots(figsize=(7.5,3.8),dpi=400)
x=np.arange(5)
ax.bar(x,means,width=0.62,color=BLUE,edgecolor='none',zorder=3)
ax.errorbar(x,means,yerr=[np.array(means)-np.array(ci_lo),np.array(ci_hi)-np.array(means)],
            fmt='none',ecolor=DARK,elinewidth=1.2,capsize=4,capthick=1.2,zorder=4)
ax.axhline(1.0,ls='--',lw=1.1,color=GRAY,zorder=2)
ax.text(4.55,1.135,'dashed line: parity (ratio = 1)',ha='right',va='top',
        fontsize=7.2,style='italic',color=GRAY,zorder=5)

for i,(m,lo,hi) in enumerate(zip(means,ci_lo,ci_hi)):
    ylab = 1.018 if i==1 else hi+0.012   # keep the 0.971 label clear of the parity line
    ax.text(i,ylab,f'{m:.3f}',ha='center',va='bottom',fontsize=8.8,
            fontweight='bold',color='#16324a',zorder=6)
    ax.text(i,m-0.045,f'[{lo:.3f}, {hi:.3f}]',ha='center',va='top',fontsize=6.4,
            color='white',zorder=6)

ax.annotate('only material deficit: same-item repurchases\n'
            '(1,385 of 9,670 two-purchase pairs, 14.3%,\n'
            'entropy ln 2 → 0)',
            xy=(-0.26,0.905),xytext=(-0.58,1.155),
            fontsize=6.8,color=RED,ha='left',va='top',linespacing=1.3,zorder=7,
            arrowprops=dict(arrowstyle='->',color=RED,lw=1.0,
                            connectionstyle='arc3,rad=0.12'))

ax.text(4,0.55,'n = 330 pairs\nwider interval',ha='center',va='center',
        fontsize=6.6,style='italic',color='white',linespacing=1.4,zorder=6)

ax.set_xticks(x)
ax.set_xticklabels([f'{b}\n(N = {n:,})' for b,n in zip(bins_lbl,N_all)],fontsize=7.6)
ax.set_xlim(-0.7,4.6); ax.set_ylim(0,1.18)
ax.set_yticks(np.arange(0,1.01,0.2))
ax.tick_params(axis='y',labelsize=7.6)
ax.set_xlabel('Purchases per consumer–agent pair',fontsize=8.4)
ax.set_ylabel('Mean evenness ratio vs. finite-draw uniform',fontsize=8.4)
for s in ['top','right']: ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig('/mnt/agents/output/VR47_work/figure4_redraw.png',dpi=400)
plt.close(fig)
print('figure4 saved')
