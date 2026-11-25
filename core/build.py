import sys
from pathlib import Path
import pandas as pd,numpy as np
root=Path(__file__).resolve().parent
raw=Path(sys.argv[1]); frames=[]
for name,n in [('train',553744),('test',66271),('val',66231)]:
 d=pd.read_csv(raw/f'{name}_sample.csv').rename(columns={'user_id':'consumer_id'}); assert len(d)==n; frames.append(d[['consumer_id','agent_id','item_id']])
d=pd.concat(frames,ignore_index=True); assert len(d)==686246 and d.duplicated().sum()==55092
assert tuple(d.nunique())==(87105,13508,60562)
d.to_csv(root/'transactions_pooled.csv.gz',index=False)
v=d.groupby(['consumer_id','agent_id']).size(); g=v.groupby(level=0).sum(); a=v.groupby(level=0).size(); h=(v/g.reindex(v.index.get_level_values(0)).to_numpy())**2; h=h.groupby(level=0).sum()
f=d.groupby(['consumer_id','item_id']).size(); p=f/g.reindex(f.index.get_level_values(0)).to_numpy(); ent=(-p*np.log(p)).groupby(level=0).sum(); shelves=d.groupby('agent_id').item_id.agg(set).to_dict(); agents=v.reset_index().groupby('consumer_id').agent_id.agg(list)
u=pd.DataFrame({'n_purchases':g,'n_agents':a,'HHI':h,'item_entropy':ent});u=u[u.n_agents>=2].copy();u['S_union']=[len(set().union(*(shelves[j] for j in agents.loc[i]))) for i in u.index]; assert len(u)==11694;u.to_csv(root/'upstream.csv');print('PASS pooled and upstream',len(d),len(u))
