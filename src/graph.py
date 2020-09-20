from pygraphblas import *
from pygraphblas.types import BOOL
from pyformlang.regular_expression import Regex

class Graph:
    def __init__(self):
        self.labels_adj = dict()
        self.start_states = set()
        self.final_states = set()
        self.size = 0

    def read_from_txt(self, filename):
        input_file = open(filename)
        edges = input_file.readlines()
        input_file.close()
        size = 0

        for edge in edges:
            v1, _, v2 = edge.split(' ')
            v1, v2 = int(v1), int(v2)
            size = max(size, v1, v2)

        size += 1
        self.size = size

        for edge in edges:
            v1, label, v2 = edge.split(' ')
            v1, v2 = int(v1), int(v2)
            if label not in self.labels_adj:
                self.labels_adj[label] = Matrix.sparse(BOOL, size, size)
            self.labels_adj[label][v1, v2] = True
            self.start_states.add(v1)
            self.final_states.add(v2)

    def read_from_regex(self, filename):
        input_file = open(filename)
        regex = Regex(input_file.read().rstrip())
        input_file.close()
        dfa = regex.to_epsilon_nfa().to_deterministic().minimize()
        size = len(dfa.states)
        self.size = size

        i = 0
        state_number = dict()
        for state in dfa.states:
            state_number[state] = i
            i += 1

        for v1, label, v2 in dfa._transition_function.get_edges():
            self.labels_adj[label] = Matrix.sparse(BOOL, size, size)
            self.labels_adj[label][state_number[v1], state_number[v2]] = True

        for st in dfa.final_states:
            self.final_states.add(state_number[st])

        self.start_states.add(state_number[dfa.start_state])

    def transitive_closure(self):
        res = Matrix.sparse(BOOL, self.size, self.size)
        for label in self.labels_adj:
            res |= self.labels_adj[label]
        for _ in range(self.size):
            res += res @ res
        return res

    def intersect(self, other):
        res = Graph()
        res.size = self.size * other.size

        for l in self.labels_adj:
            if l in other.labels_adj:
                res.labels_adj[l] = self.labels_adj[l].kronecker(other.labels_adj[l])

        for i in self.start_states:
            for j in other.start_states:
                res.start_states.add(i * self.size + j)

        for i in self.final_states:
            for j in other.final_states:
                res.final_states.add(i * self.size + j)

        for label in res.labels_adj:
            print(label, ": ", res.labels_adj[label].nvals)

        return res

    def reachable_from(self, from_vertices):
        res = self.transitive_closure()

        for v in range (self.size):
            if v not in from_vertices:
                res.assign_row(v, Vector.sparse(BOOL, self.size).full(0))

        return res

    def reachable_from_to(self, from_vertices, to_vertices):
        res = self.transitive_closure()

        for v in range (self.size):
            if v not in from_vertices:
                res.assign_row(v, Vector.sparse(BOOL, self.size).full(0))

            if v not in to_vertices:
                res.assign_col(v, Vector.sparse(BOOL, self.size).full(0))

        return res
