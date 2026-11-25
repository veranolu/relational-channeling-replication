import numpy as np,pandas as pd,glob,time
from scipy.stats import binom
from pathlib import Path
root=str(Path(__file__).resolve().parent)+'/'
d=pd.read_csv(root+'transactions_pooled.csv.gz',usecols=['consumer_id','agent_id','item_id'])
cai=d.groupby(['consumer_id','agent_id','item_id'],sort=False).size().rename('cnt').reset_index()
ai=d.groupby(['agent_id','item_id'],sort=False).size().rename('cnt').reset_index()
ad={int(a):(g.item_id.to_numpy(np.int32),g.cnt.to_numpy(np.float64)) for a,g in ai.groupby('agent_id',sort=False)}

def exact(parts,mode='local'):
    g=sum(k for _,k,_,_ in parts)
    union=np.unique(np.concatenate([it for _,_,it,_ in parts]));m=len(union)
    dist=np.zeros((m,g+1));dist[:,0]=1.;used=0
    for a,k,items,counts in parts:
        p=np.zeros(m);p[np.searchsorted(union,items)]=counts/counts.sum() if mode=='local' else 1/len(items)
        pmf=binom.pmf(np.arange(k+1)[None,:],k,p[:,None]);nxt=np.zeros_like(dist)
        for j in range(k+1):nxt[:,j:j+used+1]+=pmf[:,j,None]*dist[:,:used+1]
        dist=nxt;used+=k
    z=np.arange(g+1,dtype=float);z[0]=1
    return float(np.log(g)-np.sum(dist*(np.arange(g+1)*np.log(z))[None,:])/g)

def parts_for(uid):
    z=[]
    for a,g in cai[cai.consumer_id==uid].groupby('agent_id'):
        items,counts=ad[int(a)]; focal=dict(zip(g.item_id,g.cnt)); rem=counts-np.array([focal.get(int(it),0) for it in items]);mask=rem>0
        z.append((int(a),int(g.cnt.sum()),items[mask],rem[mask]))
    return z

