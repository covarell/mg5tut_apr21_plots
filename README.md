# Plotting scripts for POWHEG tutorials

INITIAL SETUP

This code is pure python and does not rely on CMSSW, etc. The setup instructions below are made for lxplus,
but you should be able to get it running also on your laptop or other random environment.

Go to a totally new directory (outside the one created for POWHEG in CMSSW_13_3_0).

```
bash
export SCRAM_ARCH=el8_amd64_gcc12

mkdir Tutorial
cd Tutorial
cp /eos/cms/store/group/phys_generator/POWHEGTutorial2021/NanoGEN/setup_NanoGEN.sh ./
source setup_NanoGEN.sh
```
	
LHE ANALYZER

```
git clone -b powheg_tutorial_24_02_19 git@github.com:covarell/mg5tut_apr21_plots.git
cd mg5tut_apr21_plots
mkdir lhe
mkdir plots
(copy the cmsgrid_final.lhe from the ttbar 5000-event generation inside the directory "lhe" just created)
python3 plot_skeleton.py
python3 plot_scaleVar.py
```

Follow the tutor's suggestions to modify the two python scripts above.

NANOGEN ANALYZER

```
mkdir NanoGEN
cd NanoGEN
cp -r /eos/cms/store/group/phys_generator/POWHEGTutorial2021/NanoGEN/Ex3_Showering/ ./
cd Ex3_Showering/
```

Edit python/Ex3_Showering.py to insert your gridpack location (in externalLHEProducer.args). If the job failed use: /afs/cern.ch/user/c/covarell/public/tutorial-24-02-19/gg_H-quark-mass-effects_el8_amd64_gcc12_CMSSW_13_3_0_my_tutorial_ggHfull.tgz 

```
scram b 
source run_cmsDriver.sh
cmsRun run_Ex3_Showering.py
python3 createHists.py --in NanoGEN_Ex3_Showering.root --out NanoGEN_higgsPlots.root
```