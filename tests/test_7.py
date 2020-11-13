from src.cnf import AlgoCFG
from pyformlang.cfg import Terminal


keywords = {
    'connect', 'select', 'from', 'intersect', 'name'
    , 'eps', 'count', 'edges', 'query', 'alt', 'seq'
    , 'star', 'plus', 'opt'
}


def get_lexemes(script):
    lexemes = []
    for w in script.split():
        if w in keywords:
            lexemes.append(w)
        else:
            lexemes.extend(w)
    return lexemes


def test_empty():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = ''
    assert AlgoCFG.cyk(cnf, script)


def test_connect1():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes('connect from ;')
    assert not AlgoCFG.cyk(cnf, script)


def test_connect2():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes('connect "graph" ;')
    assert AlgoCFG.cyk(cnf, script)


def test_connect3():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes('connect g h;')
    assert not AlgoCFG.cyk(cnf, script)


def test_select1():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes('select edges from name "ggg" ;')
    assert AlgoCFG.cyk(cnf, script)


def test_select2():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes('select edges name "ggg" ;')
    assert not AlgoCFG.cyk(cnf, script)


def test_select3():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes(
        'select edges from name "g" intersect name "h" intersect name "j";'
    )
    assert AlgoCFG.cyk(cnf, script)


def test_pattern1():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes(
        'select count edges from query a star seq b plus;'
    )
    assert AlgoCFG.cyk(cnf, script)


def test_pattern2():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes(
        'select count edges from query a star b plus;'
    )
    assert not AlgoCFG.cyk(cnf, script)


def test_pattern3():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes(
        'select count edges from query str star alt b opt seq graph;'
    )
    assert AlgoCFG.cyk(cnf, script)


def test_script1():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes(
        '''
        connect "graph";
        select count edges from query a star seq b plus;
        select edges from name "graph" intersect name "grammar" intersect query a star seq b;
        connect "string";
        select edges from query a alt b star  intersect query a seq b;
        '''
    )
    assert AlgoCFG.cyk(cnf, script)


def test_script2():
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes(
        '''
        connect "graph";
        select count edges from query a star seq b plus
        select edges from name "graph" intersect name "grammar" intersect query a star seq b;
        connect "string";
        select edges from query a alt b star  intersect query a seq b;
        '''
    )
    assert not AlgoCFG.cyk(cnf, script)
