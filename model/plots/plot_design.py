from __future__ import division
from matplotlib import rcParams

import matplotlib.pyplot as plt
import numpy as np
import sys
import numpy as np
import itertools

rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
rcParams['text.usetex'] = True


def plot(filegroups):
    
    names = []
    labels = ['(a) m = 8', '(b) m = 16', '(c) m = 32']
    lines = []
    
    fig, axes = plt.subplots(1, 3, sharey=True, sharex=True)
    plt.subplots_adjust(top = 0.9, bottom = 0.47, left = 0.08, right = 0.98, wspace=0.05, hspace=0.2)
    axes[0].set_ylabel('Acceptance Ratio (\%)',size=13)
    fig.text(0.5, 0.4, 'Utilization (\%)', size=13, ha='center')

    for i in range(3):
        axes[i].spines['top'].set_color('none')
        axes[i].spines['bottom'].set_color('none')
        axes[i].spines['left'].set_color('none')
        axes[i].spines['right'].set_color('none')
        axes[i].tick_params(labelcolor = 'black', top = 'off', bottom = 'off', left = 'off', right = 'off')
        axes[i].grid()

    for i, filegroup in enumerate(filegroups):
        marker = itertools.cycle(('o', 'd', '+', 'v','h','D','x'))
        colors = itertools.cycle(('y','g','black','b','r','b','y','r'))
        for filename in filegroup:
            # load dataset
            dataset = np.load(filename)
            dataset = dataset.item()
            # basic setting
            stepsize = dataset['step_size']        
            setsize = dataset['set_size']
            simsize = dataset['sim_size']

            utilization = map(lambda u : 100.0 * u, np.arange(stepsize, 1.0 + stepsize, stepsize))
            acceptance = map(lambda failed : 100.0 * (simsize - failed)/simsize, dataset['results'])
            axes[i].axis([-2,102,-2,102])
            axes[i].plot(utilization, acceptance, '-', color = colors.next(), marker = marker.next(), markersize = 7, fillstyle = 'none', markevery = 1, label = dataset['id'], linewidth = 1.5)
            axes[i].tick_params(labelcolor='k', top='off', bottom='off', left='off', right='off')
            names.append(dataset['id'])
            axes[i].set_title(labels[i], size=13)
        
            for tick in axes[i].xaxis.get_major_ticks():
                tick.label.set_fontsize(13)
        
            for tick in axes[i].yaxis.get_major_ticks():
                tick.label.set_fontsize(13)
    
    axes[1].legend(names, bbox_to_anchor=(1.5, 1.2),
                                loc=5,
                                ncol=3,
                                markerscale = 1.0, 
                            borderaxespad=0.,framealpha=1,    
                            prop={'size':12})
    
    #plt.show()
    return fig
