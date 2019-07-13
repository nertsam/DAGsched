import math
import numpy as np

def util(task):
    return float(task['execution']) / task['period']    

def bounded_huang(task, hp_taskset, processors):
    return processors * util (task) + sum (map (lambda item : util (item), hp_taskset)) < processors

def schedulable(taskset, processors):
    def schedulable_huang (task, hp_taskset, processors):
        if bounded_huang (task, hp_taskset, processors):
            # sum of M-1 largest Di Ui 
            sum_sigma = sum (sorted (map (lambda x : x['deadline'] * util (x), hp_taskset), reverse = True)[:processors-1])
            sum_work = sum (map (lambda x : x['execution'] * (1.0 - util (x)), hp_taskset))
            check_value_numerator = processors * task['execution'] + sum_sigma + sum_work
            check_value_denumerator = processors - sum (map (lambda x : util (x), hp_taskset))
            check_value = float (check_value_numerator) / check_value_denumerator
            if check_value > task['deadline']:
                return False
            return True
        else:
            return False
    for prio, task in enumerate (taskset):
        if schedulable_huang (task, taskset[:prio], processors) is False:
            return False
    return True