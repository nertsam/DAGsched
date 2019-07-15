import numpy as np
import model.algorithms.SchedulingTest

@model('DAG')
class SemiFederatedScheduling(model.algorithms.SchedulingTest):
    def __init__(self):
        super(SemiFederatedScheduling, self).__init__()


    class container(dict):
        def __init__(self, bound):
            dict.__setitem__(self, 'bound', bound)

    def schedulable(taskset, processors):
        # init remaining processors
        remaining = processors
        # a task is 'heavy' iff C_i > min(T_i, D_i) = D_i for constrained DL. min for safety
        heavy_tasks = [task for task in taskset if task['execution'] > task['deadline']]

        # a task 'ti' is 'light' iff 'ti' is not heavy
        light_tasks = [task for task in taskset if task not in heavy_tasks]

        # allocate processors for heavy tasks exclusively
        for task in heavy_tasks:
            gamma = float(task['execution']-task['critical']) / (task['deadline'] - task['critical'])
            if int(gamma) > remaining:
                return False
            remaining -= int(gamma)
            light_tasks.append(container(gamma-int(gamma)))

        if partition(light_tasks, remaining) is False:
            return False
        return True

    def partition(taskset, processors):

        '''
        Partitioned EDF of sporadic, constrained-deadline DAG tasks and
        container tasks with load-bounds according to the paper
        Semi-Federated Scheduling of Parallel Real-Time Tasks on
        Multiprocessors. Taskset is sorted by largest density first,
        where density(task) = C/D and density(container) = load-bound.
        '''
        if processors == 0:
            return False

        load = [0 for i in range(processors)]

        taskset = sorted(taskset, key = lambda item : item['bound'] if isinstance(item, container) else float(item['execution']) / item['deadline'], reverse=True)

        for item in taskset:
            cpu = np.argmin(load)
            if isinstance(item, container):
                if load[cpu] + item['bound'] > 1:
                    return False
                else:
                    load[cpu] += item['bound']
            else:
                if load[cpu] + (float(item['execution'])/item['deadline']) > 1.0:
                    return False
                else:
                    load[cpu] += float(item['execution'])/item['deadline']
        return True