from Grammar import *

task_7_grammar = (Grammar(start_nterm='S', infer_spaces=True)
                  .add_rule_literal('S -> if \E then \S else \S')
                  .add_rule_literal('S -> a')
                  .add_rule_literal('E -> \E or b')
                  .add_rule_literal('E -> b'))

print(*task_7_grammar.generate(n=6), sep='\n')
