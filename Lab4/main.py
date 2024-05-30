from Kasami import *
from Grammar import *
from Earley import *

if __name__ == '__main__':
    free_grammar = (Grammar(start_nterm='S')
                    .add_rule_literal('S -> \PA \Bp')
                    .add_rule_literal('PA -> \P \A')
                    .add_rule_literal('Bp -> \B \Br')
                    .add_rule_literal('Br -> \Bp \C')
                    .add_rule_literal('Br -> c')
                    .add_rule_literal('A -> a')
                    .add_rule_literal('P -> +')
                    .add_rule_literal('B -> b')
                    .add_rule_literal('C -> c'))

    # string = '+a' + 'b'*20 + 'c'*20
    string = '+abbbccc'
    print(f'Грамматика \n{free_grammar}')
    print('Эрли')
    print(
        'Строка принята' if earley(free_grammar, string, log=True)
        else 'Строка не принята',
        end='\n\n'
    )

    print('Кок-Янгер-Касами')
    print(
        'Строка принята' if CYK(free_grammar, string, log=True)
        else 'Строка не принята'
    )
