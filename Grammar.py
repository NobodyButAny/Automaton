from typing import Dict


class NTerminal:
    def __init__(self, symbol: str):
        self._symbol: str = symbol

    def get(self) -> str:
        return self._symbol

    def __eq__(self, other: 'NTerminal'):
        return isinstance(other, NTerminal) and self._symbol == other._symbol

    def __hash__(self):
        return self._symbol.__hash__()

    def __repr__(self):
        return f'\\{self._symbol}'

    def __str__(self):
        return '\\' + self._symbol


def nterm(symbol: str | NTerminal):
    return symbol if isinstance(symbol, NTerminal) else NTerminal(symbol)


def list_replace(lst, target, sublist):
    res = []
    for i, el in enumerate(lst):
        if el == target:
            for j in sublist:
                res.append(j)
        else:
            res.append(el)
    return res


class Grammar:

    def __init__(self, infer_spaces=False, start_nterm: NTerminal | str = None, spacer=None):
        self._rules: Dict[NTerminal, list[tuple[str | NTerminal]]] = {}
        if spacer is None:
            self.spacer = ' ' if infer_spaces else ''
        else:
            self.spacer = spacer
        if start_nterm:
            self.start_nterm: NTerminal = nterm(start_nterm)

    def __repr__(self):
        res: str = ''
        for rule_nterm in self._rules:
            for rule in self._rules[rule_nterm]:
                rhs = self.spacer.join(str(symbol) for symbol in rule)
                if rule_nterm == self.start_nterm:
                    res = f'{rule_nterm} -> {rhs} \n' + res
                else:
                    res = res + f"{rule_nterm} -> {rhs} \n"
        return res

    def rules(self):
        return self._rules

    def add_rule(self, nterminal: NTerminal, *symbols: str | NTerminal):
        if nterminal not in self._rules:
            self._rules[nterminal] = []
        self._rules[nterminal].append(symbols)
        return self

    def add_rule_literal(self, literal: str):
        if literal.find(' -> ') == -1:
            raise ValueError("Invalid literal. Should contain ' -> '")

        split_result = literal.split(' -> ', maxsplit=1)
        nterminal = nterm(split_result[0])
        sequence: str = split_result[1]
        rule = tuple(
            token if token[0] != '\\' else nterm(token[1:])
            for token in sequence.split(' ')
        )
        return self.add_rule(nterminal, *rule)

    def generate(self, n=10):
        fin = set()
        non_fin = set()
        non_fin.add((self.start_nterm,))
        while len(fin) < n and non_fin:
            tmp = []
            rm_queue = []
            for situation in non_fin:
                for symbol in situation:
                    if symbol not in self.rules():
                        continue
                    for rule in self.rules()[symbol]:
                        tmp.append(list_replace(situation, symbol, rule))
                rm_queue.append(situation)

            for situation in rm_queue:
                non_fin.remove(situation)

            for situation in tmp:
                is_fin = True
                for non_terminal in self.rules():
                    if non_terminal in situation:
                        is_fin = False
                if is_fin:
                    fin.add(tuple(situation))
                else:
                    non_fin.add(tuple(situation))
        return {self.spacer.join(st) for st in fin}


if __name__ == "__main__":
    test = (Grammar(start_nterm='A', infer_spaces=True)
            .add_rule_literal('A -> I \\positive eating \\fooditem')
            .add_rule_literal('fooditem -> apple')
            .add_rule_literal('positive -> like'))

    greibach_grammar = (Grammar(start_nterm='S')
                        .add_rule_literal('S -> a \\G1 \\B')
                        .add_rule_literal('S -> a \\B \\B')
                        .add_rule_literal('G1 -> a \\G1 \\B \\B')
                        .add_rule_literal('G1 -> a \\B \\B')
                        .add_rule_literal('B -> b'))
    print(test)
