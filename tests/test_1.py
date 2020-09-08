from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State, Symbol
from pygraphblas import Matrix

def test_dfa_intersection():
    dfa1 = DeterministicFiniteAutomaton()
    dfa2 = DeterministicFiniteAutomaton()

    state0 = State(0)
    state1 = State(1)

    a = Symbol("a")
    b = Symbol("b")

    dfa1.add_start_state(state0)
    dfa1.add_final_state(state1)
    dfa1.add_transition(state0, a, state1)
    dfa1.add_transition(state1, b, state1)

    dfa2.add_start_state(state0)
    dfa2.add_final_state(state1)
    dfa2.add_transition(state0, a, state1)
    dfa2.add_transition(state1, b, state1)

    result = dfa1 & dfa2

    assert result.is_equivalent_to(dfa1), "Error in dfa intersection"

def test_matrix_multiplication():
    mtx1 = Matrix.from_lists(
        [0, 0, 1, 3, 3, 4, 1, 5],
        [1, 3, 2, 4, 5, 2, 5, 4],
        [9, 3, 8, 6, 1, 4, 7, 2],)

    mtx2 = Matrix.from_lists(
        [0, 0, 1, 3, 3, 4, 1, 5],
        [1, 3, 2, 4, 5, 2, 5, 4],
        [9, 3, 8, 6, 1, 4, 7, 2],)
    
    result = mtx1 @ mtx2

    expected_result = Matrix.from_lists(
        [0, 0, 0, 1, 3, 3, 5],
        [2, 4, 5, 4, 2, 4, 2],
        [72, 18, 66, 14, 24, 2, 8])

    assert result.iseq(expected_result), "Error in matrix multiplication"
