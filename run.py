import sys,subprocess,os
from pathlib import Path
p=Path(__file__).resolve().parent/'core'
raw=Path(sys.argv[1]).resolve()
for name,args in [('build.py',[str(raw)]),('run_exact.py',[]),('run_ci.py',[]),('verify.py',[]),('contrast.py',[str(p)]),('verify_contrast.py',[])]:
 subprocess.run([sys.executable,str(p/name),*args],check=True,env={**os.environ,'OPENBLAS_NUM_THREADS':'1'})

for script,args in [("sensitivity/recompute.py",[str(raw)]),("core/plot_contrast.py",[])]:
 subprocess.run([sys.executable,str(p.parent/script),*args],check=True,env={**os.environ,"OPENBLAS_NUM_THREADS":"1"})
