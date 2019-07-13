import numpy as np
import math

def bucket(task, partition):
    a = task['deadline'] - sum(map(lambda x : x['execution'] + (float(x['execution'])/x['period']) * (task['deadline']-x['deadline']), partition))
    b = task['period'] - sum(map(lambda x : task['period'] * (x['execution']/x['period']), partition))
    return min(a,b)
    
def demand_bound(task, time):
    if float(time) < task['deadline']:
        return 0
    return task['execution'] + (float(task['execution'])/task['period'])*(float(time)-task['deadline'])

def split(group):
    group = [group[0] for k in range(len(group)+1)]
    # decrease execution budgets
    for task in group:
        task['execution'] = (task['execution'] / len(group)) + (1-(1/len(group))) * task['critical']
    return group

def best_fit(task, partitions):
    capacity = np.zeros(len(partitions))
    for i in range(len(capacity)):
        capacity[i] = bucket(task, partitions[i]) - task['execution']
    # choose best-fit
    capacity = map(lambda c : c if c >= 0 else np.inf, capacity)
    if not capacity:
        return False
    # candidates exist
    k = np.argmin(capacity)
    if capacity[k] == np.inf:
        return False
    return k

def worst_fit(task, partitions):
    capacity = np.zeros(len(partitions))
    for i in range(len(capacity)):
        capacity[i] = bucket(task, partitions[i]) - task['execution']
    # choose worst-fit
    capacity = map(lambda c : c if c >= 0 else -np.inf, capacity)
    if not capacity:
        return False
    # candidates exist
    k = np.argmax(capacity) 
    if capacity[k] == -np.inf:
        return False
    return k

def first_fit(task, partitions):
    capacity = np.zeros(len(partitions))
    for i in range(len(capacity)):
        capacity[i] = bucket(task, partitions[i]) - task['execution']
        if capacity[i] >= 0:
            return i
    return False

def fitting(task, partition, heuristic):
    if str(heuristic) not in ['worst-fit', 'best-fit', 'first-fit']:
        raise ValueError, "worst-fit, best-fit, first-fit"
        return

    if str(heuristic) == 'worst-fit':
        return worst_fit(task, partition)
    
    elif str(heuristic) == 'best-fit':
        return best_fit(task, partition)
    
    elif str(heuristic) == 'first-fit':
        return first_fit(task, partition)

def schedulable(taskset, processors, bounds, heuristic = 'first-fit'):
    # largest common gamma-value
    gamma = float(min(map(lambda x : float(x['deadline'])/x['critical'], taskset)))
    # Transformation stage
    heavy_tasks = [task for task in taskset if task['execution'] > gamma * task['critical']]
    transformed = [[task] for task in taskset if task not in heavy_tasks]
    for task in heavy_tasks:
        group = []
        mi = math.ceil(float(task['execution'] - task['critical']) / ((gamma-1.0)*task['critical']))
        if mi >= float('inf'):
            return False
        for j in range(int(mi)):
            reservation = dict()
            reservation['execution'] = (1 + ((task['execution'] - task['critical']) / (mi*task['critical']))) * task['critical']
            reservation['deadline'] = task['deadline']
            reservation['period'] = task['period']
            reservation['critical'] = task['critical']
            reservation['bound'] = max(mi, math.ceil(task['execution']/task['critical']), bounds)
            group.append(reservation)
        transformed.append(group)
    # set of transformed tasks, where 'belonging' tasks are grouped
    transformed = sorted(transformed, key = lambda group : group[-1]['deadline'], reverse=False)
    #P-EDF arbitrary-deadlines
    partition = [[] for i in range(processors)]
    for j, group in enumerate(transformed):
        # light task => no splitting
        if len(group) == 1:
            #print 'Partitioning Group: %d (light), size: %d' % (j, 1)
            for task in group:
                task_partitioned = False
                # PARTITIONING
                choice = fitting(task, partition, heuristic)
                if choice is not False:
                    partition[choice].append(task)
                    task_partitioned = True
                    break
                # PARTITIONING END
                if task_partitioned is False:
                    #print 'Could not partition light task'
                    return False
        # light task is partitioned or return False
        else:
            #print 'Partitioning Group: %d (heavy), size: %d' % (j, len(group))
            chance = False
            while len(group) <= group[0]['bound']:
                chance = True
                partition_group = list(partition)
                for i, task in enumerate(group):
                    task_is_partitioned = False
                    # PARTITIONING
                    choice = fitting(task, partition_group, heuristic)
                    if choice is not False:
                        partition_group[choice].append(task)
                        task_is_partitioned = True
                        continue
                    # PARTITION END
                    if task_is_partitioned is False:
                        chance = False
                        break
                if chance is False:
                    #print 'Split group id: %d, new size: %d' % (j, len(group))
                    group = split(group)
                    continue
                else:
                    #print 'group id: %d is partitioned with size: %d' % (j, len(group))
                    partition = partition_group
                    chance = True
                    break
            if chance is False:
                #print 'Could not partition heavy task'
                return False
    return True