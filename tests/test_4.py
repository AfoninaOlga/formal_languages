from pygraphblas import *
from src.graph import Graph
from src.cnf import AlgoCFG


def test_empty_eps_cyk():
    cnf = AlgoCFG.read_cnf("data/grammar_eps.txt")
    assert AlgoCFG.cyk(cnf, '')


def test_assertion_eps_cyk():
    cnf = AlgoCFG.read_cnf("data/grammar_eps.txt")
    assert AlgoCFG.cyk(cnf, 'abab')
    assert AlgoCFG.cyk(cnf, 'ababab')
    assert AlgoCFG.cyk(cnf, 'aaabbb')
    assert AlgoCFG.cyk(cnf, 'aaabbbabab')


def test_empty_cyk():
    cnf = AlgoCFG.read_cnf("data/grammar.txt")
    assert not AlgoCFG.cyk(cnf, '')


def test_assertion_cyk():
    cnf = AlgoCFG.read_cnf("data/grammar.txt")
    assert AlgoCFG.cyk(cnf, 'aaaa')
    assert AlgoCFG.cyk(cnf, 'abababab')
    assert AlgoCFG.cyk(cnf, 'abbbbbb')


def test_cfpq_loop():
    graph = Graph()
    graph.read_from_txt("data/graph_loop.txt")
    cnf = AlgoCFG.read_cnf("data/grammar_eps.txt")
    assert AlgoCFG.cfpq(cnf, graph).nvals == 13


def test_cfpq_empty():
    graph = Graph()
    graph.read_from_txt("data/graph.txt")
    cnf = AlgoCFG.read_cnf("data/grammar.txt")
    assert not AlgoCFG.cfpq(cnf, graph)

def test_cfpq_loops():
    graph = Graph()
    graph.read_from_txt("data/graph_loops.txt")
    cnf = AlgoCFG.read_cnf("data/grammar.txt")
    assert AlgoCFG.cfpq(cnf, graph).nvals == 5
