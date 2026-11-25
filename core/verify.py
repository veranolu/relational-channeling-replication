from pathlib import Path
import json
import numpy as np
p=Path(__file__).resolve().parent
a=json.loads((p/'actual.json').read_text()); b=json.loads((p/'expected.json').read_text())
for k in ['N','strata','components_in_sample','components_full_graph','largest_component_sample_n']: assert a[k]==b[k], k
for mode in ['uniform','local']:
 for k in ['beta','SE_CR1','CI95_normal','mean_E']: np.testing.assert_allclose(a[mode][k],b[mode][k],rtol=1e-10,atol=1e-12)
print('PASS: certified core results reproduced')
