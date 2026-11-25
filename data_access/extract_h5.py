"""Extract local RecoGCN H5 split arrays; never redistribute generated CSVs."""
import argparse
from pathlib import Path
import h5py
import numpy as np
import pandas as pd
p=argparse.ArgumentParser(); p.add_argument('h5'); p.add_argument('output'); a=p.parse_args()
out=Path(a.output); out.mkdir(parents=True,exist_ok=True)
with h5py.File(a.h5,'r') as f:
    for name,n in [('train_sample',553744),('test_sample',66271),('val_sample',66231)]:
        x=np.asarray(f[name]); assert x.shape==(n,3), (name,x.shape)
        assert np.isfinite(x).all() and np.equal(x,np.floor(x)).all(),name
        pd.DataFrame(x.astype('int64'),columns=['user_id','agent_id','item_id']).to_csv(out/(name+'.csv'),index=False)
