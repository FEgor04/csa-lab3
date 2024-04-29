from isa import Instruction
import re

def parse_lines(lines: list[str]) -> list[Instruction]:
    return []

def parse_labels(lines: list[str]) -> dict[str, int]:
    pattern = re.compile(r"^([\w\d]+):\s")
    labels = {}
    for i in range(len(lines)):
        line = lines[i]
        labels_for_line = pattern.findall(line)
        if len(labels_for_line) > 0:
            labels.update({labels_for_line[0]: i})
    return labels

def split_instruction(line: str) -> tuple[str, str, str]:
    """Парсит инструкцию и трансформирует ее в кортеж вида (метка, опкод, аргумент)"""
    return ("", "", "")

