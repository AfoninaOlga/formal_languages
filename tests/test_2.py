import os, pytest
from pyformlang.regular_expression import Regex
from pygraphblas import *
from src.graph import Graph


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
