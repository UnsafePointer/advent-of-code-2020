from typing import List


def precedence(operator: str) -> int:
    if operator == "+":
        return 1
    return 0


def operate(operand1: int, operand2: int, operator: str) -> int:
    if operator == "+":
        return operand1 + operand2
    elif operator == "*":
        return operand1 * operand2
    return -1


def evaluate(expression: List[str]) -> int:
    operators: List[str] = []
    operands: List[int] = []
    for character in expression:
        if character in ["+", "*"]:
            while len(operators) > 0 and precedence(operators[-1]) > precedence(
                character
            ):
                operands.append(
                    operate(operands.pop(), operands.pop(), operators.pop())
                )
            operators.append(character)
        elif character in ["("]:
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
        operands.append(operate(operands.pop(), operands.pop(), operators.pop()))
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
