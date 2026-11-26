"""Publication coefficient plot from verified aggregate results."""
import json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
root=Path(__file__).resolve().parent
r=json.loads((root/'contrast_actual.json').read_text())['results']; out=Path(sys.argv[1]) if len(sys.argv)>1 else root.parent/'figures';out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'svg.fonttype':'none','axes.unicode_minus':True})
fig,axes=plt.subplots(2,1,figsize=(7.1,4.8),sharex=True); fig.subplots_adjust(left=.30,right=.96,top=.92,bottom=.13,hspace=.48)
for ax,heading,keys,labels in zip(axes,['(a) Observed and reference-expected entropy','(b) Adjusted entropy and paired contrast'],[['observed','expected_uniform','expected_local'],['uniform','local','contrast']],[['Observed','Uniform expected','Local expected'],['Uniform adjusted','Local adjusted','Local − Uniform']]):
 ax.set_title(heading,loc='left',fontsize=10,fontweight='bold',pad=10); ax.axvline(0,color='.35',ls='--',lw=.9); ax.set_yticks([2,1,0],labels);ax.set_ylim(-.65,2.65);ax.set_xlim(-.31,.19);ax.xaxis.set_major_locator(MultipleLocator(.1));ax.grid(axis='x',alpha=.18);ax.set_axisbelow(True)
 for y,k,c,m in zip([2,1,0],keys,['#505050','#0072B2','#009E73'] if keys[0]=='observed' else ['#0072B2','#009E73','#A65E00'],(['o','s','D'] if keys[0]=='observed' else ['s','D','^'])):
  b=r[k]['beta'];lo,hi=r[k]['ci'];ax.errorbar(b,y,xerr=[[b-lo],[hi-b]],fmt=m,color=c,capsize=3,markersize=5,lw=1.5);ax.annotate(f'{b:+.4f}'.replace('-','−'),(b,y),xytext=(0,9),textcoords='offset points',ha='center',fontsize=8,color=c)
 for spine in ['top','right','left']:ax.spines[spine].set_visible(False)
 ax.tick_params(axis='y',length=0);ax.tick_params(axis='x',labelbottom=True)
axes[-1].set_xlabel('HHI slope (nats per unit HHI)');fig.text(.30,.025,'Points: estimates; bars: 95% component-clustered CR1 intervals.',fontsize=8)
for ext in ['png','svg','pdf']:fig.savefig(out/f'HHI_slope_decomposition.{ext}',dpi=600,facecolor='white')
