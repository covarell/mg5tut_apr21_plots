import os

import numpy as np
from lhereader import LHEReader
from matplotlib import pyplot as plt

def analyze(lhe_file):
    '''Event loop + histogram filling'''

    mass = []
    weights = []
    
    reader = LHEReader(lhe_file)
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
        mass.append(combined_p4.mass)
        temp_weights = []
        for i in [0,1,2,3,4,5,6,7,8]:
            temp_weights.append(event.weights[i])
        weights.append(temp_weights)

    return mass, weights

mass,weights = analyze('lhe/cmsgrid_final.lhe')
transposed_weights = [list(row) for row in zip(*weights)]
'''Plots all histograms. No need to change.'''
outdir = './plots/'
if not os.path.exists(outdir):
  os.makedirs(outdir)

color_names = ['palegreen','lightgreen','darkolivegreen','olive','seagreen','','chartreuse','lawngreen']
plt.gcf().clf()
fig_all, ax_all = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
for i in [0,1,2,3,4,6,7]:    # remove cases with muR*muF = 4 or 1/4
    ax_all.set_xlim(200.,1500.)
    ax_all.hist(mass,weights=transposed_weights[i],bins=50,histtype='step',fill=None,ec=color_names[i])
plt.gcf().savefig(f"{outdir}/ttbar_mass_scaleVar.pdf")

