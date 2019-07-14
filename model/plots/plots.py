from __future__ import division
import sys
import numpy as np
import matplotlib.pyplot as plt
import itertools
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Tahoma']
rcParams['ps.useafm'] = True
rcParams['pdf.use14corefonts'] = True
rcParams['text.usetex'] = True
rcParams["figure.figsize"] = (17,15)

def plot(title, *filenames):
    figlabel = itertools.cycle(('a','b','c','d','e','f','g','h','i'))
    marker = itertools.cycle(('o', 'v','*','D','x','+'))
    colors = itertools.cycle(('c','r','b','g','r','y','y','b'))
    names = []
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fig.subplots_adjust (top = 0.9, left = 0.1, right = 0.95, hspace = 0.3)
    ax.set_xlabel('Utilization (\%)',size=17)
    ax.set_ylabel('Acceptance Ratio (\%)',size=17)
    ax.spines['top'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.tick_params(labelcolor = 'w', top = 'off', bottom = 'off', left = 'off', right = 'off')

    for filename in filenames:
        data = np.load(filename)
        data = data.item()
        step_size = data['step_size']        
        set_size = data['set_size']
        sim_size = data['sim_size']

        utilization = map(lambda u : 100 * u, np.arange(step_size, 1.0 + step_size, step_size))
        acceptance = map(lambda failed : 100.0 * (sim_size - failed)/sim_size, data['results'])
        ax.axis([-2,102,-2,102])
        ax.plot(utilization, acceptance, '-', color = colors.next(), marker = marker.next(), markersize = 12, fillstyle = 'none', markevery = 1, label = data['id'], linewidth = 1.9)
        names.append(data['id'])
        ax.tick_params(labelcolor='k', top='off', bottom='off', left='off', right='off')
        
        for tick in ax.xaxis.get_major_ticks():
            tick.label.set_fontsize(15)
        
        for tick in ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(15)
         
    if len(filenames) == 1:
        ax.legend(bbox_to_anchor = (1.65, 1.2), loc = 10, markerscale = 1.0, ncol = len(filenames), borderaxespad = 0., prop = {'size':7})
        ax.set_title('('+figlabel.next()+')', size = 8, y = 1.02)
        ax.grid()
    
    plt.title(title)
    ax.legend(names)
    ax.grid()
    plt.show()
    return fig