from typing import Dict, List
from os import linesep
from re import search


def resolve_rule(rule: str, rules: Dict[str, str]) -> str:
    if rule.isdigit():
        return resolve_rule(rules[rule], rules)
    elif '"' in rule:
        return rule.replace('"', "")
    elif "|" in rule:
        splitted = rule.split("|")
        return f"(?:{resolve_rule(splitted[0].strip(), rules)}|{resolve_rule(splitted[1].strip(), rules)})"
    else:
        splitted = rule.split(" ")
        rule_to_resolve = ""
        for a_rule in splitted:
            rule_to_resolve += resolve_rule(a_rule, rules)
        return rule_to_resolve


def solve() -> str:
    file = open("input.txt", "r")
    rules: Dict[str, str] = {}
    for line in file:
        if line == linesep:
            break
        splitted = line.split(":")
        key = splitted[0]
        rule = splitted[1].strip()
        rules[key] = rule

    rule = rules["0"]
    rule = resolve_rule(rule, rules)
    rule = f"^{rule}$"

    matched_messages = 0
    for line in file:
        message = line.strip()
        if search(rule, message):
            matched_messages += 1
    return str(matched_messages)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
