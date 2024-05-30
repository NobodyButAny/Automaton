import re

PREC = {'*': 4, '/': 3, '+': 2, '-': 1}
OPERATORS = list(PREC.keys())


def tokenize(expr: str) -> list[str]:  # раскидаем на токены, regex из сети тыртырнет
    return [i for i in re.split(' *([+\-*/()]|\d+\.\d+|\d+) *', expr) if i != '']


def into_rpn(expr: str) -> list[str]:
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

# 2 12 +
# ['4', '18', '9', '3', '-', '/', '+']
def eval_rpn(expr: list):  # само за себя говорит
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
            case '+':
                expr[i] = float(left) + float(right)
            case '-':
                expr[i] = float(left) - float(right)
            case '*':
                expr[i] = float(left) * float(right)
            case '/':
                if float(right) == 0:
                    print("Деление на ноль в выражении!")
                    exit()
                expr[i] = float(left) / float(right)
        del expr[i - 2]
        del expr[i - 2]
        i = len(expr) - 1
    return expr.pop()


if __name__ == '__main__':
    while expr := input("Введите выражение:\n > "):
        expr = expr.split("=")[0]
        print(eval_rpn(into_rpn(expr)))
