from collections import deque
from pyformlang.cfg import *
from pygraphblas import Matrix, BOOL
from src.graph import Graph


def get_pairs(cfg: CFG):
    res = []
    for p in cfg.productions:
        if len(p.body) == 2:
            res.append(p)
    return res

class AlgoCFG:
    def read_cnf(input_file):
        with open(input_file, 'r') as f:
            productions = []

            for line in f:
                prod = line.split()
                productions.append(f'{prod[0]} -> {" ".join(prod[1:])}')

            cfg = CFG.from_text("\n".join(productions))
            return cfg

    def cyk(grammar: CFG, word: str):
        n = len(word)

        if n == 0:
            return grammar.generate_epsilon()

        cfg = grammar.to_normal_form()
        mtx = [[set() for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for prod in cfg.productions:
                if prod.body == [Terminal(word[i])]:
                    mtx[i][i].add(prod.head)

        for i in range(n):
            for j in range(n - i):
                for k in range(i):
                    l, r = mtx[j][j + k], mtx[j + k + 1][j + i]
                    for prod in get_pairs(cfg):
                        if prod.body[0] in l and prod.body[1] in r:
                            mtx[j][j + i].add(prod.head)

        return cfg.start_symbol in mtx[0][n - 1]

    def cfpq(grammar: CFG, graph: Graph):
        n = graph.size

        if n == 0:
            return False

        res = {}
        m = deque()

        if grammar.generate_epsilon():
            mtx = Matrix.sparse(BOOL, n, n)
            for i in range(n):
                mtx[i, i] = True
                m.append((grammar.start_symbol, i, i))
            res[grammar.start_symbol] = mtx

        cfg = grammar.to_normal_form()

        for t, mtx in graph.labels_adj.items():
            for prod in cfg.productions:
                if prod.body == [Terminal(t)]:
                    res[prod.head] = mtx

        for var, mtx in res.items():
            for i, j, _ in zip(*mtx.to_lists()):
                m.append((var, i, j))

        while m:
            to_add = []
            var, st, end = m.popleft()

            for new_var, mtx in res.items():
                for new_st, _ in mtx[:, st]:
                    for prod in get_pairs(cfg):
                        b = prod.body
                        h = prod.head
                        if (
                                list(b) == [new_var, var]
                                and (h not in res
                                     or (new_st, end) not in res[h])
                        ):
                            m.append((h, new_st, end))
                            to_add.append((h, new_st, end))

            for new_var, mtx in res.items():
                for new_end, _ in mtx[end, :]:
                    for prod in get_pairs(cfg):
                        b = prod.body
                        h = prod.head
                        if (
                                list(b) == [var, new_var]
                                and (h not in res
                                     or (st, new_end) not in res[h])
                        ):
                            m.append((h, st, new_end))
                            to_add.append((h, st, new_end))

            for var, st, end in to_add:
                mtx = res.get(var, Matrix.sparse(BOOL, n, n))
                mtx[st, end] = True
                res[var] = mtx

        return res.get(cfg.start_symbol)
