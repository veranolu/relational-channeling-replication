import numpy as np,pandas as pd,glob,time
from scipy.stats import binom
import sys,json,hashlib,os
from pathlib import Path
base=Path(__file__).resolve().parent; root=str(base.parent/'core')+'/'; raw=Path(sys.argv[1]);t0=time.time()
u=pd.read_csv(root+'upstream.csv');u=u[u.n_agents>=2].copy();u['sbin']=pd.qcut(np.log(u.S_union),5,labels=False,duplicates='drop');u['stratum']=list(zip(u.n_purchases,u.n_agents,u.sbin));gr=u.groupby('stratum');keep=(gr.HHI.transform('size')>=8)&((gr.HHI.transform('max')-gr.HHI.transform('min'))>=.04);q=u.loc[keep].copy().reset_index(drop=True);assert len(q)==9095
sc=pd.factorize(q.stratum.astype(str))[0];ns=np.bincount(sc);x=q.HHI.to_numpy();xd=x-np.bincount(sc,weights=x)[sc]/ns[sc];den=xd@xd
obs=q.item_entropy.to_numpy();uids=q.consumer_id.to_numpy();d=pd.concat([pd.read_csv(raw/f'{s}_sample.csv').rename(columns={'user_id':'consumer_id'})[['consumer_id','agent_id','item_id']] for s in ('train','val','test')],ignore_index=True);v=d.groupby(['consumer_id','agent_id','item_id'],sort=False).size().reset_index(name='cnt');cons=pd.Index(d.consumer_id.unique());cid=pd.Series(np.arange(len(cons)),index=cons)
ad={};
for a,z in v.groupby('agent_id',sort=False):
 items,code=np.unique(z.item_id.to_numpy(np.int32),return_inverse=True);ad[int(a)]=(items,code,cid.loc[z.consumer_id].to_numpy(np.int32),z.cnt.to_numpy(float))
targets=[]
for uid,z in v[v.consumer_id.isin(uids)].groupby('consumer_id',sort=False):
 parts=[]
 for a,ga in z.groupby('agent_id',sort=False):
  items,code,contributors,counts=ad[int(a)];ix=np.flatnonzero(contributors==cid.loc[uid]);parts.append((int(a),int(ga.cnt.sum()),code[ix],counts[ix]))
 targets.append((int(uid),parts))
targets=dict(targets)
# prepare fixed support union and search locations for each consumer
prepared=[]
for uid in uids:
 parts=targets[int(uid)];allitems=np.unique(np.concatenate([ad[a][0] for a,k,code,counts in parts]));prepared.append((parts,allitems,[np.searchsorted(allitems,ad[a][0]) for a,k,code,counts in parts]))

def expectation(parts,union,locations,weighted,weights,uid):
 g=sum(k for a,k,code,counts in parts);m=len(union);dist=np.zeros((m,g+1));dist[:,0]=1.;used=0
 for (a,k,code,counts),loc in zip(parts,locations):
  freq=weighted[a].copy();np.add.at(freq,code,-counts*weights[cid.loc[uid]]);freq=np.maximum(freq,0);total=freq.sum()
  if total<=0:raise ValueError('LOPO empty')
  p=np.zeros(m);p[loc]=freq/total;pmf=binom.pmf(np.arange(k+1)[None,:],k,p[:,None]);nxt=np.zeros_like(dist)
  for j in range(k+1):nxt[:,j:j+used+1]+=pmf[:,j,None]*dist[:,:used+1]
  dist=nxt;used+=k
 z=np.arange(g+1,dtype=float);z[0]=1
 return np.log(g)-np.sum(dist*(np.arange(g+1)*np.log(z))[None,:])/g


expected=json.loads((base/'sensitivity_10.json').read_text()); path=json.loads((base/'sensitivity_amplitude.json').read_text()); bu=json.loads((base.parent/'core'/'contrast_actual.json').read_text())['results']['uniform']['beta']
def evaluate(weights):
 assert np.all(weights>0)
 weighted={a:np.bincount(code,weights=cnt*weights[contributors],minlength=len(items)) for a,(items,code,contributors,cnt) in ad.items()}
 e=np.array([expectation(*prepared[j],weighted,weights,int(uid)) for j,uid in enumerate(uids)])
 return float(xd@(obs-e)/den),float(e.mean()),float(xd@e/den)
checkpoint=base/'.checkpoint.json'
h=hashlib.sha256()
for f in [Path(__file__),base/'sensitivity_10.json',base/'sensitivity_amplitude.json',base.parent/'core'/'upstream.csv',base.parent/'core'/'contrast_actual.json',*[raw/f'{s}_sample.csv' for s in ('train','val','test')]]:
 h.update(hashlib.sha256(f.read_bytes()).digest())
key=h.hexdigest()
cache=json.loads(checkpoint.read_text()) if checkpoint.exists() else {}
if cache.get('key')!=key: cache={'key':key,'values':{}}
def checked_eval(name,weights,ref,make_row):
 vals=cache['values'][name] if name in cache['values'] else evaluate(weights)
 row=make_row(*vals)
 np.testing.assert_allclose(list(row.values()),[ref[k] for k in row],rtol=0,atol=1e-10)
 cache['values'][name]=list(vals)
 tmp=checkpoint.with_suffix('.tmp');tmp.write_text(json.dumps(cache));os.replace(tmp,checkpoint)
 return vals
results=[]; amplitudes=[]
for b in range(10):
 z=np.random.default_rng(20261124000+b).exponential(size=len(cons)); beta,mean,cov=checked_eval(f"replicate_{b}",z,expected[b],lambda beta,mean,cov:dict(replicate=b,beta_local=beta,contrast=beta-bu)); r=dict(replicate=b,beta_local=beta,contrast=beta-bu);results.append(r)
 np.testing.assert_allclose(list(r.values()),[expected[b][k] for k in r],rtol=0,atol=1e-10);print('PASS replicate',b,beta,flush=True)
 if b==0:
  for ref in path:
   lam=ref['weight_amplitude'];w=1+lam*(z-1);bb,mm,cc=(beta,mean,cov) if lam==1 else checked_eval(f"amplitude_{lam}",w,ref,lambda bb,mm,cc:dict(weight_amplitude=lam,beta=bb,mean_expected_entropy=mm,x_cov_E_scaled=cc,min_weight=float(w.min()),contrast=bb-bu));r=dict(weight_amplitude=lam,beta=bb,mean_expected_entropy=mm,x_cov_E_scaled=cc,min_weight=float(w.min()),contrast=bb-bu);amplitudes.append(r)
   np.testing.assert_allclose(list(r.values()),[ref[k] for k in r],rtol=0,atol=1e-10);print('PASS amplitude',lam,bb,flush=True)
(base/'sensitivity_actual.json').write_text(json.dumps(dict(replicates=results,amplitudes=amplitudes),indent=2));print('PASS Table S17',flush=True)
