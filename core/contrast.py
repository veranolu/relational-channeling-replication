import numpy as np,pandas as pd,glob,json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from pathlib import Path
import sys
root=str(Path(sys.argv[1]).resolve())+'/'
u=pd.read_csv(root+'upstream.csv');u=u[u.n_agents>=2].copy();u['sbin']=pd.qcut(np.log(u.S_union),5,labels=False,duplicates='drop');u['stratum']=list(zip(u.n_purchases,u.n_agents,u.sbin));gr=u.groupby('stratum');keep=(gr.HHI.transform('size')>=8)&((gr.HHI.transform('max')-gr.HHI.transform('min'))>=.04);q=u.loc[keep].copy().reset_index(drop=True);assert len(q)==9095
ex=pd.read_csv(root+'G_exact_entropy_strict9095_v1.csv');q=q.merge(ex,on='consumer_id',validate='one_to_one',sort=False)
sc=pd.factorize(q.stratum.astype(str))[0];ns=np.bincount(sc);x=q.HHI.to_numpy();xd=x-np.bincount(sc,weights=x)[sc]/ns[sc];den=xd@xd
p=root+'transactions_pooled.csv.gz'
d=pd.read_csv(p,usecols=['consumer_id','agent_id']);ids=np.sort(d.consumer_id.unique());ags=np.sort(d.agent_id.unique());ui=np.searchsorted(ids,d.consumer_id.to_numpy());ai=np.searchsorted(ags,d.agent_id.to_numpy())+len(ids);adj=coo_matrix((np.ones(len(d)*2,dtype=np.uint8),(np.r_[ui,ai],np.r_[ai,ui])),shape=(len(ids)+len(ags),)*2).tocsr();nc,lab=connected_components(adj,directed=False);comp=lab[np.searchsorted(ids,q.consumer_id.to_numpy())];_,ci=np.unique(comp,return_inverse=True);G=ci.max()+1
out={'N':len(q),'strata':len(ns),'components_in_sample':int(G),'components_full_graph':int(nc),'largest_component_sample_n':int(np.bincount(ci).max()),'den':float(den),'methods':'within-stratum demeaned OLS; component-cluster CR1 sandwich; normal 1.96; fixed LOPO reference (no reference reestimation)'}
from scipy.stats import norm
Y={'observed':q.item_entropy.to_numpy(),'expected_uniform':q.E_exact_uniform.to_numpy(),'expected_local':q.E_exact_local.to_numpy()}
Y.update(uniform=Y['observed']-Y['expected_uniform'],local=Y['observed']-Y['expected_local'],contrast=Y['expected_uniform']-Y['expected_local'])
scores={}; results={}
factor=G/(G-1)*(len(q)-1)/(len(q)-len(ns)-1)/den**2
for name,y in Y.items():
 yd=y-np.bincount(sc,weights=y)[sc]/ns[sc]; b=xd@yd/den; score=np.bincount(ci,weights=xd*(yd-b*xd),minlength=G); scores[name]=score; se=np.sqrt(factor*(score@score)); results[name]={'beta':float(b),'se':float(se),'ci':[float(b-1.96*se),float(b+1.96*se)],'p':float(2*norm.sf(abs(b/se)))}
np.testing.assert_allclose(scores['contrast'],scores['local']-scores['uniform'],atol=1e-12)
np.testing.assert_allclose(results['contrast']['beta'],results['local']['beta']-results['uniform']['beta'],atol=1e-12)
np.testing.assert_allclose(results['contrast']['se']**2,results['local']['se']**2+results['uniform']['se']**2-2*factor*(scores['local']@scores['uniform']),atol=1e-12)
for mode in ['uniform','local']:
 np.testing.assert_allclose(results[mode]['beta'],results['observed']['beta']-results['expected_'+mode]['beta'],atol=1e-12)
out['results']=results
print(json.dumps(out,indent=2)); Path(root+'contrast_actual.json').write_text(json.dumps(out,indent=2))
