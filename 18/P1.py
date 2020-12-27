from typing import List


def evaluate(expression: List[str]) -> int:
    operators: List[str] = []
    operands: List[int] = []
    for character in expression:
        if character in ["+", "*", "("]:
            operators.append(character)
        elif character in [")"]:
            subexpression: List[str] = []
            while True:
                last_operator = operators.pop()
                if last_operator == "(":
                    break
                subexpression.insert(0, str(operands.pop()))
                subexpression.insert(0, last_operator)
            subexpression.insert(0, str(operands.pop()))
            subexpression_result = evaluate(subexpression)
            operands.append(subexpression_result)
        else:
            operands.append(int(character))
    while True:
        if len(operands) == 1:
            break
        operator = operators.pop(0)
        result: int
        if operator == "*":
            result = operands.pop(0) * operands.pop(0)
        elif operator == "+":
            result = operands.pop(0) + operands.pop(0)
        operands.insert(0, result)
    return operands[0]


def solve() -> str:
    result = 0

    file = open("input.txt", "r")
    for line in file:
        result += evaluate(list(line[:-1].replace(" ", "")))

    return str(result)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
