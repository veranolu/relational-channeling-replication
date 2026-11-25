from entropy import *
u=pd.read_csv(root+'upstream.csv');u=u[u.n_agents>=2].copy();u['sbin']=pd.qcut(np.log(u.S_union),5,labels=False,duplicates='drop');u['stratum']=list(zip(u.n_purchases,u.n_agents,u.sbin));gr=u.groupby('stratum');keep=(gr.HHI.transform('size')>=8)&((gr.HHI.transform('max')-gr.HHI.transform('min'))>=.04);q=u.loc[keep].copy().reset_index(drop=True);assert len(q)==9095
cgroups={int(uid):g for uid,g in cai[cai.consumer_id.isin(q.consumer_id)].groupby('consumer_id',sort=False)}
cache={};rows=[];t=time.time()
for j,uid in enumerate(q.consumer_id):
 pieces=[]
 for a,g in cgroups[int(uid)].groupby('agent_id'):
  items,counts=ad[int(a)];focal=dict(zip(g.item_id,g.cnt));rem=counts-np.array([focal.get(int(it),0) for it in items]);mask=rem>0
  pieces.append((int(a),int(g.cnt.sum()),items[mask],rem[mask]))
 rows.append((int(uid),exact(pieces,'uniform'),exact(pieces,'local')))
 if (j+1)%2000==0:print(j+1,round(time.time()-t,2),flush=True)
r=pd.DataFrame(rows,columns=['consumer_id','E_exact_uniform','E_exact_local']);q=q.merge(r,on='consumer_id');sc=pd.factorize(q.stratum.astype(str))[0];ns=np.bincount(sc);x=q.HHI.to_numpy();xd=x-np.bincount(sc,weights=x)[sc]/ns[sc];den=xd@xd
for name in ['uniform','local']:
 y=q.item_entropy.to_numpy()-q['E_exact_'+name].to_numpy();print(name,'beta exact',xd@y/den,flush=True)
r.to_csv(root+'G_exact_entropy_strict9095_v1.csv',index=False)
print('TOTAL',time.time()-t,flush=True)
