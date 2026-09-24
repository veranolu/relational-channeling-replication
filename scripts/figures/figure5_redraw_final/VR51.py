# figure5_redraw_final.py — Figure 5 (RCF framework) redraw script (legacy version, see README note)
# 性质: 概念框架图(非数据图); 框内统计数字全部为 §4.1–4.4 冻结值:
#  RQ1(Table 6): 86.6% single-agent; HHI mean 0.947; 88.2% top-share > 0.80
#  RQ2(Table 7): r = 0.41; tier mean ratios 0.968/0.999/0.988
#  RQ3(Table 8): coverage ratio 1.029; evenness 0.994 (uniform) / 1.017 (LOPO)
#  RQ4(Table 9): realized overlap 2.925% (uniform 2.095% / popularity 3.194%); agent-support overlap 50.5% (5,911/11,694)
# 复现: 沙箱 IPython 内核 exec 逐像素一致; 裸 python3 视觉等价(字体栈差异)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams.update({'font.family':'DejaVu Sans','figure.facecolor':'white','axes.grid':False})
BLUE='#1f77b4'; NAVY='#16324a'; LBLUE='#EAF2FA'; GRAY='#666666'; DGRAY='#444444'

fig,ax=plt.subplots(figsize=(7.5,4.8),dpi=400)
ax.set_xlim(0,100); ax.set_ylim(0,64); ax.axis('off')

def box(x,y,w,h,fc,ec,lw=1.4,ls='-',zd=2):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0,rounding_size=1.2',
                 fc=fc,ec=ec,lw=lw,linestyle=ls,zorder=zd))
def T(x,y,s,fs=8,c='black',w='normal',st='normal',ha='center',va='center',ls=1.25,zd=5):
    ax.text(x,y,s,fontsize=fs,color=c,fontweight=w,style=st,ha=ha,va=va,linespacing=ls,zorder=zd)

T(50,62.2,'Observed regularities (RQ1–RQ4)  vs.  untested propositions (P1–P3)',
  fs=10,st='italic',c=DGRAY)

rq=[('RQ1','Relational concentration',
     'Buyers return to a small set\nof socially tied agents',
     '86.6% single-agent\nHHI mean 0.947; 88.2% > 0.80'),
    ('RQ2','Shelf size and\nrealized diversity',
     'Larger shelves are associated\nwith higher realized entropy',
     'r = 0.41; tier ratios\n0.968 / 0.999 / 0.988'),
    ('RQ3','Coverage versus evenness',
     'No large average deficit\nunder purchase-count\nmatching',
     'coverage 1.029; evenness\n0.994 (unif.) / 1.017 (LOPO)'),
    ('RQ4','Cross-agent redundancy',
     'Low, between yet\ndistinguishable from\nboth LOPO nulls',
     'overlap 2.9% (bench. 2.1–3.2%)\nagent-support overlap 50.5%')]
xs=[0.5,25.5,50.5,75.5]; W=24; Y0=36; H=20
for (hdr,tit,desc,stat),x in zip(rq,xs):
    box(x,Y0,W,H,LBLUE,BLUE)
    cx=x+W/2
    T(cx,Y0+H-2.6,hdr,fs=9,c=BLUE,w='bold')
    T(cx,Y0+H-5.2,tit,fs=6.4,w='bold',c=NAVY,va='top')
    T(cx,Y0+H-10.0,desc,fs=6.0,c=DGRAY,va='top')
    T(cx,Y0+H-14.8,stat,fs=5.4,c=BLUE,w='bold',va='top')

box(24,15,52,11,NAVY,NAVY)
T(50,22.4,'Relational Assortment Channeling (RCF)',fs=9,c='white',w='bold')
T(50,18.4,'(provisional organizing framework)',fs=7.5,c='#CFE0EE')

entry=[34,44,56,66]
for x0,e in zip([x+W/2 for x in xs],entry):
    ax.add_patch(FancyArrowPatch((x0,Y0-0.4),(e,26.2),arrowstyle='-',
                 color=NAVY,lw=1.3,zorder=1))
ax.add_patch(FancyArrowPatch((50,14.6),(50,11.6),arrowstyle='-|>',mutation_scale=14,
             color=GRAY,lw=1.4,zorder=3))

box(17,1.2,66,10,'white',GRAY,lw=1.3,ls=(0,(5,3)))
T(50,8.6,'Untested: mechanisms (trust transfer, attention debt, switching costs)',fs=7.0,c=DGRAY)
T(50,5.9,'and propositions P1–P3  →  Table 11',fs=7.0,c=DGRAY)
T(50,3.1,'Box annotations report frozen values from Sections 4.1–4.4 (Tables 6–9)',
  fs=6.0,c=GRAY,st='italic')

fig.savefig('/mnt/agents/output/答辩留底_Figure回溯复现文档/VR51_figs/figure5_VR51.png',dpi=400)
plt.close(fig)
print('figure5 saved')
