# Figure 1 (VR47B) 研究设计总览图 —— 可复现绘图脚本
# 数据：全部为 VR47B 冻结真值（见回溯文档 Figure1 部分），无随机数
# 运行：python3 figure1_redraw_final.py  → 输出 figure1_redraw_v4.png (3000x1720 @400dpi)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BLUE='#1f6fb2'; GREEN='#2e8540'; AMBER='#b25e09'; INK='#16324f'; GREY='#444444'
fig, ax = plt.subplots(figsize=(7.5,4.3), dpi=400)   # 真尺寸：文档最终显示 7.5x4.3 英寸
ax.set_xlim(0,100); ax.set_ylim(0,64); ax.axis('off')

def box(x,y,w,h,fc,ec,lw=1.0,rs=0.6):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f"round,pad=0,rounding_size={rs}",fc=fc,ec=ec,lw=lw,zorder=2))
def txt(x,y,s,size,color=INK,weight='normal',ha='center',va='center',style='normal',z=5,**kw):
    ax.text(x,y,s,fontsize=size,color=color,fontweight=weight,ha=ha,va=va,style=style,zorder=z,**kw)

# 顶带：竞争性预测（Section 4 裁决）
box(1,57.0,98,6.6,'#fdf6e3','#8a7a1a',1.4)
txt(50,62.2,'COMPETING PREDICTIONS — adjudicated in Section 4',9.8,'#8a7a1a','bold')
box(2.5,57.4,44,3.9,'white','#8a7a1a',1.0)
txt(25,59.9,'Assortment-ceiling account: shelf capacity caps diversity',7.8,INK)
txt(25,58.3,'⇒ static ceiling-normalized ratio ≪ 1 ("narrowing")',7.6,GREY)
txt(48.6,59.3,'vs.',8.5,'#8a7a1a','bold',style='italic')
box(52,57.4,45.5,3.9,'white','#8a7a1a',1.0)
txt(74.75,59.9,'Purchase-count account: finite draws explain the shortfall',7.8,INK)
txt(74.75,58.3,'⇒ ratio ≈ 1 once benchmarks match purchase counts',7.6,GREY)

colw=[22,23,31,19]; xs=[1,24.25,48.5,80.75]
heads=[('1. DATA',BLUE),('2. MEASUREMENT',BLUE),('3. ANALYSIS & BENCHMARKS',GREEN),('4. SYNTHESIS (§5)',AMBER)]
hb=[('#eaf3fb',BLUE),('#eaf3fb',BLUE),('#edf7ee',GREEN),('#fdf1e3',AMBER)]
for (h,c),x,w,(fc,ec) in zip(heads,xs,colw,hb):
    box(x,53.6,w,2.6,fc,ec,1.2); txt(x+w/2,54.9,h,9.0,ec,'bold')
    box(x,4.0,w,48.6,fc,ec,1.0,rs=0.9)
# 列1 DATA（冻结计数：686,246 triples; 87,105/13,508/60,562; 101,577 pairs）
x=xs[0]; cx=x+colw[0]/2
txt(cx,49.0,'686,246',15,BLUE,'bold'); txt(cx,46.6,'purchase triples',9.0,INK,'bold')
txt(cx,42.3,'87,105 consumers\n13,508 selling agents\n60,562 purchased items',8.0,GREY,linespacing=1.5)
box(x+1.5,32.6,colw[0]-3,6.6,'white',BLUE,1.0)
txt(cx,37.7,'user–agent–item',8.6,INK,'bold'); txt(cx,35.9,'released transactions',7.8,GREY); txt(cx,34.2,'Aug–Nov 2018',7.8,GREY)
box(x+1.5,24.4,colw[0]-3,6.6,'white',BLUE,1.0)
txt(cx,29.5,'101,577',10.5,BLUE,'bold'); txt(cx,27.2,'consumer–agent pairs',7.8,GREY)
txt(cx,18.2,'Zenodo-archived scripts\n+ user-level table',7.8,GREY)
txt(cx,9.8,'every number\nrecomputable',7.8,GREY,style='italic')
# 列2 MEASUREMENT
x=xs[1]; cx=x+colw[1]/2
chips=[('Coverage  K','unique items purchased',44.6),('Entropy  H','Shannon, nats — Eq. (1)',38.2),
       ('Cross-agent HHI','lock-in (descriptive)',31.8),('Cross-agent overlap','shared-item incidence',25.4)]
for t1,t2,y in chips:
    box(x+1.5,y,colw[1]-3,5.2,'white',BLUE,1.0)
    txt(cx,y+3.4,t1,8.8,INK,'bold'); txt(cx,y+1.5,t2,7.8,GREY)
txt(cx,20.4,'Finite-draw benchmarks\nclosed form, Eqs. (3)–(4)\nMonte-Carlo verified',7.8,INK)
box(x+1.5,6.0,colw[1]-3,5.6,'white',BLUE,1.0)
txt(cx,10.0,'Audit trail (Table 5)',8.6,BLUE,'bold'); txt(cx,7.9,'10-stage pipeline',7.8,GREY)
# 列3 ANALYSIS（RQ 标签+章节/表锚点）
x=xs[2]; w=colw[2]
rqs=[('RQ1','Relational concentration','§4.1 · Table 6 · Fig. 2',44.6,False),
     ('RQ2','Shelf size & realized\ndiversity','§4.2 · Table 7',38.0,True),
     ('RQ3','Coverage vs. evenness','§4.3 · Table 8 · Figs. 3–4',31.2,False),
     ('RQ4','Cross-agent redundancy','§4.4 · Table 9',24.8,False)]
for rq,lab,ref,y,two in rqs:
    box(x+1.2,y,6.8,4.6,GREEN,GREEN,1.0)
    txt(x+4.6,y+2.3,rq,8.8,'white','bold')
    if two:
        txt(x+8.8,y+3.35,lab,7.9,INK,ha='left',linespacing=1.12); txt(x+8.8,y+0.55,ref,7.2,GREY,ha='left')
    else:
        txt(x+8.8,y+3.1,lab,7.9,INK,ha='left'); txt(x+8.8,y+1.2,ref,7.2,GREY,ha='left')
txt(x+w/2,18.4,'Each RQ: one unit of analysis,\none measure, one benchmark',7.8,GREY,style='italic')
txt(x+w/2,11.0,'Robustness: consumer-level aggregation\n+ LOPO (Appendices A–B)',7.8,GREY)
# 列4 SYNTHESIS
x=xs[3]; cx=x+colw[3]/2
box(x+1.0,36.6,colw[3]-2,9.6,'white',AMBER,1.0)
txt(cx,43.6,'Typology of',8.2,AMBER,'bold'); txt(cx,41.9,'intermediation',8.2,AMBER,'bold')
txt(cx,40.2,'architectures',8.2,AMBER,'bold'); txt(cx,38.3,'(§5.1)',7.4,GREY)
box(x+1.0,22.6,colw[3]-2,10.6,'white',AMBER,1.0)
txt(cx,30.6,'RCF provisional',8.2,AMBER,'bold'); txt(cx,28.9,'framework from',8.2,AMBER,'bold')
txt(cx,27.2,'documented',8.2,AMBER,'bold'); txt(cx,25.5,'regularities',8.2,AMBER,'bold'); txt(cx,23.7,'(§5.2)',7.4,GREY)
txt(cx,17.4,'➜ detailed in Figure 5',8.0,AMBER,'bold')
txt(cx,11.2,'Epistemic status of\nevery claim: Table 12',7.8,GREY)
for x0,x1 in [(23.2,24.05),(47.45,48.3),(79.7,80.55)]:
    ax.add_patch(FancyArrowPatch((x0,28),(x1,28),arrowstyle='-|>',mutation_scale=14,color='#555555',lw=1.4,zorder=6))
plt.subplots_adjust(left=0.005,right=0.995,top=0.995,bottom=0.005)
plt.savefig('figure1_redraw_v4.png',dpi=400,facecolor='white')
print('saved figure1_redraw_v4.png')
