# Plotting scripts for MG5 tutorials

This code is pure python and does not rely on CMSSW, etc. The setup instructions below are made for lxplus,
but you should be able to get it running also on your laptop or other random environment.

```bash 
source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh

# Setup virtual environnment
# Remember to re-activate if you open a new shell
ENVNAME="mg5tut"
python3 -m venv ${ENVNAME}
source ${ENVNAME}/bin/activate
export PYTHONPATH="${ENVNAME}/lib/python3.8/site-packages/:${PYTHONPATH}"

python3 -m pip install -U pip 
python3 -m pip install -U lhereader matplotlib mplhep 

```
