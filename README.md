# Plotting scripts for POWHEG tutorials

LHE ANALYZER

This code is pure python and does not rely on CMSSW, etc. The setup instructions below are made for lxplus,
but you should be able to get it running also on your laptop or other random environment.

Go to a totally new directory (outside the one created for POWHEG in CMSSW_11_2_4).

```
bash 
source /cvmfs/sft.cern.ch/lcg/views/LCG_99/x86_64-centos7-gcc8-opt/setup.sh

# Setup virtual environnment
# Remember to re-activate if you open a new shell
ENVNAME="mg5tut"
python3 -m venv ${ENVNAME}
source ${ENVNAME}/bin/activate
export PYTHONPATH="${ENVNAME}/lib/python3.8/site-packages/:${PYTHONPATH}"
python -m pip install -U pip
python -m pip install -U lhereader matplotlib mplhep 
git clone -b powheg_tutorial_21_05_20 git@github.com:covarell/mg5tut_apr21_plots.git
cd mg5tut_apr21_plots
mkdir lhe
mkdir plots
(copy the cmsgrid_final.lhe from the ttbar 3000-event generation inside the directory "lhe" just created)
python plot_skeleton.py
python plot_scaleVar.py
```

Follow the tutor's suggestions to modify the two python scripts above.

NANOGEN ANALYZER

Go to a totally new directory (outside the one created for POWHEG in CMSSW_11_2_4).

```
bash
export SCRAM_ARCH=slc7_amd64_gcc700

mkdir NanoGEN
cd NanoGEN
cp /eos/cms/store/group/phys_generator/POWHEGTutorial2021/NanoGEN/setup_NanoGEN.sh ./
source setup_NanoGEN.sh
mkdir Tutorial
cd Tutorial
cp -r /eos/cms/store/group/phys_generator/POWHEGTutorial2021/NanoGEN/Ex3_Showering/ ./
cd Ex3_Showering/
```

Edit python/Ex3_Showering.py to insert your gridpack location (in externalLHEProducer.args). If the job failed use: /afs/cern.ch/user/c/covarell/public/tutorial-21-05-20/gg_H-quark-mass-effects_slc7_amd64_gcc900_CMSSW_11_2_4_my_tutorial_ggHfull.tgz 

```
scram b -j 3
source run_cmsDriver.sh
```
Edit run_Ex3_Showering.py to change the number of events to be generated to 5000 (N.B. it must be done both in
externalLHEProducer.nEvents and in maxEvents.input!)

```
cmsRun run_Ex3_Showering.py
python createHists.py --in NanoGEN_Ex3_Showering.root --out NanoGEN_higgsPlots.root
```