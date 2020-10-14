from collections import deque
from pyformlang.cfg import *
from pygraphblas import Matrix, BOOL
from src.graph import Graph


def get_pairs_and_units(cfg: CFG):
    pairs = []
    units = []
    for p in cfg.productions:
        if len(p.body) == 2:
            pairs.append(p)
        elif len(p.body) == 1:
            units.append(p)
    return pairs, units


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

        pairs, units = get_pairs_and_units(cfg)

        for i in range(n):
            for prod in units:
                if prod.body == [Terminal(word[i])]:
                    mtx[i][i].add(prod.head)

        for i in range(n):
            for j in range(n - i):
                for k in range(i):
                    l, r = mtx[j][j + k], mtx[j + k + 1][j + i]
                    for prod in pairs:
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
        pairs, units = get_pairs_and_units(cfg)

        for t, mtx in graph.labels_adj.items():
            for prod in units:
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
                    for prod in pairs:
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
                    for prod in pairs:
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

    def cfpq_mtx(grammar: CFG, graph: Graph):
        n = graph.size
        if not n:
            return False

        res = dict()
        res[grammar.start_symbol] = Matrix.sparse(BOOL, n, n)

        if grammar.generate_epsilon():
            for i in range(n):
                res[grammar.start_symbol][i, i] = True
        cfg = grammar.to_normal_form()
        pairs, units = get_pairs_and_units(cfg)

        for l, mtx in graph.labels_adj.items():
            for p in units:
                if Terminal(l) == p.body[0]:
                    if p.head in res:
                        res[p.head] += mtx.dup()
                    else:
                        res[p.head] = mtx.dup()

        changing = True
        while changing:
            changing = False
            for p in pairs:
                if p.body[0] in res and p.body[1] in res:
                    if p.head not in res:
                        res[p.head] = Matrix.sparse(BOOL, n, n)
                    old = res[p.head].nvals
                    res[p.head] += res[p.body[0]] @ res[p.body[1]]
                    changing |= old != res[p.head].nvals
        return res[cfg.start_symbol]

    def to_rfa(cfg: CFG):
        rfa = Graph()
        rfa.size = sum(len(p.body) + 1 for p in cfg.productions)
        prods_by_verts = {}
        i = 0
        for p in cfg.productions:
            rfa.start_states.add(i)
            prods_by_verts[i, i + len(p.body)] = p
            for v in p.body:
                rfa.set(v.value, Matrix.sparse(BOOL, rfa.size, rfa.size))
                rfa.labels_adj[v.value][i, i + 1] = True
                i += 1
            rfa.final_states.add(i)
            i += 1
        return rfa, prods_by_verts

    def cfpq_tensor(grammar: CFG, graph: Graph):
        n = graph.size
        if not n:
            return False
        rfa, prods_by_verts = AlgoCFG.to_rfa(grammar)
        res = graph.copy()
        for p in grammar.productions:
            if not p.body:
                res.set(p.head, Matrix.sparse(BOOL, n, n))
                for i in range(n):
                    res.labels_adj[p.head][i, i] = True
        intersection = res.intersect(rfa)
        n = intersection.size
        tc = res.transitive_closure_sq()
        changing = True
        while changing:
            prev = tc.nvals
            for (i, j, _) in tc:
                s, f = i % rfa.size, j % rfa.size
                if s in rfa.start_states and f in rfa.final_states:
                    s1, f1 = i // rfa.size, j // rfa.size
                    res.labels_adj[prods_by_verts[s, f]][s1, f1] = True
            intersection = res.intersect(rfa)
            tc = intersection.transitive_closure_sq()
            if tc.nvals == prev:
                changing = False
        return res.labels_adj[grammar.start_symbol]
