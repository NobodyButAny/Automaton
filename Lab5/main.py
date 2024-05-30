import re

PREC = {'^': 4, '+': 3, '->': 2, '<->': 1}
OPERATORS = list(PREC.keys())


def tokenize(logic_expr: str) -> list[str]:
    pattern = r'(\b\w+\b|->|<->|\^|\+|\(|\))'
    tokens = re.findall(pattern, logic_expr)
    return tokens


def dijkstra_into_rpn(expr: str) -> list[str]:
    tokens = tokenize(expr)
    op_stack = []
    out_queue = []
    for tk in tokens:
        if tk in OPERATORS:  # если в стэке более важный оператор - в очередь
            while op_stack and op_stack[-1] != '(' and PREC[op_stack[-1]] >= PREC[tk]:
                out_queue.append(op_stack.pop())
            op_stack.append(tk)
        elif tk == '(':  # скобка - маркер для )
            op_stack.append(tk)
        elif tk == ')':  # если наехали на конец скобок, то вопреки приоритетам кидаем вперёд операции в них
            while op_stack and op_stack[-1] != '(':  # пашем до маркера (
                out_queue.append(op_stack.pop())
            op_stack.pop()
        elif tk not in OPERATORS:  # чиселка в очередь
            out_queue.append(tk)
    while op_stack:
        out_queue.append(op_stack.pop())
    return out_queue


def to_bool(expr: str | bool):
    return expr if isinstance(expr, bool) else True if expr == 'T' else False


def eval_rpn(expr: list):
    i = len(expr) - 1
    while len(expr) != 1:
        parent = expr[i]
        if expr[i - 1] in OPERATORS:
            i -= 1
            continue
        if expr[i - 2] in OPERATORS:
            i -= 2
            continue
        left = expr[i - 2]
        right = expr[i - 1]
        match parent:
            case '^':
                expr[i] = to_bool(left) and to_bool(right)
            case '+':
                expr[i] = to_bool(left) or to_bool(right)
            case '->':
                expr[i] = not to_bool(left) or to_bool(right)
            case '<->':
                expr[i] = to_bool(left) == to_bool(right)
        del expr[i - 2]
        del expr[i - 2]
        i = len(expr) - 1
    return expr.pop()


if __name__ == '__main__':
    expression = input()
    print(eval_rpn(into_rpn(expression)))
