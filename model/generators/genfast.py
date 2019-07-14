import numpy as np
import math
import randfixsum

def utiliz_uniform(nsets, msets, utilizations, processors):
    return randfixsum.randfixedsum(nsets, msets, processors*utilizations, 0, processors)

def period_uniform(nsets, msets, min_period, max_period):
    return np.random.uniform(min_period, max_period,size=(msets, nsets))

def period_loguniform(nsets, msets, min_period, max_period):
    return np.exp(np.random.uniform(min_period, max_period,size=(msets, nsets)))

def generate(nsets, msets, utilizations, min_period, max_period, processors):
    periods = period_loguniform(nsets, msets, min_period, max_period)
    utiliza = utiliz_uniform(nsets, msets, utilizations, processors)    
    tasksets = []
    for i in xrange(msets):
        taskset = []
        for j in xrange(nsets):
            execution = utiliza[i][j] * periods[i][j] 
            period = periods[i][j]
            deadline = period #np.random.uniform(1, 2) * period
            critical = np.random.uniform(0.6, 0.9) * deadline
            task = {'execution' : execution, 'critical' : critical, 'period' : period, 'deadline' : deadline}
            taskset.append(task)			
        tasksets.append(taskset)
    return tasksets