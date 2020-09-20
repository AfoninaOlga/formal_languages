import sys
from graph import Graph


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Wrong number of arguments! Expected 3, got {sys.argv}.')
    else:
        g1 = Graph()
        g2 = Graph()
        g1.read_from_txt(sys.argv[1])
        g2.read_from_regex(sys.argv[2])
        g1.intersect(g2)
