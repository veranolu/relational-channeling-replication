import json
from pathlib import Path
import numpy as np
p=Path(__file__).resolve().parent
a=json.loads((p/'contrast_actual.json').read_text()); e=json.loads((p/'contrast_expected.json').read_text())
for k in ['N','strata','components_in_sample','components_full_graph','largest_component_sample_n','den']: np.testing.assert_allclose(a[k],e[k],rtol=0,atol=1e-12)
for k in e['results']:
 for j in ['beta','se','ci','p']: np.testing.assert_allclose(a['results'][k][j],e['results'][k][j],rtol=0,atol=1e-12)
print('PASS all six slopes, CR1 SEs, intervals and p-values')
