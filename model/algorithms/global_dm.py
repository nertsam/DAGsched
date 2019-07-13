import numpy as np
import math
import chen
import huang

def schedulable(taskset, processors, gamma = None):
    if gamma is None:
        heavy_tasks = [task for task in taskset if task['execution'] > task['deadline']]
    else:
        heavy_tasks = [task for task in taskset if task['execution'] > float(gamma) * task['critical']]
    transformed = [task for task in taskset if task not in heavy_tasks]
    for task in heavy_tasks:
        if gamma is None:
            mi = math.ceil((task['execution'] - task['critical']) / (task['deadline'] - task['critical']))
        else:
            mi = math.ceil((task['execution'] - task['critical']) / (gamma * task['critical'] - task['critical']))
        if mi >= float('inf'):
            print 'INF'
            return False
        
        for j in range(int(mi)):
            reservation = dict()
            if gamma is None:
                reservation['execution'] = (1 + ((task['execution'] - task['critical']) / (mi*task['critical']))) * task['critical']
            else:
                reservation['execution'] = float(gamma) * task['critical']
            reservation['deadline'] = task['deadline']
            reservation['period'] = task['period']
            reservation['critical'] = task['critical']
            transformed.append(reservation)

    #G-DM ordering
    transformed = sorted(transformed, key = lambda task : task['deadline'], reverse=False)
    print sum(map(lambda x : x['execution']/x['period'], transformed)) / sum(map(lambda x : x['execution']/x['period'], taskset))
    return chen.schedulable(transformed, processors) or huang.schedulable(transformed, processors)