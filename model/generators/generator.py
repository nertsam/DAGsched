import taskmodels
import itertools
import operator
import datetime

def trim(data, delta):
    output = []
    last = 0

    for element in data:
        if element['utilization'] > last * (1 + delta):
            output.append(element)
            last = element['utilization']

    return output

def merge_lists(m, n):
    merged = itertools.chain(m, n)
    return sorted(merged, key=operator.itemgetter('utilization'))

def approximate_utilization(candidates, utilization, epsilon):
    acc = [{'utilization': 0, 'task': [None]}]
    leng = len(candidates)

    candidates_map = [{'utilization': t.execution/t.period, 'task': [t]} for t in candidates]

    for key, element in enumerate(candidates_map, start=1):
        augmented_list = [{
            'utilization': element['utilization'] + a['utilization'],
            'task': a['task'] + element['task']
        } for a in acc]

        acc = merge_lists(acc, augmented_list)
        acc = trim(acc, delta=float(epsilon) / (2 * leng))
        acc = [t for t in acc if t['utilization'] <= utilization]

    return acc[-1]

'''
    Generates a taskset of variable size of sporadic, 
    constrained-deadline DAG tasks. 
'''

def generate(probability, utilization, processors, prepick, alpha, type = 'implicit', cutoff = 8, epsilon=0.1):
    prepick_taskset = [taskmodels.DAG(probability, utilization, processors, alpha, type, cutoff = 8) for i in range(int(prepick))]
    picked_taskset = approximate_utilization(prepick_taskset, utilization*processors, epsilon)
    return picked_taskset['task'][1:]