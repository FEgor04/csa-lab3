from isa import Instruction, Opcode, Addressing


def parse_int_or_none(a: str) -> int | None:
    try:
        return int(a)
    except ValueError:
        return None


def is_label(s: str) -> bool:
    return s != "" and parse_int_or_none(s) is None and s[0] != "'" and s[-1] != "'"


def parse_lines(lines: list[str]) -> list[Instruction]:
    instructions = []
    labels = parse_labels(lines)
    for i in range(len(lines)):
        line = lines[i]
        if line == "":
            continue
        _, opcode, arg_raw = split_instruction(line)
        arg, addressing = parse_argument(arg_raw, labels)
        if opcode == "VAR":
            instructions += [
                Instruction(Opcode[opcode], arg, addressing)
            ]
        else:
            instructions += [Instruction(Opcode[opcode], arg, addressing)]
    return instructions


def parse_labels(lines: list[str]) -> dict[str, int]:
    labels = {}
    for i in range(len(lines)):
        line = lines[i]
        label, _, _ = split_instruction(line)
        if is_label(label):
            labels[label] = i
    return labels

def parse_argument(arg: str, labels: dict[str, int]) -> tuple[str | int, Addressing]:
    if len(arg) == 0:
        return None, None
    addressing = parse_addressing(arg)
    if addressing is Addressing.IMMEDIATE:
        if arg[0] == "'" and arg[-1] == "'": # is literal
            return arg[1:-1], addressing
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
