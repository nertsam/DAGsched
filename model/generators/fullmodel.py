import numpy as np

def generate_period(model, deadline, min_scale, max_scale, method):
    assert (model in ['constrained', 'implicit', 'arbitrary'])
    assert (min_scale < max_scale)
    assert (method in ['loguniform', 'uniform'])

    if model is 'constrained':
        return deadline * np.random.uniform(min_scale, max_scale)

def generate(set_edge_probability, num_min_nodes, num_max_nodes, utilization, processors, alpha, type, cutoff):
    generated_num_nodes = np.random.randint(int(num_min_nodes), num_max_nodes)
    generated_edges = np.tril(np.random.choice([0, 1], size=(generated_num_nodes, generated_num_nodes),
                                               p=[1.0 - float(set_edge_probability), set_edge_probability]), -1)

    generated_period = def make_period(self):

        if self.type is 'contrained':
            return self.deadline * np.random.uniform(1.0, 2.0)

        elif self.type is 'implicit':
            return self.deadline

        elif self.type is 'arbitrary':
            return self.deadline * np.random.uniform(0.8, 2.0)

        else:
            # should not happen, just to be sure
            raise ValueError, "Type must be one of: 'constained', 'implicit', 'arbitrary'."



    def make_deadline(self):

        '''
            Generates an implicit deadline such that the task set
            exhibits reasonable properties. These are
            a) valid taskset i.e., Li <= Di
            b) decent task set size for all system utilizations
            c) mix of heavy and light tasks .

            If the system utilization allows for heavy tasks
            and decent task set size, then used method 1)
            else use method 2), that scales deadlines to
            decrease task utilization.

            method 1 generates a deadline for ti such that with prob
            1/alpha, ti is heavys and with prob 1-1/alpha is light.
        '''

        if self.utilization * self.processors > self.cutoff:
            return (self.critical + np.random.uniform(0, self.alpha * (self.execution - self.critical)))
        else:
            return (self.critical + (self.execution / (0.2 * self.processors * self.utilization))) * (
                        1 + 0.25 * np.random.gamma(2, 1))


    def compute_longest(self):
        cost = np.zeros((self.num_nodes, self.num_nodes))
        for k in xrange(self.num_nodes):
            for i in xrange(self.num_nodes):
                if k == 0:
                    cost[i, :] = (self.nodes[i] + self.nodes[:]) * self.edges[i, :]
                    cost[i, cost[i, :] == 0] = -np.inf
                else:
                    cost[i, :] = maximum(cost[i, :], cost[i, k] + cost[k, :] - self.nodes[k])
        return max(max(self.nodes), cost.max())