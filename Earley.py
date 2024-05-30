from Grammar import *


class Situation:
    def __init__(
            self,
            nterm: NTerminal,
            rule: tuple[str | NTerminal],
            dot_pos: int = 0,
            index: int = 0
    ):
        self.nterm: NTerminal = nterm
        self.rule: tuple[str | NTerminal] = rule
        self.dot_pos: int = dot_pos
        self.index: int = index

    def __eq__(self, other: 'Situation'):
        return (
                self.nterm == other.nterm and
                self.rule == other.rule and
                self.dot_pos == other.dot_pos and
                self.index == other.index
        )

    def __contains__(self, item: str | NTerminal):
        return item in self.rule

    def __getitem__(self, item):
        return self.rule[item]

    def __repr__(self):
        res = ''.join(str(i) for i in self.rule)
        res = res[0:self.dot_pos] + '*' + res[self.dot_pos:]
        return str(self.nterm) + ' -> ' + res

    def __hash__(self):
        return hash((self.nterm, self.rule, self.dot_pos, self.index))

    def after_dot(self):
        return self.rule[self.dot_pos] if self.dot_pos < len(self.rule) else None

    def before_dot(self):
        return self.rule[self.dot_pos - 1] if self.dot_pos != 0 else None

    def advance(self, n: int = 1):
        return Situation(self.nterm, self.rule, self.dot_pos + n, self.index)

    def copy(self):
        return Situation(self.nterm, self.rule, self.dot_pos, self.index)


def scan(D: list[list[Situation]], j: int, grammar: Grammar, input_str: str):
    if j == 0:
        return
    for situation in D[j - 1]:
        if situation.after_dot() == input_str[j - 1]:
            D[j].append(situation.advance())


def complete(D: list[list[Situation]], j: int, grammar: Grammar, input_str: str):
    new_situations = []
    for final_situation in D[j]:
        if final_situation.after_dot() is None:
            for situation in D[final_situation.index]:
                if situation.after_dot() == final_situation.nterm:
                    new_situations.append(situation.advance())
    D[j].extend(new_situations)


def predict(D: list[list[Situation]], j: int, grammar: Grammar, input_str: str):
    new_situations = []
    for situation in D[j]:
        next_symbol = situation.after_dot()
        if next_symbol is not None and isinstance(next_symbol, NTerminal):
            for rule in grammar.rules()[next_symbol]:
                new_situations.append(Situation(next_symbol, rule, index=j))
    D[j].extend(new_situations)


def earley(grammar: Grammar, input_str: str, log=False):
    D = [[] for _ in range(len(input_str) + 1)]
    D[0].append(
        Situation(nterm("S'"), (grammar.start_nterm,))
    )
    for j in range(len(input_str) + 1):
        scan(D, j, grammar, input_str)
        prev = []
        while prev != D[j]:
            prev = list(set(D[j]))
            complete(D, j, grammar, input_str)
            predict(D, j, grammar, input_str)
            D[j] = list(set(D[j]))

    if log:
        print(*D, sep='\n', end='\n\n')
    final_situation = Situation(nterm("S'"), (grammar.start_nterm,), dot_pos=1)
    return final_situation in D[len(input_str)]


if __name__ == '__main__':
    greibach_grammar = (Grammar(start_nterm='S')
                        .add_rule_literal('S -> + a \B')
                        .add_rule_literal('B -> b \B c')
                        .add_rule_literal('B -> b b c c'))
    print(earley(greibach_grammar, '+abbcc'))
