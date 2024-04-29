from isa import Instruction, Opcode


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
        if opcode == "VAR":
            arg_parsed = parse_int_or_none(arg_raw)
            if arg_parsed is None:
                arg_parsed = arg_raw[1:-1]
            instructions += [Instruction(Opcode[opcode], arg_parsed)]
        else:
            arg_parsed = parse_int_or_none(arg_raw)
            if arg_raw != "" and arg_parsed is None:
                arg_parsed = labels[arg_raw]
            instructions += [Instruction(Opcode[opcode], arg_parsed)]
    return instructions


def parse_labels(lines: list[str]) -> dict[str, int]:
    labels = {}
    for i in range(len(lines)):
        line = lines[i]
        label, _, _ = split_instruction(line)
        if is_label(label):
            labels[label] = i
    return labels


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
