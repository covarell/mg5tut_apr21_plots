import os

import numpy as np
from hist import Hist
from lhereader import LHEReader
from matplotlib import pyplot as plt


def plot(histograms):
    '''Plots all histograms. No need to change.'''
    outdir = './plots/'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for observable, histogram in histograms.items():
        plt.gcf().clf()
        histogram.plot()
        plt.gcf().savefig(f"{outdir}/{observable}.pdf")

def setup_histograms():
    '''Histogram initialization. Add new histos here.'''
    
    # Bin edges for each observable
    # TODO: Add your new observables and binnings here
    bins ={
        'ttbar_mass' : np.linspace(250,1200,50),
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
        # Find tops
        tops = filter(
            lambda x: abs(x.pdgid)==6,
            event.particles
        )

        # Sum over top four-momenta in the event
        combined_p4 = None
        for p4 in map(lambda x: x.p4(), tops):
            if combined_p4:
                combined_p4 += p4
            else:
                combined_p4 = p4

        # TODO: Fill more histograms around here
        histograms['ttbar_mass'].fill(combined_p4.mass, weight=event.weights[0])

    return histograms

histograms = analyze('lhe/cmsgrid_final.lhe')
plot(histograms)
