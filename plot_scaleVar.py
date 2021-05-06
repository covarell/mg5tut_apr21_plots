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

    plt.gcf().clf()
    histograms['ttbar_mass_def'].plot()
    histograms['ttbar_mass_1'].plot()
    histograms['ttbar_mass_2'].plot() 
    histograms['ttbar_mass_3'].plot() 
    histograms['ttbar_mass_4'].plot() 
    histograms['ttbar_mass_5'].plot() 
    histograms['ttbar_mass_6'].plot() 
    plt.gcf().savefig(f"{outdir}/ttbar_mass_variations.pdf")

def setup_histograms():
    '''Histogram initialization. Add new histos here.'''
    
    # Bin edges for each observable
    # TODO: Add your new observables and binnings here
    bins ={
        'ttbar_mass_def' : np.linspace(250,1200,50),
        'ttbar_mass_1' : np.linspace(250,1200,50),
        'ttbar_mass_2' : np.linspace(250,1200,50),
        'ttbar_mass_3' : np.linspace(250,1200,50),
        'ttbar_mass_4' : np.linspace(250,1200,50),
        'ttbar_mass_5' : np.linspace(250,1200,50),
        'ttbar_mass_6' : np.linspace(250,1200,50),
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
        histograms['ttbar_mass_def'].fill(combined_p4.mass, weight=event.weights[0])
        histograms['ttbar_mass_1'].fill(combined_p4.mass, weight=event.weights[1])
        histograms['ttbar_mass_2'].fill(combined_p4.mass, weight=event.weights[2])
        histograms['ttbar_mass_3'].fill(combined_p4.mass, weight=event.weights[3])
        histograms['ttbar_mass_4'].fill(combined_p4.mass, weight=event.weights[4])
        histograms['ttbar_mass_5'].fill(combined_p4.mass, weight=event.weights[5])
        histograms['ttbar_mass_6'].fill(combined_p4.mass, weight=event.weights[7])

    return histograms

histograms = analyze('lhe/cmsgrid_final.lhe')
plot(histograms)
