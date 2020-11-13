from src.cnf import AlgoCFG
from src.cyk_analyzer import cyk_analyzer


def test_empty():
    script = ''
    assert cyk_analyzer(script)


def test_connect1():
    script = 'connect from ;'
    assert not cyk_analyzer(script)


def test_connect2():
    script = 'connect "graph" ;'
    assert cyk_analyzer(script)


def test_connect3():
    script = 'connect g h;'
    assert not cyk_analyzer(script)


def test_select1():
    script = 'select edges from name "ggg" ;'
    assert cyk_analyzer(script)


def test_select2():
    script = 'select edges name "ggg" ;'
    assert not cyk_analyzer(script)


def test_select3():
    script = 'select edges from name "g" intersect name "h" intersect name "j";'
    assert cyk_analyzer(script)


def test_pattern1():
    script = 'select count edges from query a star seq b plus;'
    assert cyk_analyzer(script)


def test_pattern2():
    script = 'select count edges from query a star b plus;'
    assert not cyk_analyzer(script)


def test_pattern3():
    script = 'select count edges from query str star alt b opt seq graph;'
    assert cyk_analyzer(script)


def test_script1():
    script = '''
        connect "graph";
        select count edges from query a star seq b plus;
        select edges from name "graph" intersect name "grammar" intersect query a star seq b;
        connect "string";
        select edges from query a alt b star  intersect query a seq b;
        '''
    assert cyk_analyzer(script)


def test_script2():
    script = '''
        connect "graph";
        select count edges from query a star seq b plus
        select edges from name "graph" intersect name "grammar" intersect query a star seq b;
        connect "string";
        select edges from query a alt b star  intersect query a seq b;
        '''
    assert not cyk_analyzer(script)