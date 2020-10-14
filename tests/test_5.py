from src.graph import Graph
from src.cnf import AlgoCFG


def test_cpfq_mtx_empty():
    graph = Graph()
    graph.read_from_txt("data/graph.txt")
    cnf = AlgoCFG.read_cnf("data/grammar.txt")
    assert not AlgoCFG.cfpq_mtx(cnf, graph)

def test_cfpq_mtxm_loop():
    graph = Graph()
    graph.read_from_txt("data/graph_loop.txt")
    cnf = AlgoCFG.read_cnf("data/grammar_eps.txt")
    assert AlgoCFG.cfpq_mtx(cnf, graph).nvals == 13

def test_cfpq_mtx_loops():
    graph = Graph()
    graph.read_from_txt("data/graph_loops.txt")
    cnf = AlgoCFG.read_cnf("data/grammar.txt")
    assert AlgoCFG.cfpq_mtx(cnf, graph).nvals == 5


def test_cpfq_tensor_empty():
    graph = Graph()
    graph.read_from_txt("data/graph.txt")
    cnf = AlgoCFG.read_cnf("data/grammar.txt")
    assert not AlgoCFG.cfpq_mtx(cnf, graph)

def test_cfpq_tensor_loop():
    graph = Graph()
    graph.read_from_txt("data/graph_loop.txt")
    cnf = AlgoCFG.read_cnf("data/grammar_eps.txt")
    assert AlgoCFG.cfpq_mtx(cnf, graph).nvals == 13

def test_cfpq_tensor_loops():
    graph = Graph()
    graph.read_from_txt("data/graph_loops.txt")
    cnf = AlgoCFG.read_cnf("data/grammar.txt")
    assert AlgoCFG.cfpq_mtx(cnf, graph).nvals == 5
