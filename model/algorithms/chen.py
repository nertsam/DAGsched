import math
import model.algorithms.SchedulingTest

@requires('sad')
class ChenExtendedWindowAnalysis(model.algorithms.SchedulingTest):
    def __init__(self):
        super(ChenExtendedWindowAnalysis, self).__init__()



    @staticmethod
    def util(task):
        return float(task['execution'])/task['period']

    @staticmethod
    def intersect(interval_x, interval_y):

        if interval_lhs[0] <= 0 or interval_lhs[1] <= 0 or interval_rhs[0] <= 0 or interval_rhs[1] <= 0:
            return (0, 0)

        # verify input s.t. a0 < a1 and b0 < b1
        if a[0] > a[1] or b[0] > b[1]:
            return (0, 0)

        if (b[0] <= a[0]) and (a[0] <= b[1]):
            return (b[0], max(a[1], b[1]))

        if (a[0] <= b[0] and (b[0] <= a[1])):
            return (a[0], max (a[1], b[1]))

        return (0,0)

def l_max_increasing(task, mu, processors):
    rho = float(processors-mu)/(processors-1)    
    if float(task['execution'])/task['deadline'] > rho:
        return (0,0)
    
    if float(task['execution'])/task['period'] <= rho:
        return (1, float('inf'))
    
    numerator = rho*(task['period']-task['deadline'])
    denumerator = rho*task['period'] - task['execution']
    
    if denumerator == 0:
        bound = float('inf')
    else:
        bound = int(float(numerator)/denumerator)
    
    return (1, bound)

def l_max_decreasing(task, mu, processors):
    rho = float(processors-mu)/(processors-1)
    if float(task['execution'])/task['period'] > rho:
        return (0,0)

    if float(task['execution'])/task['deadline'] <= rho:
        return (1, float('inf'))
    
    numerator = rho*(task['period']-task['deadline'])
    denumerator = rho*task['period']-task['execution']
    
    if denumerator == 0:
        return (0,0)
    else:
        return (math.ceil(float(numerator)/denumerator), float('inf'))


def retrieve_intervals(intervals = []):
    
    """
    retrieveIntervals returns True 
    iff the merging of intervals yields [1, infinity)
    """
    # (0,0) represent discardable elements and need to be removed
    ivals = [iv for iv in intervals if min(iv[0], iv[1]) > 0]
    if not ivals:
        return False
    ivals = sorted(ivals, key = lambda ival : ival[0], reverse=True)
    pivot = ivals.pop()
    left = pivot[0]
    right = pivot[1]
    while ivals:
        ival = ivals.pop()
        if (ival[0] >= left) and (ival[0] <= right):
            right = max(right,float(ival[1]))
        else:
            return False
    if (left == 1) and (right == float('inf')):
        return True
    return False


def f_fixpoint(task, hp_taskset, mu, processors):
    rho = float(processors-mu)/(processors-1)
    carry_in = int(math.ceil(mu)-1)
    
    sumUiDi = sum(sorted(map(lambda x : util(x)*x['deadline'], filter(lambda y : util(y) > rho, hp_taskset)), reverse=True)[:carry_in])
    sumUi = sum(map(lambda x : util(x), hp_taskset))
    sumCiCiUi = sum(map(lambda x : x['execution'] * (1.0-util(x)), hp_taskset))
    
    numerator = sumUiDi + sumCiCiUi + mu*(task['period']-task['deadline']) + sumUi*(task['deadline']-task['period'])
    denumerator = mu*task['period'] - sumUi*task['period'] - task['execution']
    if denumerator == 0:
        return float('inf')
    return float(numerator)/denumerator


def is_increasing(task, hp_taskset, mu, processors):
    rho = float(processors-mu)/(processors-1)
    largest = int(math.ceil(mu)-1)
    sum_task = util(task) * (task['deadline'] - task['period'])
    sum_mu = sum(sorted(map(lambda x : util(x)*x['deadline'], filter(lambda y : util(y)>rho, hp_taskset)),reverse=True)[:largest])  
    sum_hp = sum(map(lambda x:x['execution']*(1.0-util(x)),hp_taskset))
    return sum_task >= sum_mu-sum_hp
    
def is_decreasing(task, hp_taskset, mu, processors): 
    return not is_increasing(task,hp_taskset,mu,processors)

def f_infinity_mu(task, hp_taskset):
    return util(task) + sum(map(lambda x : util(x), hp_taskset))

def f_one_mu(task, hp_taskset, mu, processors):
    rho = float(processors-mu)/(processors-1)
    largest = int(math.ceil(mu)-1)
    sum_util = sum(map(lambda x : util(x), hp_taskset))
    sum_mu = sum(sorted(map(lambda x : util(x)*x['deadline'], filter(lambda y : util(y) > rho,hp_taskset)), reverse=True)[:largest])
    sum_hp = sum(map(lambda x : x['execution']*(1.0-util(x)), hp_taskset))
    return (float(task['execution']) + sum_hp + sum_mu) / task['deadline'] + sum_util

def l_feasible_region(task, hp_taskset, mu, processors):
    
    """
    Compute the set of feasible l-values for any given mu, that is 
    a subset of the valid interval.
    """
    
    # compute the valid interval
    if task['deadline'] >= task['period']:
        l_valid = l_max_increasing(task, mu, processors)
    else:
        l_valid = l_max_decreasing(task, mu, processors)
    
    # compute the feasible-region
    if is_increasing(task, hp_taskset,mu,processors) is True:
        if f_one_mu(task,hp_taskset,mu,processors) > mu:
            # never holds for any l
            # return invalid interval
            return (0,0)
        
        if f_infinity_mu(task,hp_taskset) <= mu:
            # holds for every l, so we return all mu-valid l-values
            return l_valid
        
        # if we reach this point, then there must be an intersection with 
        # the given mu value
        # i.e holds for all l values less then the border l-value l_mu
        else:
            # analytic formula to calculate F(l_mu, mu) = mu 
            l_mu = f_fixpoint(task,hp_taskset,mu,processors)
            # hold for all 1 <= l <= l_mu
            return intersect(l_valid, (1, float(l_mu)))
    # decreasing     
    else:
        if f_one_mu(task,hp_taskset,mu,processors) <= mu:
            # holds for every l, so return the 'valid interval'
            return l_valid

        if f_infinity_mu(task,hp_taskset) > mu:
            # never holds, so return an empty-measure interval
            return (0,0)
        
        # if we reach this point, then there must be an intersection with the given mu value
        # i.e holds for all l values larger then the border l value l_mu
        else:
            # analytic formula to calculate F(l_mu, mu) = mu 
            l_mu = f_fixpoint(task, hp_taskset, mu, processors)
            return intersect(l_valid, (float(l_mu), float('inf')))
    
    # should never get here
    raise ValueError, 'Could not compute the feasible region.'


def schedulable (taskset, processors):
    if processors <= 1:
        raise ValueError, "Amount of processors must be larger than one"
    def schedulable (task, hp_taskset, processors):
        feasible_region = []
        mu_range = []
        
        # enumerate through all relevant mu values,
        # where mu is dependant on task k
        if task['deadline'] >= task['period']:
            # 1 <= mu <= M - (M-1) * C_k / D_k
            border_mu = processors-(processors-1)*float(task['execution'])/task['deadline']
            mu_range = range(1, int(border_mu) + 1) + [border_mu]
        else:
            # 1 <= mu <= M - (M-1) * C_k / T_k
            border_mu = processors-(processors-1)*float(task['execution'])/task['period']
            mu_range = range(1, int(border_mu) + 1) + [border_mu]
        
        # enumerate over all relevant mu
        for mu in mu_range:
            # fit the l-region accordingly 
            feasible_region.append(l_feasible_region(task, hp_taskset, mu, processors))
        
        # return the set of all l-values for which a rho exists
        # i.e., if 'feasible' is the set of natural numbers, the 
        # the theorem holds and otherwise not. 
        return retrieve_intervals(feasible_region)
    
    # assert taskset to be ordered by priority
    for prio, task in enumerate(taskset):
        if not schedulable(task, taskset[:prio], processors):
            return False
    return True
    