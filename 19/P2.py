from typing import Dict, List
from os import linesep
from re import search, fullmatch, findall


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


def rule_0_matches(rules: Dict[str, str], line: str) -> bool:
    rule42 = rules["42"]
    rule42 = resolve_rule(rule42, rules)
    rule31 = rules["31"]
    rule31 = resolve_rule(rule31, rules)
    rule_0_expression = f"({rule42}{{2,}})({rule31}+)"
    matches = fullmatch(rule_0_expression, line)
    if matches is None:
        return False
    rule42_groups, rule31_groups = matches.groups()
    return len(findall(rule42, rule42_groups)) > len(findall(rule31, rule31_groups))


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

    matched_messages = 0
    for line in file:
        message = line.strip()
        if rule_0_matches(rules, message):
            matched_messages += 1
    return str(matched_messages)


def main() -> None:
    print(solve())


if __name__ == "__main__":
    main()
