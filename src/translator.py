import json
import sys
from isa import Instruction, Opcode, Addressing
import re


def parse_int_or_none(a: str) -> int | None:
    try:
        return int(a)
    except ValueError:
        return None


def is_label(s: str) -> bool:
    return s != "" and parse_int_or_none(s) is None and s[0] != "'" and s[-1] != "'"


def parse_lines(lines: list[str]) -> list[Instruction]:
    lines = expand_lines(lines)
    instructions = []
    labels = parse_labels(lines)
    for i in range(len(lines)):
        line = lines[i]
        if line == "":
            continue
        _, opcode, arg_raw = split_instruction(line)
        arg, addressing = parse_argument(arg_raw, labels)
        instructions += [Instruction(Opcode[opcode], arg, addressing)]
    pc = labels["START"] if "START" in labels else 0
    return instructions, pc


def parse_labels(lines: list[str]) -> dict[str, int]:
    labels = {}
    for i in range(len(lines)):
        line = lines[i]
        label, _, _ = split_instruction(line)
        if is_label(label):
            labels[label] = i
    return labels


def parse_argument(arg: str, labels: dict[str, int]) -> tuple[int, Addressing]:
    if len(arg) == 0:
        return None, None
    addressing = parse_addressing(arg)
    if addressing is Addressing.IMMEDIATE:
        if arg[0] == "'" and arg[-1] == "'":  # is literal
            return ord(arg[1]), addressing
        if arg.isdecimal():
            return int(arg), addressing
        return labels[arg], addressing
    stripped = arg[1:-1]
    return int(stripped) if stripped.isdecimal() else labels[stripped], addressing


def parse_addressing(argument: str) -> Addressing | None:
    if len(argument) == 0:
        return None
    if argument[0] == "(" and argument[-1] == ")":
        return Addressing.DIRECT
    if argument[0] == "[" and argument[-1] == "]":
        return Addressing.INDIRECT
    assert argument[0] not in ["[", "("] and argument[-1] not in ["]", ")"]
    return Addressing.IMMEDIATE


def split_instruction(line: str) -> tuple[str, str, str]:
    """Парсит инструкцию и трансформирует ее в кортеж вида (метка, опкод, аргумент)"""
    splitted = line.split()
    if len(splitted) == 3:
        label, opcode, arg = splitted
        return label.split(":")[0], opcode, arg
    if len(splitted) == 2:
        if splitted[0].find(":") != -1:
            label, opcode = splitted
            return label.split(":")[0], opcode, ""
        opcode, arg = splitted
        return "", opcode, arg
    if len(splitted) == 1:
        return "", splitted[0], ""
    return "", "", ""


def expand_lines(lines: list[str]) -> list[str]:
    ans = []
    var_pattern = re.compile(r"(\w+:\s)?VAR\s'(\w+)'")
    for line in lines:
        match = var_pattern.match(line)
        if match is None:
            ans += [line]
            continue
        groups = match.groups()
        if len(groups) == 1:  # VAR 'test'
            label = None
            value = groups[0]
        else:
            label = groups[0]
            value = groups[1]
        if label:
            ans += [f"{label}VAR '{value[0]}'"]
            for c in value[1:]:
                ans += [f"VAR '{c}'"]
        else:
            for c in value:
                ans += [f"VAR '{c}'"]

    return ans


def convert_to_json(instructions: list[Instruction], pc: int) -> str:
    code = {
        "pc": pc,
        "instructions": instructions,
    }
    return json.dumps(code)


def main(input, output):
    with open(input, encoding="utf-8") as f:
        lines = f.readlines()
    instructions, pc = parse_lines(lines)
    json = convert_to_json(instructions, pc)
    with open(output, "w", encoding="utf-8") as f:
        f.write(json)


if __name__ == "__main__":
    assert (
        len(sys.argv) == 3
    ), "Wrong arguments: translator.py <input_file> <target_file>"
    _, input, output = sys.argv
    main(input, output)
