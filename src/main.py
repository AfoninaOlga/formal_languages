import sys
import timeit
from statistics import fmean

from graph import Graph

if __name__ == '__main__':
    graphs = ['LUBM300', 'LUBM500', 'LUBM1M', 'LUBM1.5M', 'LUBM1.9M']
    regexes = ['q1_0', 'q2_0', 'q3_0', 'q4_2_0', 'q5_0', 'q6_0', 'q7_0', 'q8_0', 'q9_2_0', 'q10_2_0', 'q11_2_0',
               'q_12_0', 'q_13_0', 'q_14_0', 'q_15_0', 'q_16_0']
    for g in graphs:
        for reg in regexes:
            g1 = Graph()
            g2 = Graph()
            output = open("results.txt", 'a')
            graph_setup = ''' 
from __main__ import inter, g1, g2 
from graph import Graph'''
            g1.read_from_txt(f"refinedDataForRPQ/{g}/{g}.txt")
            g2.read_from_regex(f"refinedDataForRPQ/{g}/regexes/{reg}")
            inter = g1.intersect(g2)
            intersection_time = round(fmean(timeit.repeat("g1.intersect(g2)",
                                                          setup=graph_setup,
                                                          repeat=5,
                                                          number=1)), 6)
            square_time = round(fmean(timeit.repeat("inter.transitive_closure_sq()",
                                                    setup=graph_setup,
                                                    repeat=5,
                                                    number=1)), 6)
            mul_time = round(fmean(timeit.repeat("inter.transitive_closure_mul()",
                                                 setup=graph_setup,
                                                 repeat=5,
                                                 number=1)), 6)
            print_time = round(fmean(timeit.repeat("inter.print_pairs()",
                                                   setup=graph_setup,
                                                   repeat=5,
                                                   number=1)), 6)
            output.write(
                f"{g} {reg}\ninter = {intersection_time}\nprint = {print_time}\nsq = {square_time}\nmul = {mul_time}\n")
