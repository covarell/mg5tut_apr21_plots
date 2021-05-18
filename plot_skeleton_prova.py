import os

import numpy as np
from hist import Hist
from lhereader import LHEReader
from matplotlib import pyplot as plt


def plot(histograms1,histograms2, histograms3):
    '''Plots all histograms. No need to change.'''
    outdir = './plots/'
    if not os.path.exists(outdir):
        os.makedirs(outdir);

    plt.gcf().clf()

    for observable, histogram in histograms1.items():
        histogram.plot()
    for observable, histogram in histograms2.items():
        histogram.plot()
    for observable, histogram in histograms3.items():
        histogram.plot()
        
    plt.gcf().savefig(f"{outdir}/{observable}.pdf")

def setup_histograms():
    '''Histogram initialization. Add new histos here.'''
    
    # Bin edges for each observable
    # TODO: Add your new observables and binnings here
    bins ={
        'hh_mass' : np.linspace(250,2000,20),
    } 

    # No need to change this part
    histograms = { 
                    observable : (
                                    Hist.new
                                    .Var(binning, name=observable, label=observable)
                                    .Int64()
                                )
                    for observable, binning in bins.items()
    }

    return histograms

def analyze(lhe_file):
    '''Event loop + histogram filling'''
    
    reader = LHEReader(lhe_file)
    histograms = setup_histograms()
    for event in reader:
        # Find charged leptons
        tops = filter(
            lambda x: abs(x.pdgid)==25,
            event.particles
        )

        # Sum over top four-momenta in the event
        combined_p4 = None
        for p4 in map(lambda x: x.p4(), tops):
            if combined_p4:
                combined_p4 += p4
            else:
                combined_p4 = p4

        myweight = 10.0
        if 'run_01' in lhe_file:
            myweight = 1.257
        if 'run_02' in lhe_file: 
            myweight = 1.704
        if 'run_03' in lhe_file: 
            myweight = 1.460

        # TODO: Fill more histograms around here
        histograms['hh_mass'].fill(combined_p4.mass, weight=myweight)

    return histograms

histograms1 = analyze('/afs/cern.ch/work/c/covarell/mg5_amcatnlo/test-dim8-zzh/MG5_aMC_v2_7_3_py3/test-vbf-hh/Events/run_01/unweighted_events.lhe')
histograms2 = analyze('/afs/cern.ch/work/c/covarell/mg5_amcatnlo/test-dim8-zzh/MG5_aMC_v2_7_3_py3/test-vbf-hh/Events/run_02/unweighted_events.lhe')
histograms3 = analyze('/afs/cern.ch/work/c/covarell/mg5_amcatnlo/test-dim8-zzh/MG5_aMC_v2_7_3_py3/test-vbf-hh/Events/run_03/unweighted_events.lhe')
plot(histograms1,histograms2,histograms3)
