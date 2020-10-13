from pygraphblas import *
from src.graph import Graph


def test_reachable_from():
    g = Graph()
    g.read_from_txt("data/g3.txt")

    expected = Matrix.sparse(BOOL, g.size, g.size)
    for v in range(1, g.size):
        expected[0, v] = True
    for v in range(1, g.size):
        expected.assign_row(v, Vector.sparse(BOOL, g.size).full(0))

    assert g.reachable_from({0}).iseq(expected)


def test_reachable_from_to():
    g = Graph()
    g.read_from_txt("data/g3.txt")

    expected = Matrix.sparse(BOOL, g.size, g.size)
    for v in range(2, g.size):
        expected.assign_row(v, Vector.sparse(BOOL, g.size).full(0))
    for v in range(1, g.size):
        expected.assign_col(v, Vector.sparse(BOOL, g.size).full(0))

    assert g.reachable_from_to({0, 1}, {0}).iseq(expected)


def test_intersection():
    g1 = Graph()
    g2 = Graph()

    g1.read_from_txt("data/g1.txt")
    g2.read_from_regex("data/r1.txt")

    intersection = g1.intersect(g2)

    assert intersection.labels_adj["a"].nvals == g1.labels_adj["a"].nvals
    assert intersection.labels_adj["b"].nvals == g1.labels_adj["b"].nvals


def test_intersection_empty():
    g1 = Graph()
    g2 = Graph()

    g1.read_from_txt("data/g2.txt")
    g2.read_from_regex("data/r2.txt")

    intersection = g1.intersect(g2)

    for l in intersection.labels_adj:
        assert intersection.labels_adj[l].nvals == 0


def test_intersection_gt():
    g1 = Graph()
    g2 = Graph()

    g1.read_from_txt("data/g3.txt")
    g2.read_from_regex("data/r3.txt")

    intersection = g1.intersect(g2)
    for l in intersection.labels_adj:
        assert intersection.labels_adj[l].nvals == g1.labels_adj[l].nvals
        assert g2.labels_adj[l].nvals != 0
