from collections import deque
import numpy as np
import math

def wcrt_list_sched(nodes, edges, processors = 1):
    
    # create a working copy for deleting
    edge = edges.copy()
    
    # wort-case execution time of sub tasks
    wcet = list(nodes)
    
    # init the worst-case responsetimes
    wcrt = [0 for i in range(processors)]
    
    # init release and finish of each task 
    finished = list(nodes)
    released = [0 for i in range(len(wcet))]
    
    ready_list = deque()
    
    # find all source tasks in DAG
    for k in reversed(range(len(wcet))):
        if max(edge[i,k] for i in range(len(wcet))) == 0:
            ready_list.append(k)

    # compute the responsetimes
    while ready_list:
        # pick ready task
        task = ready_list.popleft()
        
        # choose idle processor
        selected = np.argmin(wcrt) 
        
        # update worst-case responsetime
        wcrt[selected] = max(wcrt[selected], released[task]) + wcet[task]
        
        # update finishing time of task
        finished[task] = wcrt[selected]
        
        # release adjacent tasks
        for j in range(len(wcet)):
            if edge[task, j] == 1:
                edge[task, j] = 0
                # set lower bound on release time
                released[j] = max(released[j], finished[task])
                # trigger if no precedence constraints
                if max(edge[k, j] for k in range(len(wcet))) == 0:
                    ready_list.append(j)
    return max(wcrt)

def util(task):
    return float(task['execution'])/task['period']

def demand_bound(task, time):
    if float(time) < task['deadline']:
        return 0
    return task['execution'] + util(task)*(float(time)-task['deadline'])

def partition(taskset, processors):
    if processors == 0:
        return False
    partitions = [[] for i in range(processors)]
    taskset = sorted(taskset, key = lambda task : task['deadline'], reverse=False)
    for task in taskset:
        ispartitioned = False
        for i in range(processors):
            COND_A = task.execution + sum(map(lambda x : demand_bound(x, task['deadline']), partitions[i])) <= task['deadline']
            COND_B = task.execution + task['period'] * sum(map(lambda x : util(x), partitions[i])) <= task['period']
            if COND_A and COND_B:
                partitions[i].append(task)
                ispartitioned = True
                break
        if ispartitioned is False:
            return False
    return ispartitioned

def minprocs(task, m):
    density = math.ceil(task['execution'] / min(task['deadline'], task['period']))
    if task['deadline'] <= task['period']:
        # constrained-deadline case
        for k in range(int(density), int(m) + 1):
            wcrt = wcrt_list_sched(task.nodes, task.edges, k)
            if wcrt <= task['deadline']:
                return k
        return np.inf        
    else:
        # arbitrary-deadline case
        for k in range(int(density), int(m) + 1):
            bound = k*task['deadline'] - (k-1)*task['critical']
            if (task['execution'] * (task['deadline'] / task['period'])) + min(k * (task['deadline'] % task['period']), task['execution']) <= bound:
                return k
        return np.inf
    return np.inf

def schedulable(taskset, processors):
    
    '''
        Sufficient schedulability test by Sanjoy Baruah
        according to 'Federated Scheduling of Sporadic DAG Task Systems'
    '''

    remaining = processors
    
    heavy_tasks = [task for task in taskset if task['execution'] > min(task['deadline'], task['period'])]
    light_tasks = [task for task in taskset if task not in heavy_tasks]
    
    #print 'heavy %d' % len(heavy_tasks)
    #print 'light %d' % len(light_tasks)
    #print sum(map(lambda x : x['execution']/x['period'], light_tasks))
    for task in heavy_tasks:
        needed = minprocs(task, remaining)
        #print needed
        if needed > remaining:
            return False
        else:
            remaining -= needed
    return partition(light_tasks, remaining)