import os

import sys
import numpy as np
from hist import Hist
from lhereader import LHEReader
from matplotlib import pyplot as plt
import json
from cycler import cycler

def plot(histograms1,histograms2,oppe,valu,label):
    '''Plots all histograms. No need to change.'''
    outdir = './plots/'
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    thelabel = "$m_{" + label + "}$ [GeV]"

    hist_1 = Hist.new.Var(np.linspace(550,3550,30), name="wz_mass", label=thelabel).Double()
    hist_2 = Hist.new.Var(np.linspace(550,3550,30), name="wz_mass", label=thelabel).Double()

    plt.gcf().clf()
    for observable, histogram in histograms1.items():
        hist_2 = histogram
    for observable, histogram in histograms2.items():
        hist_1 = histogram
        
    fig = plt.figure(figsize=(8, 6))
    thelabel = "$f_{" + oppe[1:3] + "}/\Lambda^4 =" + valu + "$ TeV$^{-4}$"
    main_ax_artists, subplot_ax_artists = hist_1.plot_ratio(
        hist_2,
        rp_ylabel="Ratio",
        rp_num_label=thelabel,
        rp_denom_label="SM",
        rp_uncert_draw_type="line",  # line or bar
        rp_uncertainty_type="poisson",
        rp_ylim = [-0.5,5.5]
    )
    #ax.set_ylabel("cross section [fb/50 GeV]") 
    plt.gcf().savefig(f"{outdir}/{observable}.pdf")

def setup_histograms(label):
    '''Histogram initialization. Add new histos here.'''
    
    # Bin edges for each observable
    # TODO: Add your new observables and binnings here
    bins ={
        'wz_mass' : np.linspace(550,3550,30),
   #     'jj_mass' : np.linspace(0,5000,50),
    } 
    thelabel = "$m_{" + label + "}$ [GeV]"

    # No need to change this part
    histograms = { 
                    observable : (
                                    Hist.new
                                    .Var(binning, name=observable, label=thelabel)
                                    .Double()
                                )
                    for observable, binning in bins.items()
    }

    return histograms

def analyze(processo,oppe,valu,xs,label):
    '''Event loop + histogram filling'''

    lhe_file = '/afs/cern.ch/user/c/covarell/work/mg5_amcatnlo/dim8-hh/MG5_aMC_v2_7_3_py3/' +processo+ '/Events/run_' + oppe + '_' + valu + '_nocutshistat/unweighted_events.lhe'     
    os.system("gunzip "+lhe_file+".gz")
    reader = LHEReader(lhe_file)
    histograms = setup_histograms(label)
  
    for event in reader:
        # Find tops
        tops = filter(
            lambda x: abs(x.pdgid) in (23,24,25),
            event.particles
        )
    #    jets = filter(
    #        lambda x1: abs(x1.pdgid) in (1,2,3,4,5) and x1.status > 0,
    #        event.particles
    #    )

        # Sum over top four-momenta in the event
        combined_p4 = None
        for p4 in map(lambda x: x.p4(), tops):
            if combined_p4:
                combined_p4 += p4
            else:
                combined_p4 = p4

    #    for i_limit in limit_list.keys():
     #       if combined_p4.mass < i_limit: 
      #          limit_list[i_limit] += 1
     
      #  combined_p42 = None
      #  for p42 in map(lambda x1: x1.p4(), jets):
      #      if combined_p42:
      #          combined_p42 += p42
      #      else:
       #         combined_p42 = p42

        # --- save file with fit results
        #outfile = './fractions_' + processo + '_' + oppe + '_' + valu + '.json'
        #with open(outfile,'w') as f:
        #        json.dump(limit_list,f)
        myweight = float(xs)/40.;

        # TODO: Fill more histograms around here
        histograms['wz_mass'].fill(combined_p4.mass, weight=myweight)
     #   histograms['jj_mass'].fill(combined_p42.mass, weight=1.)

    os.system("gzip "+lhe_file)
    return histograms

def main():

    if (len(sys.argv) < 3):
        print("specify the process, operator and valu please")
        sys.exit(1)

    # --- out directory
    processo = sys.argv[1]
    oppe = sys.argv[2]
    valu = sys.argv[3]
    valu2 = sys.argv[4]
    xs = sys.argv[5]
    xs2 = sys.argv[6]
    label = sys.argv[7]

    #histograms = analyze('/afs/cern.ch/work/c/covarell/mg5_amcatnlo/test-dim8-zzh/MG5_aMC_v2_7_3_py3/vbf-hh-mhhcut/Events/run_05/unweighted_events.lhe')
    #histograms = analyze('/afs/cern.ch/user/c/covarell/work/mg5_amcatnlo/dim8-hh/MG5_aMC_v2_7_3_py3/vbf-wpmz-4f/Events/run_FM4_20_cutshistat/unweighted_events.lhe')
    histograms1 = analyze(processo,oppe,valu,xs,label)
    histograms2 = analyze(processo,oppe,valu2,xs2,label)
    plot(histograms1,histograms2,oppe,valu2,label)

if __name__=="__main__":
    main()
    exit(0)
