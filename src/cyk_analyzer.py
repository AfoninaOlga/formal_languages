from src.cnf import AlgoCFG


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


def cyk_analyzer(script):
    cnf = AlgoCFG.read_cnf("syntax.txt")
    script = get_lexemes(script)
    return AlgoCFG.cyk(cnf, script)
