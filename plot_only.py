# run with 
# python3 plot_only.py processo operatore valore_operatore_1(SM) valore_operatore_2 xsec1_inPb xsec2_inPb label 

import os

import sys
import numpy as np
from hist import Hist
from lhereader import LHEReader
from matplotlib import pyplot as plt
import json
from cycler import cycler
import gzip
import shutil

plt.rcParams.update({'font.size': 16}) # size of labels and axis title


def plot(data1,data2,oppe,valu2,xs,xs2,label):
#def plot(data1, data2,oppe,valu,label):
    '''Plots all histograms. No need to change.'''

    outdir = './plots_alessandra_script/'
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    hist_name = label + '_mass'
    xaxis_name = '$m_{' + label + '}$ [GeV]'

    xminhist = 550
    xmaxhist = 3550 
    nbins = (float(xmaxhist)-float(xminhist))/100. # define bins to have 100 GeV in each bin
    print('nbins: ',nbins)

    fig = plt.figure(figsize=(8.,6.))

    print('length data SM: ',len(data1))
    print('length data BSM: ',len(data2))

    weight1 = np.full_like(data1, (float(xs)*1000.)/float(len(data1))) # weight: xsec [pb] transformed in fb divided per number of events
    weight2 = np.full_like(data2, (float(xs2)*1000.)/float(len(data2)))

    print('weight1 array: ', weight1)
    print('weight2 array: ', weight2)
    print('length weight1: ', len(weight1))
    print('length weight2 : ', len(weight2))
    print('sum of weight1: ', sum(weight1))
    print('sum of weight2: ', sum(weight2))
    print('xsec SM: ', xs)
    print('xsec BSM: ', xs2)
   

    # Plot two distributions on the same plot
    ax1 = fig.add_subplot(4, 1, (1,3)) # nrows, ncols, index (fist, last)
    ax1.set_ylabel("cross section [fb/100 GeV]")
    ax1.set_xticklabels([]) #remove labels of x axis
    ax1.set_xlim(xminhist,xmaxhist) #fix limits of xaxis
    if (oppe == 'FM3' and label == 'HH'):
        ax1.set_ylim(0.000005,5) #fix limits of xaxis
    ax1.set_yscale('log') # log scale of y axis

    val_of_bins_data2, edges_of_bins_data2, patches_data2 = plt.hist(data2, int(nbins), range=(xminhist, xmaxhist), density=False, weights=weight2, histtype='step', label="$f_{" + oppe[1:3] + "}/\Lambda^4 =" + valu2 + "$ TeV$^{-4}$")
    val_of_bins_data1, edges_of_bins_data1, patches_data1 = plt.hist(data1, int(nbins), range=(xminhist, xmaxhist), density=False, weights=weight1, histtype='step', label="SM")

    print('bin content hist SM: ', val_of_bins_data1)
    print('bin content hist BSM: ', val_of_bins_data2)
    print('edges of bin hist SM: ', edges_of_bins_data1)
    print('edges of bin hist BSM: ',edges_of_bins_data2)
    len1 = len(edges_of_bins_data1)-1
    len2 = len(edges_of_bins_data2)-1
    print(len1, len2)
    print('area hist SM: ', sum(val_of_bins_data1[0:len1]))
    print('area hist BSM: ', sum(val_of_bins_data2[0:len2]))

    ax1.legend()

    # Set ratio where val_of_bins_data2 is not zero
    ratio = np.divide(val_of_bins_data2,
                      val_of_bins_data1,
                      where=(val_of_bins_data1 !=0))

    print("ratio:", ratio)

    # Compute error on ratio (null if cannot be computed)
    # error propagation, bin per bin
    # error on bins: sum of squared weights
    # val_of_bins_data1 = num of evt in 1 bin * weight (since all weight are equal)
    # the squared error (sigma^2) on the bin of weighted hist is sum(weight^2)
    # since all weights are equal, sigma^2 = sum(weight^2) = num of evt in 1 bin * weight^2 
    # simplifying a bit, it remains like this
    error = ratio * np.sqrt(np.divide(weight2[0], val_of_bins_data2, where=(val_of_bins_data2 != 0)) +
                            np.divide(weight1[0], val_of_bins_data1, where=(val_of_bins_data1 != 0))
                            )

    print("error:", error)

    for i in range(len(ratio)):
        # replace hardik with shardul
        if (abs(ratio[i]) < 0.1):
            ratio[i] = 999.
        if (error[i] > 0.5*ratio[i]):
            error[i] = 1.			
            
    # Add the ratio on the existing plot
    # Add an histogram of errors
    ax3 = fig.add_subplot(4, 1, 4)
    ax3.set_ylabel('BSM/SM') # y axis of the ratio plot name
    ax3.set_xlabel(xaxis_name) # x axis name
    ax3.set_xlim(xminhist,xmaxhist) #fix limits of xaxis

    bincenter = 0.5 * (edges_of_bins_data1[1:] + edges_of_bins_data1[:-1])
    ax3.errorbar(bincenter, ratio, yerr=error, fmt='o', color='k') # ratio with error
    ax3.set_ylim(-0.5,5.)
    ax3.set_yticks([0, 1, 2, 3, 4])

    # horizontal line
    ax3.hlines(y=1., xmin=xminhist, xmax=xmaxhist, linewidth=1, colors='k', linestyles='dashed')
 

    plt.subplots_adjust(hspace=0)
    plt.savefig(f"{outdir}/{hist_name}.pdf")



def analyze(processo,oppe,valu):
    '''Event loop + histogram filling'''

#    lhe_file = os.path.join('/afs', 'cern.ch', 'user', 'a', 'acappati', 'work', 'ZZH', '220414_process1_nocuts', 'MG5_aMC_v2_7_3_py3', processo, 'Events', 'run_' + oppe + '_' + valu + '_cuts', 'unweighted_events.lhe') # process 1
    lhe_file = os.path.join('/afs', 'cern.ch', 'work', 'c', 'covarell', 'mg5_amcatnlo', 'dim8-hh', 'MG5_aMC_v2_7_3_py3', processo, 'Events', 'run_' + oppe + '_' + valu + '_nocutshistat', 'unweighted_events.lhe') # process 3
    lhe_file_gz = lhe_file + '.gz'

    # check if gzipped file exists
    if os.path.isfile(lhe_file_gz):
        # open the gzip (read+byte mode) as file_in context
        # open the recipient unzipped file (write+byte mode) as file_out context
        with gzip.open(lhe_file_gz, 'rb') as file_in, open(lhe_file, 'wb') as file_out:
            # copy content of zipped file to recipient
            shutil.copyfileobj(file_in, file_out)

    # check if unzipped file exists
    print('opening file ', lhe_file)
    if os.path.isfile(lhe_file):
        reader = LHEReader(lhe_file)
    else:
        # throw error
        raise FileNotFoundError(f'{lhe_file} not found!')
    
    # array delle masse
    mass_array = []
 
    # loop over events 
    for event in reader:
        # Find bosons
        tops = filter(
            lambda x: abs(x.pdgid) in (23,24,25),
            event.particles
        )

        # Sum over top four-momenta in the event
        combined_p4 = None
        for p4 in map(lambda x: x.p4(), tops):
            if combined_p4:
                combined_p4 += p4
            else:
                combined_p4 = p4

        mass_array.append(combined_p4.mass) # fill mass array

    return mass_array


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
    data1 = analyze(processo,oppe,valu)
    data2 = analyze(processo,oppe,valu2)
    plot(data1,data2,oppe,valu2,xs,xs2,label)

if __name__=="__main__":
    main()
    exit(0)
