import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages


def analyses(*files):
    
    for k, file in enumerate(files):
        
        extension = str(k) + '_'

        dataset = np.load(file)
        dataset = dataset.item()

        tasks_same_utilization = [[] for i in range(10)]

        for i in range(10):
            for j in range(100):
                tasks_same_utilization[i] += dataset['tasksets'][i][j]
        
        # measurements
        wcets = [map(lambda x : x.execution, tasks_same_utilization[i]) for i in range(10)]
        densities = [map(lambda x : x.execution/min(x.period, x.deadline), tasks_same_utilization[i]) for i in range(10)]
        periods = [map(lambda x : x.period, tasks_same_utilization[i]) for i in range(10)]
        deadlines = [map(lambda x : x.deadline, tasks_same_utilization[i]) for i in range(10)]
        ratio = [map(lambda x : x.execution/x.critical, tasks_same_utilization[i]) for i in range(10)]
        avg_size = [[len(dataset['tasksets'][i][j]) for j in range(100)] for i in range(10)]

        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(30, 15))

        a = axes[0, 0].violinplot(wcets, widths=0.5, showmeans=True, showextrema=True, showmedians=True)
        axes[0, 0].set_title('Worst-case execution times', fontsize=16)
        axes[0, 0].set_xticklabels(['10%', '20%', '30%', '40%', '50%', '60%','70%', '80%', '90%', '100%'])
        axes[0, 0].set_xticks([y+1 for y in range(10)])
        axes[0, 0].set_xlabel('Utilization')
        axes[0, 0].grid()

        for partname in ('cbars','cmins','cmaxes','cmeans','cmedians'):
            vp = a[partname]
            vp.set_edgecolor('black')
            vp.set_linewidth(1)

        for pc in a['bodies']:
            pc.set_facecolor('grey')
            pc.set_edgecolor('black')
            pc.set_alpha(0.6)

        b = axes[0, 1].violinplot(deadlines, widths=0.3, showmeans=True, showextrema=True, showmedians=True)
        axes[0, 1].set_title('Deadlines', fontsize=16)
        axes[0, 1].set_xticklabels(['10%', '20%', '30%', '40%', '50%', '60%','70%', '80%', '90%', '100%'])
        axes[0, 1].set_xticks([y+1 for y in range(10)])
        axes[0, 1].set_xlabel('Utilization')
        axes[0, 1].grid()

        for partname in ('cbars','cmins','cmaxes','cmeans','cmedians'):
            vp = b[partname]
            vp.set_edgecolor('black')
            vp.set_linewidth(1)

        for pc in b['bodies']:
            pc.set_facecolor('grey')
            pc.set_edgecolor('black')
            pc.set_alpha(0.8)

        c = axes[0, 2].violinplot(periods, widths=0.3, showmeans=True, showextrema=True, showmedians=True)
        axes[0, 2].set_title('Periods', fontsize=16)
        axes[0, 2].set_xticklabels(['10%', '20%', '30%', '40%', '50%', '60%','70%', '80%', '90%', '100%'])
        axes[0, 2].set_xticks([y+1 for y in range(10)])
        axes[0, 2].set_xlabel('Utilization')
        axes[0, 2].grid()

        for partname in ('cbars','cmins','cmaxes','cmeans','cmedians'):
            vp = c[partname]
            vp.set_edgecolor('black')
            vp.set_linewidth(1)

        for pc in c['bodies']:
            pc.set_facecolor('grey')
            pc.set_edgecolor('black')
            pc.set_alpha(0.8)

        d = axes[1, 0].violinplot(ratio, widths=0.3, showmeans=True, showextrema=True, showmedians=True)
        axes[1, 0].set_title('Worst-case execution time to critical path ratio', fontsize=16)
        axes[1, 0].set_xticklabels(['10%', '20%', '30%', '40%', '50%', '60%','70%', '80%', '90%', '100%'])
        axes[1, 0].set_xticks([y+1 for y in range(10)])
        axes[1, 0].set_xlabel('Utilization')
        axes[1, 0].grid()

        for partname in ('cbars','cmins','cmaxes','cmeans','cmedians'):
            vp = d[partname]
            vp.set_edgecolor('black')
            vp.set_linewidth(1)

        for pc in d['bodies']:
            pc.set_facecolor('grey')
            pc.set_edgecolor('black')
            pc.set_alpha(0.8)

        e = axes[1, 1].violinplot(densities, widths=0.3, showmeans=True, showextrema=True, showmedians=True)
        axes[1, 1].set_title('Densities', fontsize=16)
        axes[1, 1].set_xticklabels(['10%', '20%', '30%', '40%', '50%', '60%','70%', '80%', '90%', '100%'])
        axes[1, 1].set_xticks([y+1 for y in range(10)])
        axes[1, 1].set_xlabel('Utilization')
        axes[1, 1].grid()

        for partname in ('cbars','cmins','cmaxes','cmeans','cmedians'):
            vp = e[partname]
            vp.set_edgecolor('black')
            vp.set_linewidth(1)

        for pc in e['bodies']:
            pc.set_facecolor('grey')
            pc.set_edgecolor('black')
            pc.set_alpha(0.8)

        f = axes[1, 2].violinplot(avg_size, widths=0.3, showmeans=True, showextrema=True, showmedians=True)
        axes[1, 2].set_title('Task set size', fontsize=16)
        axes[1, 2].set_xticklabels(['10%', '20%', '30%', '40%', '50%', '60%','70%', '80%', '90%', '100%'])
        axes[1, 2].set_xticks([y+1 for y in range(10)])
        axes[1, 2].set_xlabel('Utilization')
        axes[1, 2].grid()

        for partname in ('cbars','cmins','cmaxes','cmeans','cmedians'):
            vp = f[partname]
            vp.set_edgecolor('black')
            vp.set_linewidth(1)

        for pc in f['bodies']:
            pc.set_facecolor('grey')
            pc.set_edgecolor('black')
            pc.set_alpha(0.8)
        
        title = r'DAG task set statistics (%s-deadline, %d processors, $P_{e}$ = %.2f, $P_{h}$ = %.2f, $P_{\ell}$ = %.2f)' % (dataset['tasktype'], dataset['processors'], dataset['probedge'], dataset['probheavy'], dataset['problight'])

        fig.suptitle(title, fontsize=20)
 	fig.subplots_adjust(top = 0.78, bottom = 0.3, left = 0.08, right = 0.98, wspace=0.05, hspace=0.2)
        
        pp = PdfPages ('test.pdf')
        pp.savefig(fig)
        pp.close()
