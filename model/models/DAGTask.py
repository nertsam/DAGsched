import numpy as np


class DAG(object):

    def __init__(self, nodes, edges, period, deadline):
        self.nodes = nodes
        self.edges = edges
        self.period = period
        self.deadline = deadline
        self.volume = None
        self.length = None

    def set_nodes(self, nodes):
        self.nodes = nodes

    def set_edges(self, edges):
        self.edges = edges

    def set_deadline(self, deadline):
        self.deadline = deadline

    def set_period(self, period):
        self.period = period

    def get_volume(self):
        if not self.volume:
            self.volume = sum(self.nodes)
        return self.volume

    def get_length(self):
        if (self.nodes and self.edges) and not self.length:
            num_nodes = len(self.nodes)
            length = np.zeros((num_nodes, num_nodes))
            for k in range(num_nodes):
                for i in range(num_nodes):
                    if k == 0:
                        length[i, :] = (self.nodes[i] + self.nodes[:]) * self.edges[i, :]
                        length[i, length[i, :] == 0] = -np.inf
                    else:
                        length[i, :] = np.maximum(length[i, :], length[i, k] + length[k, :] - self.nodes[k])
            return max(max(self.nodes), length.max())
        return self.length
