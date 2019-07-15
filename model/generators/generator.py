import numpy as np
import itertools
import operator


def approximateUtilization(candidate_taskset, utilization, delta):
    def trim(taskset, delta):
        trimmed = []
        last = 0
        for task in taskset:
            if task.utilization > last * (1 + delta):
                trimmed.append()
                last = task.utilization
        return trimmed
    acc = [{'utilization': 0, 'task': [None]}]
    leng = len(candidate_taskset)
    candidates_map = [{'utilization': t.execution/t.period, 'task': [t]} for t in candidate_taskset]
    for key, element in enumerate(candidates_map, start=1):
        augmented_list = [{
                'utilization': element['utilization'] + a['utilization'],
                'task'       : a['task'] + element['task']
            } for a in acc]

        acc = sorted(itertools.chain(acc, augmented_list), key=operator.itemgetter('utilization'))
        acc = trim(acc, delta=float(delta)/(2*leng))
        acc = [t for t in acc if t['utilization'] <= utilization]
        return acc[-1]

    @staticmethod
    def randfixedsum(n, m, s, a, b):
        """

        ROGER STAFFORD
        https://de.mathworks.com/matlabcentral/fileexchange/9700-random-vectors-with-fixed-sum?focused=5064802&tab=function

        This generates an n by m array x, each of whose m columns
        contains n random values lying in the interval [a,b], but
        subject to the condition that their sum be equal to s.  The
        scalar value s must accordingly satisfy n*a <= s <= n*b.  The
        distribution of values is uniform in the sense that it has the
        conditional probability distribution of a uniform distribution
        over the whole n-cube, given that the sum of the x's is s.
        """

        if int(m) != m or int(n) != n or m < 0 or n < 1:
            raise (ValueError, "N must be a whole number and m a non-negative integer.")

        elif s < n * a or s > n * b or a >= b:
            raise (ValueError, "Inequalities n*a <= s <= n*b and a < b must hold.")

        tiny = np.finfo(float).tiny
        huge = np.finfo(float).max

        s = float(s - n * a) / (b - a)

        k = max(min(int(s), n - 1), 0)
        s = max(min(s, k + 1), k)

        s1 = s - np.arange(k, k - n, -1)
        s2 = np.arange(k + n, k, -1.) - s

        w = np.zeros((n, n + 1))
        w[0, 1] = huge
        t = np.zeros((n - 1, n));

        for i in np.arange(2, n + 1):
            tmp1 = w[i - 2, np.arange(1, i + 1)] * s1[np.arange(0, i)] / float(i)
            tmp2 = w[i - 2, np.arange(0, i)] * s2[np.arange(n - i, n)] / float(i)
            w[i - 1, np.arange(1, i + 1)] = tmp1 + tmp2
            tmp3 = w[i - 1, np.arange(1, i + 1)] + tiny
            tmp4 = s2[np.arange(n - i, n)] > s1[np.arange(0, i)]
            t[i - 2, np.arange(0, i)] = (tmp2 / tmp3) * tmp4 + (1 - tmp1 / tmp3) * (np.logical_not(tmp4))

        x = np.zeros((n, m))
        if m == 0:
            return

        rt = np.random.uniform(size=(n - 1, m))
        rs = np.random.uniform(size=(n - 1, m))
        s = np.repeat(s, m)
        j = np.repeat(k + 1, m)
        sm = np.zeros((1, m))
        pr = np.repeat(1, m)

        for i in np.arange(n - 1, 0, -1):
            e = rt[(n - i) - 1, ...] <= t[i - 1, j - 1]
            sx = rs[(n - i) - 1, ...] ** (1.0 / i)
            sm = sm + (1.0 - sx) * pr * s / (i + 1)
            pr = sx * pr
            x[(n - i) - 1, ...] = sm + pr * e
            s = s - e
            j = j - e
        x[n - 1, ...] = sm + pr * s

        for i in range(0, m):
            x[..., i] = (b - a) * x[np.random.permutation(n), i] + a

        return x.T.tolist()

    @staticmethod
    def generateUniformUtilization(num_sets, num_tasks_sets, num_processors, utilization):
        return Generator.randfixedsum(num_sets, num_tasks_sets, num_processors*utilization, 0, num_processors)

    @staticmethod
    def generateUniformPeriods(num_sets, num_tasks_sets, min_period, max_period):
        return np.random.uniform(min_period, max_period, size=(num_tasks_sets, num_sets))

    @staticmethod
    def generateLogUniformPeriods(num_sets, num_tasks_sets, min_period, max_period):
        return np.exp(np.random.uniform(min_period, max_period, size=(num_tasks_sets, num_sets)))
