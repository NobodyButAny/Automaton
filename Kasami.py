from Grammar import *


def has_rule(grammar: Grammar, nterm: NTerminal, symb: str | NTerminal):
    for case in grammar.rules()[nterm]:
        for sym in case:
            if sym == symb:
                return True
    return False


def print_table(table):
    for sym in table:
        print(sym)
        for i in range(len(table[sym])):
            for j in range(len(table[sym][i])):
                print(1 if table[sym][i][j] else 0, end=' ')
            print('')
        print('')


def CYK(grammar: Grammar, string: str, log=False):
    d = dict()
    n = len(string)
    for i in grammar.rules():
        d[i] = [
            [False for j in range(n)]
            for k in range(n)
        ]

    for i in range(n):
        for nterm in grammar.rules():
            d[nterm][i][i] = has_rule(grammar, nterm, string[i])

    for m in range(1, n):
        for i in range(n):
            if m + i >= n:
                continue
            j = m + i
            for nterm in grammar.rules():
                d[nterm][i][j] = any([
                    any([
                        d[rule[0]][i][k] and d[rule[1]][k + 1][j]
                        for k in range(i, j)
                    ])
                    for rule in grammar.rules()[nterm] if len(rule) == 2
                ])

    if log:
        print_table(d)
    return d[grammar.start_nterm][0][n - 1]
