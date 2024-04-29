from isa import Instruction, Opcode
import re

def parse_int_or_none(a: str) -> int | None:
    try:
        return int(a)
    except:
        return None

def parse_lines(lines: list[str]) -> list[Instruction]:
    instructions = []
    labels = parse_labels(lines)
    for i in range(len(lines)):
        line = lines[i]
        _, opcode, arg = split_instruction(line)
        instructions += [Instruction(Opcode[opcode], None)]
    return instructions


def parse_labels(lines: list[str]) -> dict[str, int]:
    pattern = re.compile(r"^([\w\d]+):\s")
    labels = {}
    for i in range(len(lines)):
        line = lines[i]
        label, _, _ = split_instruction(line)
        if label != "":
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
    return "", splitted[0], ""
