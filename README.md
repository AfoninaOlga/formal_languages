# SPBU Formal Languages Course

## Required libriries:
- [pyformlang](https://pypi.org/project/pyformlang/)
- [pygraphblas](https://github.com/michelp/pygraphblas)


## Assignment 1 [![Build Status](https://travis-ci.com/AfoninaOlga/formal_languages.svg?branch=assignment_1)](https://travis-ci.com/AfoninaOlga/formal_languages)
Simple matrix multiplication test using ```pygraphblas``` and automata intersection test using ```pyformlang```.

### Run
Tests can be run by ```pytest```

## Assignment 2 [![Build Status](https://travis-ci.com/AfoninaOlga/formal_languages.svg?branch=assignment_2)](https://travis-ci.com/AfoninaOlga/formal_languages)
Simple tests for graph intersection using tensor product.

### Run
- Tests can be run by ```python -m pytest```
- To get intersection of two graphs read from files run ```python src\main.py [path to file with adges] [path to file with regex]```, where the first file consists of triples of the form: ```"{vertex number} {label} {vertex number}"``` and the second one contains a ```regular expression``` (see examples in data folder).

## Assignment 4 [![Build Status](https://travis-ci.com/AfoninaOlga/formal_languages.svg?branch=assignment_4)](https://travis-ci.com/AfoninaOlga/formal_languages)
Implementation of CYK and CFPQ algorithms.

### Run
Tests can be run by ```pytest```

## Assignment 5 [![Build Status](https://travis-ci.com/AfoninaOlga/formal_languages.svg?branch=assignment_5)](https://travis-ci.com/AfoninaOlga/formal_languages)
Implementation of CFPQ algorithms using matrix multiplication and tensor product.

### Run
Tests can be run by ```pytest```
